# Codebase Concerns

**Analysis Date:** 2026-02-03

## Tech Debt

**Incomplete Plugin Implementation - Missing Premium Features:**
- Issue: Both `comply` and `ecoscore` plugins describe premium-tier features (`/comply:audit`, `/comply:report`, `/ecoscore:analyze` detailed benchmarks) in their documentation but implementation details are not present in the repository. These commands/agents are referenced in hooks, command hints, and READMEs but no actual execution logic is included.
- Files:
  - `plugins/comply/commands/scan.md` (lines 199-217: premium upgrade path)
  - `plugins/comply/README.md` (lines 67-102: audit/report commands)
  - `plugins/ecoscore/commands/analyze.md` (lines 71-114: benchmark execution)
  - `plugins/ecoscore/README.md` (lines 26-36: full analysis features)
- Impact: Premium tier functionality is incomplete and undefined. Users following documentation to upgrade will encounter missing implementations. Revenue/feature model cannot be delivered without this work.
- Fix approach: Define concrete implementation specs for premium commands. Either implement full functionality or document which features are placeholders. Consider creating separate PREMIUM_ROADMAP.md file to track planned vs. implemented features.

**Incomplete csrd-analyzer Agent:**
- Issue: `comply` plugin README (line 120) mentions `csrd-analyzer` agent but no corresponding agent file exists in `plugins/comply/agents/`
- Files: `plugins/comply/README.md` (lines 120-127)
- Impact: Documentation references non-existent functionality. Users trying to trigger this agent via natural language will not get the advertised behavior.
- Fix approach: Either implement `csrd-analyzer.md` in `plugins/comply/agents/` or remove the reference from README.

**Missing compliance-advisor Agent:**
- Issue: `comply` plugin README (line 129) documents `compliance-advisor` agent with use case examples, but no agent file exists
- Files: `plugins/comply/README.md` (lines 129-136)
- Impact: Educational agent is advertised but not implemented. Users cannot access referenced feature.
- Fix approach: Implement `compliance-advisor.md` or remove from README documentation.

**Vague Usage Tracking Implementation:**
- Issue: `/comply:scan` command documents usage tracking (lines 222-241 in `plugins/comply/commands/scan.md`) with `.claude/comply-usage.json` file format but no implementation logic is shown. Command cannot enforce 40-scan limit without tracking mechanism.
- Files: `plugins/comply/commands/scan.md` (lines 222-241)
- Impact: Freemium model cannot be enforced. No usage limits means paying customers have no advantage over free users.
- Fix approach: Define where/how usage tracking is actually implemented (probably needs state storage outside markdown) or clarify this is handled by Claude Code runtime.

## Missing Critical Functionality

**PII Detection Scripts Referenced But Not Included:**
- Issue: Documentation references helper scripts that don't exist in the repository:
  - `detect-pii.py` mentioned in `comply` README (line 263-270)
  - `scan-secrets.sh` mentioned in `gdpr-analyzer.md` (line 521)
- Files:
  - `plugins/comply/README.md` (lines 263-270)
  - `plugins/comply/agents/gdpr-analyzer.md` (line 521)
- Impact: Commands cannot run automated scanning without these scripts. Documentation overstates capability.
- Fix approach: Either implement scripts in `plugins/comply/skills/eu-compliance/scripts/` or remove references and document that analysis is pattern-based only.

**Carbon Estimation Script Missing:**
- Issue: AGENTS.md (line 39) references testing `estimate-carbon.py` script but file doesn't exist
- Files: `AGENTS.md` (line 39)
- Impact: Cannot verify carbon calculation methodology. Scoring transparency is compromised.
- Fix approach: Implement script or update documentation to reflect actual implementation approach.

**Unimplemented Dependency Analysis Script:**
- Issue: AGENTS.md (line 36) references `analyze-dependencies.sh` but script not found
- Files: `AGENTS.md` (line 36)
- Impact: Dependency analysis scope (part of 9-scope EcoScore) cannot be validated as independent utility.
- Fix approach: Implement or remove from test/validation documentation.

## Integration Gaps

**ecoscore ↔ comply Integration Incomplete:**
- Issue: `comply` plugin documentation (lines 307-321 in README) states: "Comply uses the `ecoscore` plugin for CSRD metrics" and describes inter-plugin calling, but no actual command definitions show this integration.
- Files: `plugins/comply/README.md` (lines 307-321)
- Impact: CSRD compliance analysis depends on environmental data from ecoscore, but integration point is undocumented. Unclear if `/comply:audit csrd` invokes ecoscore directly or requires separate analysis.
- Fix approach: Define exact CLI/API contract between plugins. Document in command implementations or create INTEGRATION.md at repository root.

**Hook Execution Clarity:**
- Issue: Both plugins define `hooks.json` with PreToolUse matchers and prompt specifications, but unclear how JSON prompts execute when tools are used. No documentation of hook execution model.
- Files:
  - `plugins/ecoscore/hooks/hooks.json`
  - `plugins/comply/hooks/hooks.json`
- Impact: Cannot verify hooks will actually fire or what "systemMessage" output does in Claude Code context. Hooks may not work as intended.
- Fix approach: Document hook execution model in AGENTS.md or create HOOKS.md with examples of expected behavior.

## Test Coverage Gaps

**No Testing Infrastructure:**
- Issue: Repository contains no test files (.test.md, .spec.md, test scripts) for validating plugin functionality
- Files: Entire `plugins/` directory
- Impact: Cannot verify that agents trigger correctly, hooks execute properly, or scoring formulas work as documented. No regression detection.
- Fix approach: Create test suite for:
  - Agent trigger conditions (examples in agent YAML should trigger agent)
  - Hook execution (Pre/PostToolUse behavior)
  - Scoring calculations (verify 0-100 ranges produce expected results)
  - Integration points (ecoscore/comply data flow)

**No Validation for Complex Scoring:**
- Issue: Both plugins define complex scoring methodologies with weighted formulas and severity classifications, but no test data or verification exists
- Files:
  - `plugins/ecoscore/agents/ecoscore-analyzer.md` (lines 87-96: scoring weights)
  - `plugins/ecoscore/skills/green-it-analysis/SKILL.md` (lines 31-38: overall score formula)
  - `plugins/comply/agents/gdpr-analyzer.md` (lines 326-359: scoring system)
- Impact: Scoring could produce incorrect results without detection. Users trust numeric scores but methodology is unverified.
- Fix approach: Create test cases with example projects and verify outputs match expected scores.

## Documentation Inconsistencies

**Mismatched Command Tool Permissions:**
- Issue: `quick-check.md` declares tools `["Read", "Glob", "Grep"]` but describes needing `model: haiku` which suggests inference capability not reflected in allowed tools. `analyze.md` declares `Bash(npm:*, node:*, python:*, pip:*, go:*, cargo:*, git:*)` but also mentions running benchmarks which may require sudo/system access.
- Files:
  - `plugins/ecoscore/commands/quick-check.md` (lines 2-4)
  - `plugins/ecoscore/commands/analyze.md` (line 3)
- Impact: Tool permission lists don't match actual requirements. Commands may fail if Claude Code enforces declared permissions strictly.
- Fix approach: Audit actual tool usage in each command and update allowed-tools lists. Add inline comments explaining less obvious permissions.

**Version Mismatch Between marketplace.json and plugin.json:**
- Issue: `marketplace.json` shows ecoscore version "0.1.0" and comply version "0.1.0", but no version tracking for individual command/agent changes. Both plugins marked as "0.1.0" indefinitely.
- Files:
  - `.claude-plugin/marketplace.json` (lines 14-28)
  - `plugins/ecoscore/.claude-plugin/plugin.json` (line 2)
  - `plugins/comply/.claude-plugin/plugin.json` (line 2)
- Impact: Cannot track feature releases or breaking changes. All updates bundled together.
- Fix approach: Define versioning strategy. Consider semantic versioning for command additions/changes within a plugin version.

**Agent Trigger Examples Don't Map to Usage Instructions:**
- Issue: Agent frontmatter includes trigger examples (e.g., `ecoscore-analyzer.md` lines 5-11) but commands section in READMEs doesn't explain how users invoke agents vs. commands
- Files:
  - `plugins/ecoscore/README.md` (lines 33-36 show agent names but not invocation)
  - `plugins/comply/README.md` (lines 109-136 document agents but no usage examples)
- Impact: Users learn about agents but don't know how to access them. Documentation assumes knowledge of Claude Code agent triggering system.
- Fix approach: Add "Agent Invocation" section to each README with actual examples. Clarify difference between explicit `/plugin:command` and implicit agent triggers.

## Security Concerns

**Hardcoded Scoring and Configuration Assumptions:**
- Issue: Plugins assume specific cloud regions, model names, and service providers without allowing customization. scoring weights are hardcoded (not configurable). Compliance artifacts reference "Standard Contractual Clauses" and specific GDPR penalties without legal review disclaimer.
- Files:
  - `plugins/ecoscore/agents/ecoscore-analyzer.md` (lines 87-96: hardcoded weights)
  - `plugins/comply/agents/gdpr-analyzer.md` (lines 326-359: hardcoded penalties "Up to €20M or 4%")
  - `plugins/comply/agents/gdpr-analyzer.md` (lines 491-510: quality standards include legal interpretation)
- Impact: Plugins make regulatory/legal claims without professional legal review. Scoring doesn't account for project-specific requirements. Users may rely on inaccurate fines/penalties in decisions.
- Fix approach: Add prominent disclaimers that plugins provide technical guidance, not legal advice. Recommend consulting legal counsel. Make scoring weights configurable via `.claude/` config files.

**PII Detection Pattern Quality Unknown:**
- Issue: `gdpr-analyzer.md` (lines 83-99) shows regex patterns for detecting PII but no validation data for false positive/false negative rates mentioned. Quality statement claims "~95% accuracy with <5% false positives" but this is unverified.
- Files: `plugins/comply/agents/gdpr-analyzer.md` (lines 83-99, 353)
- Impact: PII detection may miss real violations or flag false positives. Users make decisions based on unvalidated accuracy claims.
- Fix approach: Document detection methodology limitations. Create test dataset of real codebases with known PII to validate accuracy. Remove accuracy claims until verified.

**Hook Prompts Request Compliance Decisions Without Context:**
- Issue: Hook prompts in both plugins ask Claude to make compliance decisions in PreToolUse context with 15-second timeout. Hooks can flag legitimate code as violations based on pattern matching without full context understanding.
- Files:
  - `plugins/comply/hooks/hooks.json` (lines 9-12: prompt requests GDPR violation detection)
  - `plugins/ecoscore/hooks/hooks.json` (lines 9-12: prompt requests anti-pattern detection)
- Impact: Hooks may incorrectly flag code during active development. False negatives in hook warnings don't block commits so users may miss real issues. Time pressure (15 seconds) may cause rushed analysis.
- Fix approach: Clarify that hooks are educational warnings only, not compliance assurance. Add warning in output: "This is a pattern match, not a legal opinion. Always verify before production."

## Scalability Concerns

**9-Scope Environmental Analysis Complexity:**
- Issue: EcoScore declares 9 analysis scopes with deep methodology but command implementations are markdown + prompts. No indication of how analysis scales with codebase size. Analyzing large projects (100K+ files) could hit token/execution limits.
- Files:
  - `plugins/ecoscore/commands/analyze.md` (lines 23-70: 9 scope descriptions)
  - `plugins/ecoscore/skills/green-it-analysis/SKILL.md` (lines 40-180: detailed methodology)
- Impact: Performance characteristics unknown. Large projects may timeout or produce incomplete analysis.
- Fix approach: Document recommended project sizes and scope limitations. Define maximum file/dependency counts that can be analyzed. Provide guidance for large projects.

**Compliance Audit Depth vs. Performance:**
- Issue: `gdpr-analyzer.md` (lines 59-99) describes exhaustive personal data detection including indirect identifiers, behavioral data, special categories, but no sampling strategy for large codebases. Could scan 10K+ files.
- Files: `plugins/comply/agents/gdpr-analyzer.md` (lines 59-99)
- Impact: Comprehensive analysis impossible in reasonable time on large projects. Users choose between quick shallow scan or waiting for deep analysis.
- Fix approach: Implement sampling strategy for large projects. Document analysis time estimates by project size. Consider progressive scanning (quick first, detailed on demand).

## Missing Reference Documentation

**No Architecture Decision Record (ADR):**
- Issue: Repository contains no ADRs explaining why plugin model was chosen, why these specific 9 scopes for EcoScore, why freemium for Comply. Design decisions are not documented.
- Files: Repository root
- Impact: Cannot understand design rationale. Future maintainers don't know constraints/tradeoffs. Difficult to debate architecture changes.
- Fix approach: Create `docs/adr/` directory with ADRs for major decisions.

**No Compliance/Audit Trail Model:**
- Issue: Both plugins describe audit outputs and compliance documentation but no specification of what audit trail should contain, how it's versioned, or how it integrates with external audit systems
- Files:
  - `plugins/comply/README.md` (lines 93-102: audit documentation mentioned)
  - `plugins/comply/README.md` (lines 104-107: output formats)
- Impact: Cannot implement audit trail feature without reversal engineering from vague description.
- Fix approach: Create `AUDIT_MODEL.md` specifying what audit data is collected, retention policy, export formats.

## Performance Anti-Patterns

**Potential N+1 Query Pattern in Documentation:**
- Issue: `gdpr-analyzer.md` (lines 54-60) instructs to "Search database models for personal data fields" then "Check API request/response payloads" then "Examine logging statements" then "Review analytics integrations" then "Scan localStorage/cookies usage" - this is sequential grep/read across many files without batching
- Files: `plugins/comply/agents/gdpr-analyzer.md` (lines 54-60)
- Impact: For large projects, analysis could perform hundreds of individual file reads instead of batched Glob+Grep. Memory usage and execution time suffer.
- Fix approach: Restructure analysis to batch file discovery first, then single pass through files.

**Redundant Compliance Check Execution:**
- Issue: Both hooks and agents perform similar pattern matching (PII detection, secrets detection). Running both hooks + agent analysis duplicates work
- Files:
  - `plugins/comply/hooks/hooks.json` (lines 10-12: checks PII)
  - `plugins/comply/agents/gdpr-analyzer.md` (lines 54-99: same checks)
- Impact: Users get double processing, slower response times
- Fix approach: Hooks should reference agent for deep analysis, not duplicate. Hooks remain lightweight warning only.

---

*Concerns audit: 2026-02-03*
