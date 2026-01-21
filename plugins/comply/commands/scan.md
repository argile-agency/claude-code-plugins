---
description: Quick GDPR and sustainability compliance scan
allowed-tools: Read, Glob, Grep, Bash(command:*)
argument-hint: [scope]
---

# Comply Scan (Free Tier)

Quick compliance check for GDPR violations and sustainability metrics.

## Usage Limits (Free Tier)

- **40 scans per month** per repository
- Basic issue detection only
- No line-by-line remediation guidance
- Upgrade to Premium for unlimited scans and detailed fixes

## Optional Scope Filter

Run targeted scans:
- `$ARGUMENTS = gdpr` - GDPR compliance only
- `$ARGUMENTS = csrd` - Sustainability metrics only  
- `$ARGUMENTS = all` or empty - Full compliance scan (default)

## Scan Process

### Phase 1: Project Discovery (2-3 min)

Identify project type and gather context:

1. **Find package managers**: package.json, requirements.txt, composer.json, Cargo.toml
2. **Identify frameworks**: React, Svelte, Laravel, Django, Adonis, Tauri
3. **Check infrastructure**: Cloud configs, environment variables
4. **Detect database**: Models, migrations, ORM patterns

### Phase 2: GDPR Quick Check (5-7 min)

If scope includes GDPR:

**1. Secrets Scanning**
- Search for hardcoded credentials: `password`, `api_key`, `secret`, `token`
- Check for AWS keys, private keys, database credentials
- Pattern: `(password|api[_-]?key|secret|token)\s*[:=]\s*['"]\w+['"]`

**2. PII Detection**
- Search for personal data in logs: `logger`, `console.log`, `print`, `echo`
- Check for emails, names, IDs in logging statements
- Patterns: emails, phone numbers, SSN, credit cards

**3. Data Subject Rights Check**
- Search for endpoints: `user/export`, `user/delete`, `user/data`
- Check for CRUD operations on user data
- Look for data portability implementations

**4. Consent Management**
- Search user models for: `consent`, `agreed_at`, `legal_basis`
- Check signup/registration flows for consent tracking
- Look for consent version tracking

**5. Cross-Border Transfers**
- Detect API calls to non-EU services: `api.stripe.com`, `aws`, `gcp`
- Check cloud regions in configs: `us-east-1`, `ap-south-1`
- Look for Standard Contractual Clauses references

### Phase 3: CSRD Basic Check (3-5 min)

If scope includes CSRD:

**1. Infrastructure Detection**
- Find cloud provider configs (AWS, GCP, Azure)
- Detect regions and calculate carbon intensity
- Estimate infrastructure emissions

**2. Code Efficiency Highlights**
- Count heavy dependencies (moment.js, lodash full)
- Check for large bundle sizes
- Identify algorithmic inefficiencies (nested loops)

**3. CSRD Gap Analysis**
- Check for energy consumption tracking
- Look for emission reduction targets
- Verify sustainability governance documentation

**Note:** For full CSRD ESRS E1 report, use `/comply:audit csrd` (Premium)

### Phase 4: Scoring & Report Generation

**Scoring System (0-100):**

**GDPR Score:**
- Start at 100
- Deduct for each issue found:
  - Critical (secrets, unencrypted PII): -15 each
  - Major (missing rights, no consent): -10 each
  - Minor (suboptimal patterns): -5 each

**CSRD Score:**
- Energy tracking: 25 points
- Emission calculation: 25 points
- Reduction targets: 25 points
- Governance: 25 points

**Overall Score:** Weighted average (GDPR 60%, CSRD 40%)

### Output Format

Generate summary report:

```markdown
## Comply Scan Results

**Scan Date:** [timestamp]
**Repository:** [repo-name]
**Scope:** [gdpr|csrd|all]

---

### Overall Compliance

**GDPR Score:** X/100 [Rating]
**CSRD Score:** X/100 [Rating]
**Overall:** X/100 [Rating]

**Rating Scale:**
- 90-100: ✅ Compliant
- 70-89: ⚠️ Mostly Compliant
- 50-69: ⚠️ At Risk
- 30-49: ❌ High Risk
- 0-29: ❌ Critical

---

### Issues Summary

**Critical Issues:** X
- [Issue type]: X occurrences
- [Issue type]: X occurrences

**Major Issues:** X
- [Issue type]: X occurrences

**Minor Issues:** X

---

### GDPR Highlights

**Personal Data Found:**
- Email addresses in logs: X files
- Potential PII exposure: X locations

**Missing Implementations:**
- ❌ Right to erasure endpoint
- ⚠️ Consent tracking incomplete
- ✅ Data encryption configured

**Secrets Detected:**
- 🔴 Hardcoded API keys: X
- 🔴 Database credentials: X

---

### CSRD Highlights

**Digital Carbon Footprint Estimate:**
- Annual emissions: ~X kg CO2e/year
- Primary sources: Infrastructure (X%), Data transfer (X%)

**Compliance Gaps:**
- ❌ Energy consumption not tracked (required by 2025)
- ❌ No emission reduction targets set
- ⚠️ Infrastructure in high-carbon region

**Quick Wins:**
- Migrate to eu-north-1: -X% emissions
- Remove heavy dependencies: -X KB bundle size

---

### Next Steps

**Immediate Actions:**
1. Remove hardcoded secrets (CRITICAL)
2. Stop logging PII (CRITICAL)
3. Review cross-border data transfers

**This Week:**
1. Implement data deletion endpoint (GDPR Art. 17)
2. Add consent tracking to user model
3. Plan cloud region migration for lower emissions

**This Month:**
1. Set up energy consumption monitoring
2. Define emission reduction targets
3. Create data processing register

---

### Upgrade to Premium

Get detailed remediation guidance:
- ✅ **Unlimited scans** (no 40/month limit)
- ✅ **Line-by-line fixes** with code examples
- ✅ **Full CSRD ESRS E1 reports** for regulatory compliance
- ✅ **Audit documentation** generation
- ✅ **Priority support** from Argile

**Pricing:** €199/month or €1,990/year (save 17%)

[Contact Argile](mailto:aloha@argile.agency?subject=Comply%20Premium%20Upgrade)

---

**Scans remaining this month:** X/40

*Run `/comply:audit [gdpr|csrd|all]` for deep analysis (Premium)*
*Run `/comply:report [framework]` for audit documentation (Premium)*
```

---

## Usage Tracking

Check scan usage before proceeding:

1. Look for `.claude/comply-usage.json` in repository root
2. If not found, create with initial state
3. Check current month and scan count
4. If >= 40 scans this month, show upgrade message and exit
5. Increment scan counter
6. Proceed with scan

**Usage file format:**
```json
{
  "current_month": "2026-01",
  "scans_used": 23,
  "limit": 40,
  "tier": "free"
}
```

---

## Implementation Notes

**Tools Usage:**
- **Glob**: Find configuration files, user models, logging files
- **Grep**: Search for PII patterns, secrets, consent keywords
- **Read**: Examine flagged files for context
- **Bash**: Run scripts for PII detection, secret scanning

**Skills Reference:**
- Use `eu-compliance` skill for GDPR patterns and detection rules
- Reference GDPR articles in findings
- Provide actionable remediation steps

**Performance:**
- Complete scan in 10-15 minutes for typical projects
- Prioritize high-signal patterns (avoid false positives)
- Focus on critical issues in free tier

**Freemium Strategy:**
- Show enough value to demonstrate capability
- Create urgency with issue counts
- Clear upgrade path to premium features
