# Comply - EU Compliance Automation

GDPR and CSRD compliance automation for European SaaS companies. Scan your codebase for data protection violations and generate sustainability reports.

## Features

### GDPR Compliance
- **Personal data detection** - Find PII in logs, code, databases
- **Data subject rights** - Verify implementation of access, erasure, portability
- **Consent management** - Check for proper consent tracking
- **Security measures** - Encryption, access controls, audit logging
- **Cross-border transfers** - Detect non-EU data flows
- **Breach notification** - Verify incident response procedures

### CSRD Sustainability Reporting
- **Digital carbon footprint** - Calculate emissions from code and infrastructure
- **ESRS E1 compliance** - Full climate change disclosure
- **Energy tracking** - Monitor kWh consumption
- **Reduction targets** - Set and track 2030/2050 goals
- **Integration with ecoscore** - Leverage existing environmental metrics

### Compliance Features
- **Pre-commit warnings** - Catch violations before they're committed
- **Line-by-line remediation** - Specific fixes with code examples
- **Audit documentation** - Generate regulator-ready reports
- **Multi-framework support** - GDPR, CSRD, LPD (coming soon), SOC2 (roadmap)

## Installation

```bash
# Install comply plugin
claude /plugin https://github.com/argile-agency/claude-code-plugins comply

# Or install from local path
claude /plugin /path/to/claude-code-plugins comply
```

## Commands

### `/comply:scan [scope]`

Quick compliance scan (FREE tier - 40 scans/month)

```bash
# Full compliance scan (GDPR + CSRD)
/comply:scan

# GDPR only
/comply:scan gdpr

# Sustainability only
/comply:scan csrd
```

**Output:**
- Compliance scores (0-100)
- Issue summary by severity
- GDPR violation highlights
- CSRD gap analysis
- Next steps and recommendations

**Free tier limits:**
- 40 scans per month
- Basic issue detection
- No line-by-line fixes

### `/comply:audit [framework]` (Premium)

Deep compliance audit with detailed remediation

```bash
# GDPR deep audit
/comply:audit gdpr

# Full CSRD ESRS E1 report
/comply:audit csrd

# Digital sustainability only
/comply:audit csrd-digital

# Complete compliance audit
/comply:audit all
```

**Premium features:**
- Unlimited audits
- File:line issue locations
- Code examples (bad → good)
- Risk assessment and prioritization
- Full ESRS E1 reporting

### `/comply:report [framework]` (Premium)

Generate audit-ready compliance documentation

```bash
# GDPR data protection report
/comply:report gdpr

# CSRD sustainability statement
/comply:report csrd
```

**Output formats:**
- Markdown (human-readable)
- PDF (regulator submission)
- JSON (machine-readable, XBRL export)

## Agents

### `gdpr-analyzer`

Triggered when you ask about GDPR compliance:
- "Is this GDPR compliant?"
- "Check for privacy violations"
- "Analyze data protection"

Performs deep GDPR analysis across all 99 articles.

### `csrd-analyzer`

Triggered when you ask about sustainability reporting:
- "Check CSRD compliance"
- "Generate ESRS E1 report"
- "Calculate carbon footprint"

Integrates with ecoscore plugin for environmental metrics.

### `compliance-advisor`

Educational agent for compliance questions:
- "What is GDPR consent?"
- "How do I implement data deletion?"
- "Explain CSRD requirements"

Provides implementation guidance with code examples.

## Hooks

**Pre-commit warnings:**
- Detects PII in logs before commit
- Flags hardcoded secrets
- Warns about compliance violations
- Suggests quick fixes

**Never blocks commits** - warnings only.

## Example Output

```markdown
## Comply Scan Results

**GDPR Score:** 68/100 ⚠️ (At Risk)
**CSRD Score:** 55/100 ⚠️ (Gaps Found)
**Overall:** 62/100 ⚠️

### Issues Found
- 🔴 Critical: 3 (PII in logs, no data deletion endpoint)
- 🟡 Major: 8 (consent tracking, retention policy)
- 🟢 Minor: 12

### CSRD Highlights
- Annual emissions: ~1,240 kg CO2e
- Energy consumption: Not tracked (required by 2025)
- Reduction targets: Not set

### Next Steps
1. Remove PII from logs (CRITICAL)
2. Implement /user/delete endpoint (GDPR Art. 17)
3. Set emission reduction targets (CSRD)

**Scans remaining: 37/40**
```

## Pricing

| Feature | Free | Premium | Enterprise |
|---------|------|---------|------------|
| Compliance scans | 40/month | Unlimited | Unlimited |
| GDPR basic check | ✅ | ✅ | ✅ |
| CSRD highlights | ✅ | ✅ | ✅ |
| Deep audits | ❌ | ✅ | ✅ |
| Line-by-line fixes | ❌ | ✅ | ✅ |
| Full ESRS E1 reports | ❌ | ✅ | ✅ |
| Audit documentation | ❌ | ✅ | ✅ |
| Support | Community | Priority | Dedicated |
| **Price** | **Free** | **€199/mo** | **Custom** |

[Upgrade to Premium](mailto:aloha@argile.agency?subject=Comply%20Premium%20Upgrade)

## Supported Frameworks

### Current
- ✅ **GDPR** - EU General Data Protection Regulation
- ✅ **CSRD** - Corporate Sustainability Reporting Directive (ESRS E1)

### Coming Soon
- 🚧 **LPD** - Swiss Federal Act on Data Protection (Q2 2026)
- 🚧 **SOC2** - Trust Service Criteria (Q3 2026)

## Tech Stack Coverage

Comply analyzes code across all major stacks:
- **Frontend**: React, Svelte
- **Backend**: Node.js, Adonis.js, Laravel, Django
- **Desktop**: Tauri (Rust)
- **Databases**: PostgreSQL, MySQL, MongoDB patterns
- **Cloud**: AWS, GCP, Azure configurations

## How It Works

### GDPR Analysis

1. **Personal Data Inventory**
   - Scans database models for PII fields
   - Checks API payloads for personal data
   - Detects logging of emails, names, IDs

2. **Legal Basis Verification**
   - Checks for consent tracking
   - Verifies contractual necessity
   - Validates legitimate interest documentation

3. **Data Subject Rights**
   - Searches for `/user/export`, `/user/delete` endpoints
   - Verifies data portability formats
   - Checks rectification capabilities

4. **Security Measures**
   - Validates encryption (at rest, in transit)
   - Checks access controls (RBAC)
   - Verifies audit logging

5. **Compliance Scoring**
   - Deducts points for violations
   - Categorizes by severity
   - Provides remediation timeline

### CSRD Analysis

1. **Calls ecoscore Plugin**
   - Gets carbon footprint metrics
   - Retrieves energy consumption data
   - Obtains code efficiency scores

2. **Maps to ESRS E1**
   - Converts metrics to ESRS format
   - Calculates Scope 2/3 emissions
   - Identifies reporting gaps

3. **Generates Reports**
   - Digital-only or full ESRS E1
   - Includes reduction targets
   - Formats for third-party assurance

## Scripts

### `detect-pii.py`

Automated PII detection:

```bash
# Scan current directory
python plugins/comply/skills/eu-compliance/scripts/detect-pii.py

# Scan specific directory
python plugins/comply/skills/eu-compliance/scripts/detect-pii.py /path/to/code

# JSON output
python plugins/comply/skills/eu-compliance/scripts/detect-pii.py --json
```

**Detects:**
- Emails, phone numbers
- SSN, credit cards
- IP addresses, UUIDs
- Postal codes

## GDPR Articles Covered

- **Art. 4**: Personal data definitions
- **Art. 5**: Processing principles (minimization, limitation)
- **Art. 6**: Lawful basis for processing
- **Art. 7**: Conditions for consent
- **Art. 15**: Right to access
- **Art. 16**: Right to rectification
- **Art. 17**: Right to erasure
- **Art. 18**: Right to restriction
- **Art. 20**: Right to data portability
- **Art. 21**: Right to object
- **Art. 25**: Privacy by design and default
- **Art. 32**: Security of processing
- **Art. 33-34**: Breach notification
- **Art. 44-50**: International transfers

## CSRD Standards Covered

- **ESRS E1**: Climate Change
  - E1-1: Transition plan
  - E1-2: Policies
  - E1-3: Actions
  - E1-4: Metrics (emissions, energy)
  - E1-5: Targets

## Integration with ecoscore

Comply uses the `ecoscore` plugin for CSRD metrics:

```
/comply:audit csrd
  → Calls /ecoscore:analyze
  → Gets carbon footprint, energy consumption
  → Maps to ESRS E1 requirements
  → Generates compliance report
```

**Why this matters:**
- Unified environmental analysis
- Consistent carbon calculations
- Single source of truth for sustainability

## Best Practices

### Before Committing
1. Run `/comply:scan` to catch violations
2. Fix critical issues (PII in logs, secrets)
3. Review pre-commit warnings

### Monthly
1. Run full `/comply:audit all` (Premium)
2. Track compliance score trends
3. Address new violations

### Annually
1. Generate `/comply:report gdpr` for DPO
2. Generate `/comply:report csrd` for sustainability statement
3. Update policies and documentation

### For Audits
1. Use Premium tier for audit-ready reports
2. Document all remediation steps
3. Re-scan to verify compliance

## FAQ

**Q: Is comply a replacement for legal counsel?**
A: No. Comply provides technical analysis and guidance, but you should consult legal experts for regulatory interpretation.

**Q: Does comply guarantee GDPR compliance?**
A: No. Comply helps identify issues and provides remediation guidance, but compliance is your responsibility.

**Q: How accurate is PII detection?**
A: ~95% accuracy with <5% false positives. Always review findings in context.

**Q: Can I use comply for non-EU companies?**
A: Yes! If you process EU personal data or have EU customers, GDPR applies regardless of location.

**Q: Does CSRD apply to my company?**
A: CSRD applies to large companies (250+ employees) and listed SMEs starting 2024-2028 (phased). Check official EU guidance.

**Q: How does ecoscore integration work?**
A: Comply calls ecoscore commands to get environmental metrics, then maps them to CSRD ESRS E1 requirements.

**Q: What's included in free tier?**
A: 40 scans/month with basic issue detection. No line-by-line fixes or audit reports.

**Q: How do I upgrade to Premium?**
A: Contact [aloha@argile.agency](mailto:aloha@argile.agency?subject=Comply%20Premium%20Upgrade)

## Roadmap

### Version 0.2 (Q2 2026)
- [ ] LPD (Swiss) compliance framework
- [ ] Custom rule builder
- [ ] Multi-repo support
- [ ] Compliance dashboard

### Version 0.3 (Q3 2026)
- [ ] SOC2 trust principles
- [ ] Automated remediation suggestions
- [ ] CI/CD integration
- [ ] Slack/Teams notifications

### Version 1.0 (Q4 2026)
- [ ] Full ESRS coverage (E1-E5, S1-S4, G1)
- [ ] Third-party audit trail
- [ ] Historical compliance tracking
- [ ] API for custom integrations

## Resources

**GDPR:**
- [Full GDPR text](https://gdpr-info.eu/)
- [ICO Guide](https://ico.org.uk/for-organisations/guide-to-data-protection/)
- [EDPB Guidelines](https://edpb.europa.eu/)

**CSRD:**
- [CSRD Directive](https://eur-lex.europa.eu/eli/dir/2022/2464)
- [ESRS Standards](https://www.efrag.org/lab6)
- [Implementation Timeline](https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en)

**Support:**
- Email: [aloha@argile.agency](mailto:aloha@argile.agency)
- Website: [https://argile.agency](https://argile.agency)
- GitHub: [Issues](https://github.com/argile-agency/claude-code-plugins/issues)

## License

MIT License - See [LICENSE](../../LICENSE) for details.

## About Argile

Argile Agency specializes in sustainable software development and compliance automation for European businesses.

**Our plugins:**
- **codeeco** - Code-level environmental impact analysis
- **ecoscore** - Organizational sustainability & CSRD reporting
- **comply** - GDPR & CSRD compliance automation

[Learn more about Argile](https://argile.agency)
