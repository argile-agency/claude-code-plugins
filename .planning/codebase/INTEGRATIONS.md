# External Integrations

**Analysis Date:** 2026-02-03

## APIs & External Services

**No External APIs Currently Used:**
- Plugins execute entirely within Claude Code environment
- No third-party API calls in core plugin functionality
- Plugins designed to analyze codebases, not integrate with external services

**Potential Third-Party Services (Analyzed, Not Integrated):**
- Stripe - Referenced in GDPR analyzer examples for cross-border transfer documentation
- SendGrid - Referenced in GDPR analyzer examples for email service compliance
- AWS - Referenced in carbon estimation scripts for region-based carbon intensity calculation
- GCP - Referenced in carbon estimation scripts for region-based carbon intensity calculation
- Azure - Referenced in carbon estimation scripts for region-based carbon intensity calculation

## Data Storage

**Databases:**
- None - Plugins are stateless analysis tools
- No persistent data storage required
- All analysis is performed on scanned codebase files

**File Storage:**
- Local filesystem only
- Plugins read codebase files using `Read`, `Glob`, `Bash` tools
- No uploads to external storage

**Caching:**
- None implemented
- Analysis performed on-demand per command/agent execution

## Authentication & Identity

**Auth Provider:**
- Claude Code platform handles authentication
- No separate auth provider needed
- Plugins inherit user context from Claude Code

## Monitoring & Observability

**Error Tracking:**
- None configured
- Errors handled within plugin prompts (graceful fallback)

**Logs:**
- No external logging
- Execution logs within Claude Code platform
- Utility scripts (`estimate-carbon.py`, `detect-pii.py`) can write JSON output to stdout

## CI/CD & Deployment

**Hosting:**
- GitHub-based distribution
- Installable via: `claude /plugin https://github.com/argile-agency/claude-code-plugins [plugin-name]`
- No deployment infrastructure required

**CI Pipeline:**
- None detected
- Repository is maintained via Git with standard commits
- No automated testing/deployment configured

## Environment Configuration

**Required Environment Variables:**
- None for core functionality
- Python utility scripts accept CLI arguments instead (e.g., `--region us-east-1`, `--tokens 1000000`)

**Secrets Location:**
- Not applicable - No external API keys or secrets needed
- Plugins analyze security in target codebases, they don't require security config

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

## Script-Based Integrations

**Python Utility Scripts:**

### `plugins/ecoscore/skills/green-it-analysis/scripts/estimate-carbon.py`
- **Purpose:** Calculate carbon footprint from software metrics
- **Usage:** CLI-based standalone tool
- **Inputs:** `--tokens`, `--model`, `--server-hours`, `--server-size`, `--region`, `--build-minutes`, `--recommend-region`
- **Outputs:** JSON or human-readable text to stdout
- **External Data:** Hardcoded carbon intensity tables for AWS, GCP, Azure regions
- **No External Dependencies:** Uses Python standard library only

### `plugins/comply/skills/eu-compliance/scripts/detect-pii.py`
- **Purpose:** Scan codebase for Personally Identifiable Information
- **Usage:** CLI-based standalone tool
- **Inputs:** Directory path, `--json` flag for output format
- **Outputs:** JSON or human-readable report to stdout
- **Pattern Matching:** Regex-based detection for emails, SSN, credit cards, IP addresses, phone numbers, UUIDs, postal codes
- **Excluded Directories:** node_modules, vendor, dist, build, .git, venv, env, target, bin, obj
- **Scanned Extensions:** .js, .ts, .jsx, .tsx, .py, .rb, .php, .java, .go, .rs, .sql, .json, .yaml, .yml, .env, .config, .md, .txt, .log
- **No External Dependencies:** Uses Python standard library only

## Knowledge Base References

**ecoscore Skill References** (in `plugins/ecoscore/skills/green-it-analysis/references/`)
- `ai-carbon-estimation.md` - Methodology for calculating carbon from AI/LLM usage
- `carbon-regions.md` - Cloud region carbon intensity data (AWS, GCP, Azure)
- `dependency-alternatives.md` - Lightweight package alternatives (e.g., moment.js vs date-fns)
- `frontend-patterns.md` - Frontend optimization patterns for energy efficiency

**comply Skill References** (in `plugins/comply/skills/eu-compliance/`)
- `eu-compliance/SKILL.md` - GDPR and CSRD methodology and patterns
- Potentially: `references/gdpr-comprehensive.md`, `references/csrd-integration.md` (referenced in skill but not present)

## Integration Patterns Used by Plugins

**Compliance Hooks** (`PreToolUse` in `hooks.json`):
- **ecoscore plugin** - Warns on Write/Edit operations if environmental anti-patterns detected
  - Checks for: heavy dependencies, AI inefficiency, database issues, resource waste
  - Response: JSON with `permissionDecision: "allow"` (warn-only, never blocks) and systemMessage warning

- **comply plugin** - Warns on Write/Edit operations if compliance issues detected
  - Checks for: GDPR violations (PII in logs, hardcoded secrets, unencrypted data, missing consent, cross-border transfers)
  - Checks for: sustainability issues (heavy dependencies, inefficient patterns, high-carbon infrastructure)
  - Response: JSON with `permissionDecision: "allow"` (warn-only, never blocks) and systemMessage warning

**Tool Access Pattern:**
- Agents specify allowed tools in YAML frontmatter: `tools: ["Read", "Glob", "Grep", "Bash"]`
- `ecoscore-analyzer` and `gdpr-analyzer` agents use all four tools
- Commands inherit tool restrictions from their parent plugin configuration

## Data Flow Model

**Analysis Pattern:**
1. User triggers command (e.g., `/ecoscore:analyze`)
2. Command/Agent runs within Claude Code
3. Tools (Read, Glob, Grep, Bash) access local codebase files
4. Analysis performed entirely within Claude Code environment
5. Python utility scripts can be executed via `Bash` tool if needed
6. Results returned to user (no external storage)

**No External Data Sources:**
- All data comes from local codebase being analyzed
- Reference data (carbon intensity, package alternatives) hardcoded in skills and scripts
- No API calls required for core functionality

---

*Integration audit: 2026-02-03*
