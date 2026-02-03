# Coding Conventions

**Analysis Date:** 2026-02-03

## Overview

This codebase is a Claude Code plugin marketplace containing markdown-based plugins with YAML frontmatter for metadata. There is no compiled code—all components are declarative configurations and documentation. Conventions are lightweight and focused on consistency across markdown, JSON, and bash/python scripts.

## Naming Patterns

**Files:**
- Commands: kebab-case (e.g., `analyze.md`, `quick-check.md`)
- Agents: kebab-case (e.g., `ecoscore-analyzer.md`, `gdpr-analyzer.md`)
- Skills: SKILL.md (uppercase) with references in subdirectory
- Config files: JSON or JSON format (plugin.json, hooks.json, marketplace.json)
- Scripts: kebab-case.sh or kebab-case.py (e.g., `analyze-dependencies.sh`)

**Plugin names:**
- Lowercase, single word (e.g., `ecoscore`, `comply`)
- Location: `plugins/<plugin-name>/`

**Command/Agent/Skill names:**
- Internal name (in metadata): lowercase with hyphens (e.g., `ecoscore-analyzer`, `quick-check`)
- Display name (in description): Title Case with spaces (e.g., `Green IT Analysis`, `GDPR Analyzer`)
- Examples from codebase: `plugins/ecoscore/commands/analyze.md`, `plugins/comply/agents/gdpr-analyzer.md`

**JSON keys:**
- camelCase: `pluginName`, `allowedTools`, `scopeBreakdown`
- YAML frontmatter fields: lowercase with hyphens (`allowed-tools`, `argument-hint`, `description`)
- Examples from `plugins/ecoscore/.claude-plugin/plugin.json`:
  ```json
  {
    "name": "ecoscore",
    "version": "0.1.0",
    "description": "...",
    "author": { "name": "..." }
  }
  ```

**Directory names:**
- Lowercase: `commands/`, `agents/`, `hooks/`, `skills/`
- Plugin names: lowercase (`ecoscore`, `comply`)
- Reference subdirectories: lowercase with hyphens (`eu-compliance`, `green-it-analysis`)

## Code Style

**Formatting:**
- JSON: 2-space indentation (see `.claude-plugin/marketplace.json`, `plugins/*/hooks/hooks.json`)
- Markdown: ATX-style headings (`#`, `##`, `###`)
- Code blocks: Always specify language (```javascript, ```bash, ```python, ```typescript)
- Tables: Use markdown pipe syntax with alignment

**JSON Files:**
- Maintain consistent key ordering: name → version → description → metadata → plugins/keywords/license/author
- Include required fields: name, version, description
- Optional fields: keywords, license, author, owner, category, tags
- Example from `.claude-plugin/marketplace.json`:
  ```json
  {
    "name": "argile-skills",
    "owner": {
      "name": "Argile Agency",
      "email": "aloha@argile.agency",
      "website": "https://argile.agency"
    },
    "metadata": {
      "description": "...",
      "version": "1.0.0"
    },
    "plugins": [...]
  }
  ```

**Markdown Content:**
- Use ATX-style headings with proper hierarchy
- Numbered lists for step-by-step processes (1, 2, 3...)
- Bullet points for unordered information
- Bold for emphasis on key terms: `**term**`
- Italics for supplementary notes: `*note*`
- Code inline for: file paths (backticks), command names, variable names
- Backtick format for file paths: `` `src/services/user.ts` ``

**Linting:**
- No automated linter enforced (markdown-friendly environment)
- JSON syntax validated manually with `jq .` before commit (as noted in AGENTS.md)
- YAML frontmatter validated by reading first file lines

## YAML Frontmatter Patterns

**Commands** (`plugins/<plugin>/commands/*.md`):
```yaml
---
description: Clear one-line description of what command does
allowed-tools: Read, Glob, Grep, Bash(npm:*, node:*, python:*, pip:*, git:*)
argument-hint: [optional-arg-name]
---
```

**Agents** (`plugins/<plugin>/agents/*.md`):
```yaml
---
name: agent-name-kebab-case
description: When to use this agent (include concrete examples with user message)
model: inherit
color: blue|green|purple|orange|yellow
tools: ["Read", "Glob", "Grep", "Bash"]
---
```

**Skills** (`plugins/<plugin>/skills/*/SKILL.md`):
```yaml
---
name: Skill Name (Title Case with Spaces)
description: When this skill should load automatically
version: X.Y.Z
---
```

**Concrete examples:**
- From `plugins/ecoscore/commands/quick-check.md`: `allowed-tools: Read, Glob, Grep` + `model: haiku`
- From `plugins/comply/agents/gdpr-analyzer.md`: `color: blue`, `tools: ["Read", "Glob", "Grep", "Bash"]`
- From `plugins/ecoscore/agents/green-advisor.md`: `model: haiku`, `color: yellow` (for quick reviews)

## Import Organization

**Pattern in Commands and Agents:**
1. Skills referenced by name: `Use the skill-name skill for detailed methodology`
2. Tools specified in YAML frontmatter (not imported)
3. File references use relative paths from skill root: `See references/file.md for details`
4. Script execution references: `${CLAUDE_PLUGIN_ROOT}/skills/skill-name/scripts/script.sh`

**Examples from codebase:**
- `plugins/ecoscore/commands/analyze.md`: "Use the green-it-analysis skill knowledge for scoring methodology"
- `plugins/comply/commands/scan.md`: "Use `eu-compliance` skill for GDPR patterns and detection rules"
- Skills reference: `plugins/ecoscore/skills/green-it-analysis/SKILL.md` → "See `references/dependency-alternatives.md`"

**Directory references:**
- Relative to plugin root: `plugins/ecoscore/commands/analyze.md` references `commands/quick-check` as `/ecoscore:quick-check`
- Skills referenced by internal name from marketplace: `green-it-analysis`, `eu-compliance`

## Error Handling

**Bash Scripts:**
- Use `set -e` for fail-fast behavior (as documented in AGENTS.md)
- Check command existence: `command -v node &> /dev/null`
- Redirect stderr for cleanup: `2>/dev/null`
- Provide clear usage instructions on error

**Python Scripts:**
- Shebang: `#!/usr/bin/env python3` at line 1
- Type hints required: `def func(arg: str) -> dict:`
- Use argparse for CLI argument parsing
- Docstrings for functions (Google or numpy style)

**JSON/YAML Validation:**
- Validate JSON: `jq . .claude-plugin/marketplace.json` (as noted in AGENTS.md line 25)
- Validate YAML frontmatter by ensuring proper `---` delimiters

**Agent/Command Output:**
- Always return structured response JSON when applicable (see hooks.json pattern)
- Use markdown for human-readable output
- Include fallback messages for edge cases

**Examples from hooks.json:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow"
  },
  "systemMessage": "[Brief warning or empty string]"
}
```

## Logging and Output

**Console Output:**
- Use markdown formatting for readability
- Tables for structured data (scope breakdowns, compliance scores)
- Code blocks for examples and recommendations
- Brief, actionable language (avoid verbose explanations)

**Examples from commands:**
- `plugins/ecoscore/commands/analyze.md`: Output format includes table of scope breakdown with Score | Issues columns
- `plugins/comply/commands/scan.md`: Output structured as markdown with sections, checklists, and metrics

**Markdown Output Structure:**
```markdown
## Title

**Score:** X/100

### Section 1
- Point 1
- Point 2

### Section 2
| Column | Column |
|--------|--------|
| Data   | Data   |
```

## Comments and Documentation

**When to Comment:**
- Explain complex scoring algorithms (e.g., in agent descriptions)
- Document regex patterns for PII detection (e.g., in GDPR analyzer)
- Clarify GDPR article references and legal requirements
- Provide code examples showing BAD → GOOD patterns

**JSDoc/TSDoc:**
- Not used (no TypeScript in codebase)
- Use code block examples instead with BAD/GOOD markers

**Examples from codebase:**
- From `plugins/comply/agents/gdpr-analyzer.md`:
  ```typescript
  // ❌ BAD - Invalid consent
  <input type="checkbox" checked> I agree to all terms

  // ✅ GOOD - Valid consent
  <input type="checkbox"> Send me marketing emails
  ```

## Function/Process Design

**Size:**
- Commands: 1-3 main sections (discovery, analysis, output)
- Agents: Well-structured sections with clear responsibilities
- Keep prompt text under 200 words for Haiku model agents (see `green-advisor.md` guideline)

**Parameters:**
- Commands use `$ARGUMENTS` variable for optional arguments
- Tools specified in YAML frontmatter as allowed-tools/tools
- No function parameters—configuration-driven

**Return Values:**
- Commands return markdown-formatted results
- Agents return JSON for hook outputs
- Structured, scannable format (tables, checklists, scores)

**Examples:**
- `plugins/ecoscore/commands/quick-check.md`: Outputs markdown with structured sections, estimated score, and actionable items
- `plugins/comply/commands/scan.md`: Returns markdown report with scores, checklists, and highlighted gaps

## Module Design

**Plugin Structure:**
```
plugins/<plugin-name>/
├── .claude-plugin/plugin.json       # Manifest (name, version, description)
├── commands/                        # User-invocable commands
│   ├── command1.md
│   └── command2.md
├── agents/                          # Background processors
│   ├── agent1.md
│   └── agent2.md
├── hooks/hooks.json                 # Event-driven hooks
└── skills/                          # Knowledge bases
    └── skill-name/
        ├── SKILL.md
        ├── references/
        │   ├── file1.md
        │   └── file2.md
        └── scripts/
            ├── script1.sh
            └── script2.py
```

**Exports Pattern:**
- Each command/agent is independently executable
- Skills are auto-loaded by matching description keywords
- No barrel files—direct file references

**Cross-Plugin References:**
- Marketplace config: `.claude-plugin/marketplace.json` registers all plugins
- Commands can reference other plugins: `/pluginname:commandname`
- Skills are referenced by name from YAML frontmatter

**Example from codebase:**
- `.claude-plugin/marketplace.json` lists: ecoscore plugin at `plugins/ecoscore` and comply plugin at `plugins/comply`
- `plugins/ecoscore/commands/analyze.md` references `/ecoscore:quick-check` as alternative
- `plugins/comply/commands/scan.md` references `/comply:audit` as premium feature

## Frontmatter Metadata Conventions

**Required fields always present:**
- `description`: Clear, action-oriented summary
- `name` (agents/skills): Unique identifier or display name
- `allowed-tools` (commands): Exact list of tools permitted
- `model` (agents): "inherit" for default or specific model name
- `tools` (agents): Array of available tools

**Optional fields used consistently:**
- `color`: For agent visual differentiation (blue, green, purple, orange, yellow)
- `argument-hint`: Parameter name or description
- `version`: Semantic versioning for skills
- `keywords`: Array for plugin discovery
- `author`/`owner`: Contact information

**Example from `plugins/ecoscore/agents/ecoscore-analyzer.md`:**
```yaml
---
name: ecoscore-analyzer
description: Use this agent when...
model: inherit
color: green
tools: ["Read", "Glob", "Grep", "Bash"]
---
```

## Convention Violations to Avoid

1. **DO NOT** use camelCase for file names (use kebab-case)
2. **DO NOT** mix markdown heading styles (use only `#`, not underlines)
3. **DO NOT** hardcode file paths without backticks
4. **DO NOT** use undefined tool references in frontmatter
5. **DO NOT** create commands without `allowed-tools` frontmatter
6. **DO NOT** use 4-space indentation in JSON (always 2-space)
7. **DO NOT** reference skills that don't exist in the plugins
8. **DO NOT** include AI model names or assistance mentions in commit messages (per CLAUDE.md)

---

*Convention analysis: 2026-02-03*
