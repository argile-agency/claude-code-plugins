#!/usr/bin/env python3
"""
PII (Personally Identifiable Information) Detection Script

Scans codebase for personal data patterns to support GDPR compliance analysis.
Detects: emails, phone numbers, SSN, credit cards, IPs, and more.

Usage:
    python detect-pii.py [directory]
    python detect-pii.py --json [directory]  # JSON output
    python detect-pii.py --help
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

# PII Detection Patterns
PII_PATTERNS = {
    'email': {
        'pattern': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        'severity': 'high',
        'gdpr_article': 'Art. 4(1)',
        'description': 'Email address (direct identifier)'
    },
    'ssn_us': {
        'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
        'severity': 'critical',
        'gdpr_article': 'Art. 4(1)',
        'description': 'US Social Security Number'
    },
    'credit_card': {
        'pattern': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        'severity': 'critical',
        'gdpr_article': 'Art. 4(1)',
        'description': 'Credit card number'
    },
    'phone': {
        'pattern': r'\b(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        'severity': 'high',
        'gdpr_article': 'Art. 4(1)',
        'description': 'Phone number'
    },
    'ip_address': {
        'pattern': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        'severity': 'medium',
        'gdpr_article': 'Art. 4(1)',
        'description': 'IP address (indirect identifier)'
    },
    'uuid': {
        'pattern': r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
        'severity': 'low',
        'gdpr_article': 'Art. 4(1)',
        'description': 'UUID (potential user identifier)'
    },
    'postal_code_us': {
        'pattern': r'\b\d{5}(-\d{4})?\b',
        'severity': 'low',
        'gdpr_article': 'Art. 4(1)',
        'description': 'US postal code'
    },
}

# Exclude patterns (to reduce false positives)
EXCLUDE_PATTERNS = [
    r'example\.com',
    r'test@',
    r'user@',
    r'localhost',
    r'127\.0\.0\.1',
    r'0\.0\.0\.0',
    r'255\.255\.255',
    r'192\.168\.',
    r'10\.0\.',
]

# File extensions to scan
SCAN_EXTENSIONS = {
    '.js', '.ts', '.jsx', '.tsx',
    '.py', '.rb', '.php',
    '.java', '.go', '.rs',
    '.sql', '.json', '.yaml', '.yml',
    '.env', '.config',
    '.md', '.txt', '.log'
}

# Directories to skip
SKIP_DIRS = {
    'node_modules', 'vendor', 'dist', 'build',
    '.git', '.svn', '.hg',
    'venv', 'env', '__pycache__',
    'target', 'bin', 'obj'
}


def is_false_positive(match_text: str, context: str) -> bool:
    """Check if match is likely a false positive."""
    # Check against exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, match_text, re.IGNORECASE):
            return True
    
    # Check if in comment
    if any(marker in context for marker in ['//', '#', '/*', '*/', '<!--', '-->']):
        # Still flag if it looks like real data in comments
        if '@example' in match_text or 'test' in match_text.lower():
            return True
    
    return False


def scan_file(filepath: Path) -> List[Dict]:
    """Scan a single file for PII patterns."""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Check each PII pattern
                for pii_type, pii_info in PII_PATTERNS.items():
                    pattern = pii_info['pattern']
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    
                    for match in matches:
                        matched_text = match.group(0)
                        
                        # Skip false positives
                        if is_false_positive(matched_text, line):
                            continue
                        
                        findings.append({
                            'file': str(filepath),
                            'line': line_num,
                            'type': pii_type,
                            'severity': pii_info['severity'],
                            'gdpr_article': pii_info['gdpr_article'],
                            'description': pii_info['description'],
                            'matched': matched_text,
                            'context': line.strip()[:100]  # First 100 chars
                        })
    
    except Exception as e:
        # Skip binary or unreadable files
        pass
    
    return findings


def scan_directory(directory: Path) -> List[Dict]:
    """Recursively scan directory for PII."""
    all_findings = []
    
    for filepath in directory.rglob('*'):
        # Skip directories
        if filepath.is_dir():
            continue
        
        # Skip excluded directories
        if any(skip_dir in filepath.parts for skip_dir in SKIP_DIRS):
            continue
        
        # Skip non-scanned extensions
        if filepath.suffix not in SCAN_EXTENSIONS and filepath.suffix:
            continue
        
        # Scan file
        findings = scan_file(filepath)
        all_findings.extend(findings)
    
    return all_findings


def categorize_findings(findings: List[Dict]) -> Dict:
    """Categorize findings by severity and type."""
    categorized = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }
    
    for finding in findings:
        severity = finding['severity']
        categorized[severity].append(finding)
    
    return categorized


def generate_report(findings: List[Dict], categorized: Dict, output_json: bool = False) -> str:
    """Generate human-readable or JSON report."""
    
    if output_json:
        return json.dumps({
            'total_findings': len(findings),
            'by_severity': {
                severity: len(items) for severity, items in categorized.items()
            },
            'findings': findings
        }, indent=2)
    
    # Human-readable report
    report = []
    report.append("=" * 60)
    report.append("PII Detection Report - GDPR Compliance Scan")
    report.append("=" * 60)
    report.append("")
    
    # Summary
    report.append("## Summary")
    report.append(f"Total PII instances found: {len(findings)}")
    report.append("")
    report.append("By Severity:")
    report.append(f"  🔴 Critical: {len(categorized['critical'])}")
    report.append(f"  🟠 High:     {len(categorized['high'])}")
    report.append(f"  🟡 Medium:   {len(categorized['medium'])}")
    report.append(f"  🟢 Low:      {len(categorized['low'])}")
    report.append("")
    
    # Detailed findings by severity
    for severity in ['critical', 'high', 'medium', 'low']:
        items = categorized[severity]
        if not items:
            continue
        
        emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
        report.append(f"## {emoji} {severity.upper()} Severity ({len(items)} findings)")
        report.append("")
        
        # Group by file for readability
        by_file = {}
        for item in items:
            filepath = item['file']
            if filepath not in by_file:
                by_file[filepath] = []
            by_file[filepath].append(item)
        
        for filepath, file_findings in sorted(by_file.items()):
            report.append(f"### {filepath}")
            for finding in file_findings:
                report.append(f"  Line {finding['line']}: {finding['description']}")
                report.append(f"    Type: {finding['type']}")
                report.append(f"    GDPR: {finding['gdpr_article']}")
                report.append(f"    Found: {finding['matched']}")
                report.append(f"    Context: {finding['context']}")
                report.append("")
        
    # Recommendations
    report.append("=" * 60)
    report.append("## Recommendations")
    report.append("=" * 60)
    report.append("")
    
    if categorized['critical']:
        report.append("🔴 CRITICAL: Immediately review critical findings")
        report.append("   - SSN, credit cards must be encrypted")
        report.append("   - Never log or expose in plain text")
        report.append("")
    
    if categorized['high']:
        report.append("🟠 HIGH: Review high-severity personal data")
        report.append("   - Emails, phones are personal data (GDPR Art. 4)")
        report.append("   - Ensure proper legal basis for processing")
        report.append("   - Implement data subject rights (access, erasure)")
        report.append("")
    
    if categorized['medium'] or categorized['low']:
        report.append("🟡 MEDIUM/LOW: Review context for these findings")
        report.append("   - IP addresses can be personal data")
        report.append("   - UUIDs may identify users")
        report.append("   - Ensure compliance with GDPR principles")
        report.append("")
    
    report.append("For detailed GDPR analysis, run:")
    report.append("  /comply:audit gdpr")
    report.append("")
    
    return "\n".join(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scan codebase for PII (Personally Identifiable Information)'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to scan (default: current directory)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    scan_dir = Path(args.directory)
    if not scan_dir.exists():
        print(f"Error: Directory '{scan_dir}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not scan_dir.is_dir():
        print(f"Error: '{scan_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    # Scan directory
    print(f"Scanning {scan_dir} for PII...", file=sys.stderr)
    findings = scan_directory(scan_dir)
    
    # Categorize
    categorized = categorize_findings(findings)
    
    # Generate report
    report = generate_report(findings, categorized, args.json)
    print(report)
    
    # Exit code: 0 if no critical/high findings, 1 otherwise
    if categorized['critical'] or categorized['high']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
