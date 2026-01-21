---
name: EU Compliance
description: This skill should be used when the user asks about "GDPR", "data protection", "privacy compliance", "CSRD", "sustainability reporting", "ESRS", "personal data", "data subject rights", "consent management", or wants to analyze code for EU regulatory compliance. Provides comprehensive methodology for GDPR and CSRD compliance analysis.
version: 0.1.0
---

# EU Compliance Analysis

Comprehensive methodology for analyzing software compliance with EU regulations: GDPR (data protection) and CSRD (sustainability reporting).

## Purpose

Analyze codebases to ensure compliance with European Union regulations and generate actionable remediation guidance for:
1. **GDPR** - Personal data protection and privacy
2. **CSRD** - Corporate sustainability reporting (digital operations)

## Regulatory Framework

### GDPR (General Data Protection Regulation)

**Regulation (EU) 2016/679**
- Applies to: Processing of personal data of EU residents
- Scope: Any organization processing EU personal data (regardless of location)
- Penalties: Up to €20M or 4% of global annual revenue
- Effective: May 25, 2018

**Key Principles (Art. 5):**
1. Lawfulness, fairness, transparency
2. Purpose limitation
3. Data minimization
4. Accuracy
5. Storage limitation
6. Integrity and confidentiality
7. Accountability

### CSRD (Corporate Sustainability Reporting Directive)

**Directive (EU) 2022/2464**
- Applies to: Large companies (50,000+ EU companies)
- Scope: Environmental, Social, Governance (ESG) reporting
- Timeline: Phased rollout 2024-2028
- Standard: ESRS (European Sustainability Reporting Standards)

**Relevant for Software:**
- ESRS E1: Climate Change (Scope 2 & 3 emissions from digital operations)
- Energy consumption reporting
- GHG emission targets (2030, 2050)
- Third-party assurance required

---

## GDPR Analysis Methodology

### 1. Personal Data Identification

**What is Personal Data? (Art. 4.1)**

Any information relating to an identified or identifiable natural person.

**Direct Identifiers:**
- Full name, email address
- Phone number, postal address
- National ID number (SSN, passport, driver's license)
- Account number, username
- IP address, MAC address
- Cookie identifiers

**Indirect Identifiers:**
- Location data (GPS coordinates)
- Device fingerprints, user agents
- Behavioral data (browsing history, purchase patterns)
- Demographic data (age, gender, income)
- Preferences, interests

**Special Categories (Art. 9) - Higher Protection:**
- Health data (medical records, genetic, biometric)
- Racial or ethnic origin
- Political opinions
- Religious or philosophical beliefs
- Trade union membership
- Sexual orientation

**Detection Patterns:**

```regex
# Email addresses
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# Phone numbers
\+?1?\d{9,15}

# Social Security Numbers (US)
\d{3}-\d{2}-\d{4}

# Credit card numbers
\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}

# IP addresses (IPv4)
\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b

# UUIDs (common for user IDs)
[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
```

**Common Locations:**
- Database models/schemas (`users`, `customers`, `profiles`)
- API request/response payloads
- Application logs
- Frontend localStorage/cookies
- Analytics events
- Email templates
- Error messages

---

### 2. Legal Basis for Processing (Art. 6)

**Six Lawful Bases:**

**a) Consent** - Freely given, specific, informed, unambiguous
```typescript
// Valid consent example
{
  user_id: "123",
  marketing_consent: true,
  analytics_consent: false,
  consented_at: "2026-01-20T10:30:00Z",
  consent_version: "2.1",
  ip_address: "192.168.1.1",
  consent_method: "signup_form"
}
```

**b) Contract** - Necessary to fulfill contractual obligation
```typescript
// Example: Shipping address needed for order delivery
{
  shipping_address: "...",  // ✅ Necessary for contract
  browsing_history: "..."    // ❌ Not necessary
}
```

**c) Legal Obligation** - Required by law (e.g., tax records)

**d) Vital Interests** - Protect life (emergency medical)

**e) Public Task** - Official authority function

**f) Legitimate Interest** - Balancing test required
```typescript
// Example: Fraud prevention
{
  legal_basis: "legitimate_interest",
  purpose: "fraud_prevention",
  balancing_test_doc: "link/to/LIA.pdf"
}
```

**Check for:**
- Is legal basis documented?
- Is it appropriate for the purpose?
- For consent: Is it properly obtained and tracked?
- For legitimate interest: Is balancing test documented?

---

### 3. Data Subject Rights (Art. 15-22)

**Must implement:**

#### Right to Access (Art. 15)
User can request copy of all their data.

```http
GET /api/user/:id/data
Authorization: Bearer {user_token}

Response:
{
  "personal_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-15"
  },
  "processing_purposes": ["service_delivery", "marketing"],
  "retention_period": "2 years after account deletion",
  "recipients": ["Stripe", "SendGrid"],
  "source": "direct_signup",
  "automated_decisions": false
}
```

#### Right to Erasure (Art. 17)
"Right to be Forgotten"

```http
DELETE /api/user/:id
Authorization: Bearer {user_token}

Implementation checklist:
- [ ] Delete user record
- [ ] Delete all related records (posts, comments, etc.)
- [ ] Anonymize analytics data
- [ ] Remove from backups (or pseudonymize)
- [ ] Notify third-party processors
- [ ] Confirm deletion to user
```

**Exceptions to erasure:**
- Legal obligation to retain
- Freedom of expression
- Public interest
- Legal claims

#### Right to Data Portability (Art. 20)
Machine-readable export

```http
GET /api/user/:id/export
Authorization: Bearer {user_token}

Response: JSON/CSV file
{
  "format": "JSON",
  "user_data": { ... },
  "posts": [ ... ],
  "comments": [ ... ]
}
```

#### Right to Rectification (Art. 16)
User can update incorrect data

```http
PUT /api/user/:id/profile
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

#### Right to Restriction (Art. 18)
Limit processing while dispute is resolved

```typescript
user.processing_restricted = true;
user.restriction_reason = "accuracy_contested";
user.restricted_at = new Date();
```

#### Right to Object (Art. 21)
Object to processing (e.g., direct marketing)

```typescript
user.marketing_objection = true;
user.objection_date = new Date();
// Must stop marketing immediately
```

**Detection:**
- Search for routes: `/user/data`, `/user/export`, `/user/delete`
- Check for CRUD operations on user data
- Verify machine-readable export format
- Confirm cascading deletes

---

### 4. Security Measures (Art. 32)

**Technical and organizational measures:**

#### Encryption

**At Rest:**
```sql
-- Database column encryption
CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  ssn VARCHAR(255) ENCRYPTED  -- Encrypted column
);
```

```typescript
// Application-level encryption
import crypto from 'crypto';

function encryptPII(data: string): string {
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  return cipher.update(data, 'utf8', 'hex');
}
```

**In Transit:**
```nginx
# Force HTTPS
server {
  listen 80;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
}
```

#### Access Controls

```typescript
// Role-Based Access Control (RBAC)
function requireRole(role: string) {
  return (req, res, next) => {
    if (req.user.role !== role) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

app.get('/admin/users', requireRole('admin'), getUsers);
```

#### Audit Logging

```typescript
// Log all access to personal data
auditLog.create({
  action: 'data_access',
  user_id: targetUserId,
  accessed_by: currentUserId,
  data_type: 'personal_profile',
  timestamp: new Date(),
  ip_address: req.ip
});
```

**Must log:**
- Who accessed what data
- When (timestamp)
- From where (IP address)
- What action (read, update, delete)
- Result (success/failure)

#### Pseudonymization

```typescript
// Replace identifiers with pseudonyms
function pseudonymize(userId: string): string {
  return crypto.createHash('sha256')
    .update(userId + SALT)
    .digest('hex');
}

// Use in analytics
analytics.track({
  user_id: pseudonymize(realUserId),  // ✅ Pseudonym
  event: 'purchase',
  amount: 99.99
});
```

---

### 5. Data Retention & Deletion (Art. 5.1.e)

**Storage Limitation Principle:**

```typescript
// Define retention policies
const RETENTION_POLICIES = {
  user_accounts: {
    active: 'indefinite',
    inactive: '2 years',
    deleted: '30 days'  // Grace period
  },
  logs: {
    application: '90 days',
    security: '1 year',
    audit: '7 years'  // Legal requirement
  },
  analytics: {
    identified: '14 months',
    anonymized: 'indefinite'
  }
};

// Scheduled cleanup job
cron.schedule('0 0 * * *', async () => {
  // Delete accounts inactive for 2+ years
  const cutoff = new Date();
  cutoff.setFullYear(cutoff.getFullYear() - 2);
  
  await db.users.deleteMany({
    last_login: { $lt: cutoff },
    deletion_requested: true
  });
  
  // Anonymize old analytics
  await db.analytics.updateMany({
    created_at: { $lt: cutoff }
  }, {
    $unset: { user_id: 1, email: 1, ip_address: 1 }
  });
});
```

**Check for:**
- Documented retention periods
- Automated deletion/archival jobs
- TTL settings on caches
- Backup rotation policies

---

### 6. Cross-Border Transfers (Art. 44-50)

**Transfers outside EU/EEA:**

**Adequacy Decisions** (no additional safeguards needed):
- Andorra, Argentina, Canada (commercial), Faroe Islands
- Guernsey, Israel, Isle of Man, Japan, Jersey
- New Zealand, South Korea, Switzerland, UK, Uruguay

**Standard Contractual Clauses (SCC)** for others:
```typescript
// Example: US-based service
const stripeConfig = {
  api_key: process.env.STRIPE_KEY,
  region: 'us',
  scc_reference: 'docs/stripe-scc-2021.pdf',  // ✅ SCC in place
  data_transferred: ['email', 'name', 'payment_info']
};
```

**Detection:**
- Search for third-party API calls
- Check cloud provider regions in configs
- Identify CDN locations
- Flag transfers without safeguards

**Common services:**
```typescript
// Check for these patterns
const THIRD_PARTY_SERVICES = {
  'stripe.com': { location: 'US', scc_available: true },
  'sendgrid.com': { location: 'US', scc_available: true },
  's3.amazonaws.com': { check: 'region' },
  'firestore.googleapis.com': { check: 'region' }
};
```

---

### 7. Breach Notification (Art. 33-34)

**Requirements:**
- Notify supervisory authority within **72 hours**
- Notify affected users if **high risk** to rights and freedoms

```typescript
// Breach detection and notification
class BreachResponse {
  async detectBreach(incident: SecurityIncident) {
    if (this.isPersonalDataBreach(incident)) {
      await this.assess(incident);
      
      if (incident.severity >= 'medium') {
        await this.notifySupervisoryAuthority(incident);  // 72h
      }
      
      if (incident.severity === 'high') {
        await this.notifyAffectedUsers(incident);
      }
      
      await this.documentBreach(incident);  // Art. 33.5
    }
  }
}
```

**Check for:**
- Incident response procedures
- Security monitoring/alerting
- Breach notification templates
- Breach register (Art. 33.5)

---

### 8. Privacy by Design & Default (Art. 25)

**Principles:**

```typescript
// ❌ BAD - Not privacy by design
class User {
  email: string;
  name: string;
  marketing_consent = true;  // Opt-out (not default)
  analytics_tracking = true;
}

// ✅ GOOD - Privacy by design
class User {
  email: string;
  name: string;
  
  // Privacy by default - opt-in for non-essential
  marketing_consent = false;
  analytics_tracking = false;
  
  // Data minimization
  created_at: Date;  // Only necessary fields
  
  // Pseudonymization
  get pseudonym_id() {
    return hash(this.id + SALT);
  }
}
```

**Check for:**
- Opt-in by default (not opt-out)
- Minimal data collection
- Pseudonymization where possible
- Encryption by default

---

## CSRD Analysis Methodology

### Integration with ecoscore Plugin

**CSRD digital sustainability relies on ecoscore for metrics:**

```markdown
## Step 1: Get Environmental Metrics from ecoscore

Use the ecoscore plugin to calculate:
- Carbon footprint (kg CO2e/year)
- Energy consumption (kWh/year)
- Infrastructure carbon intensity
- Code efficiency scores
- Optimization opportunities

Command: `/ecoscore:analyze` or `/ecoscore:metrics`
```

### ESRS E1 - Climate Change (Digital Operations)

**Five Disclosure Requirements:**

#### E1-1: Transition Plan
- Targets for 2030 and 2050
- Decarbonization strategy for digital operations
- Investment plan

**Check for:**
- Documented reduction targets in code/docs
- Migration plans to low-carbon regions
- Code optimization roadmaps

#### E1-2: Policies
- Climate change mitigation policies
- Responsibility assignment

**Check for:**
- Sustainability governance documentation
- Energy efficiency policies
- Green hosting policies

#### E1-3: Actions
- Mitigation measures taken
- Progress tracking

**Check for:**
- Code optimization efforts
- Infrastructure efficiency improvements
- Renewable energy usage

#### E1-4: Metrics (Most Important)
- **GHG emissions** (Scope 1, 2, 3)
- **Energy consumption** (kWh)
- **Energy mix** (renewable %)
- **Carbon intensity**

**Digital Operations Scope:**

**Scope 2 (Indirect - Energy):**
- Cloud infrastructure (AWS, GCP, Azure)
- Data center electricity
- Office energy (if tracked)

**Scope 3 (Value Chain):**
- End-user device energy
- Data transmission networks
- Upstream: Software dependencies, dev tools
- Downstream: Customer usage of software

**Metrics to Calculate:**
```typescript
interface CSRD_Metrics {
  // Energy
  total_energy_kwh: number;
  renewable_energy_percent: number;
  
  // Emissions
  scope_2_emissions_kg_co2e: number;
  scope_3_emissions_kg_co2e: number;
  total_emissions_kg_co2e: number;
  
  // Intensity
  emissions_per_user_kg: number;
  emissions_per_transaction_g: number;
  
  // Regional breakdown
  emissions_by_region: {
    region: string;
    kwh: number;
    carbon_intensity_g_per_kwh: number;
    emissions_kg_co2e: number;
  }[];
}
```

#### E1-5: Targets
- Science-based targets (SBT)
- Interim milestones (2030)
- Net-zero commitment (2050)

**Check for:**
- Documented emission reduction targets
- Progress tracking mechanism
- Alignment with Paris Agreement (1.5°C pathway)

---

### CSRD Compliance Scoring (0-100)

**Breakdown:**

1. **Energy Tracking (25 points)**
   - Full monitoring: 25
   - Partial tracking: 15
   - No tracking: 0

2. **Emission Calculation (25 points)**
   - Scope 2 + 3 calculated: 25
   - Scope 2 only: 15
   - No calculation: 0

3. **Targets Set (25 points)**
   - Science-based targets (SBT): 25
   - Internal targets: 15
   - No targets: 0

4. **Governance & Documentation (25 points)**
   - Full ESRS E1 documentation: 25
   - Partial documentation: 15
   - Missing: 0

**Rating:**
- 90-100: ✅ Compliant (ready for assurance)
- 70-89: ⚠️ Mostly Compliant (minor gaps)
- 50-69: ⚠️ At Risk (significant work needed)
- 30-49: ❌ Non-Compliant (urgent action)
- 0-29: ❌ Critical (no reporting capability)

---

## Detection Patterns Summary

### Common Anti-Patterns

| Category | Anti-Pattern | Detection | Fix |
|----------|--------------|-----------|-----|
| **GDPR - Logging** | PII in logs | `logger.*user.email` | Log user ID only |
| **GDPR - Storage** | Plaintext passwords | `password: string` | Use bcrypt/argon2 |
| **GDPR - API** | No HTTPS | `http://` endpoints | Force HTTPS |
| **GDPR - Rights** | No deletion | Missing `/user/delete` | Implement erasure |
| **GDPR - Consent** | Pre-checked boxes | `<input checked>` | Require opt-in |
| **GDPR - Transfer** | US region | `us-east-1` | Use EU region or SCC |
| **CSRD - Region** | High-carbon region | `us-east-1` (379g) | Migrate to `eu-north-1` (8g) |
| **CSRD - Deps** | Heavy packages | moment.js (300KB) | Use date-fns (13KB) |
| **CSRD - Tracking** | No monitoring | Missing metrics | Implement energy tracking |
| **CSRD - Targets** | No goals | Missing targets | Set 2030/2050 targets |

---

## References

**GDPR Resources:**
- Full text: https://gdpr-info.eu/
- ICO Guide: https://ico.org.uk/for-organisations/guide-to-data-protection/
- EDPB Guidelines: https://edpb.europa.eu/

**CSRD Resources:**
- Directive text: https://eur-lex.europa.eu/eli/dir/2022/2464
- ESRS Standards: https://www.efrag.org/lab6
- CSRD implementation timeline: 2024-2028 (phased)

**Integration:**
- See `references/gdpr-comprehensive.md` for detailed GDPR patterns
- See `references/csrd-integration.md` for ecoscore integration guide
- See `scripts/detect-pii.py` for automated PII detection

---

## Usage in Commands

This skill provides the knowledge base for:

- `/comply:scan` - Quick compliance scan
- `/comply:audit [gdpr|csrd|all]` - Deep audit
- `/comply:report [framework]` - Documentation generation

Agents using this skill:
- `gdpr-analyzer` - GDPR compliance analysis
- `csrd-analyzer` - CSRD sustainability reporting
- `compliance-advisor` - Q&A and guidance
