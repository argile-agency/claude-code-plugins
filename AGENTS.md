# AGENTS.md

This repository contains Claude Code plugins for professional workflows. Plugins are markdown-based with no build step required.

## Repository Structure

```
claude-code-plugins/
├── .claude-plugin/marketplace.json  # Marketplace configuration
├── plugins/<plugin-name>/
│   ├── .claude-plugin/plugin.json   # Plugin manifest
│   ├── commands/                    # Slash commands (*.md with YAML frontmatter)
│   ├── agents/                      # Subagents (*.md with YAML frontmatter)
│   ├── hooks/hooks.json             # Event hooks configuration
│   └── skills/                      # Knowledge bases (SKILL.md + references/)
```

## Build/Test/Lint

No build step required. Plugins are markdown and JSON files.

To validate a plugin structure:
```bash
# Verify JSON syntax
jq . .claude-plugin/marketplace.json
jq . plugins/ecoscore/.claude-plugin/plugin.json
jq . plugins/ecoscore/hooks/hooks.json

# Validate YAML frontmatter syntax
grep -A 5 "^---" plugins/ecoscore/commands/analyze.md
```

To test scripts (bash/python):
```bash
# Test dependency analysis
bash plugins/ecoscore/skills/green-it-analysis/scripts/analyze-dependencies.sh /path/to/project

# Test carbon estimation
python3 plugins/ecoscore/skills/green-it-analysis/scripts/estimate-carbon.py --tokens 10000 --model medium
```

## Code Style Guidelines

### File Organization

- **Plugin manifest**: `.claude-plugin/plugin.json` - name, version, description, keywords, license, author
- **Marketplace**: `.claude-plugin/marketplace.json` - owner info, plugin registry
- **Commands**: `commands/*.md` - user-invocable via `/pluginname:commandname`
- **Agents**: `agents/*.md` - background processors triggered by natural language
- **Hooks**: `hooks/hooks.json` - event-driven prompts for PreToolUse, PostToolUse
- **Skills**: `skills/*/SKILL.md` - knowledge bases with optional `references/` subdirectory

### YAML Frontmatter (Commands, Agents, Skills)

**Commands**:
```yaml
---
description: Clear one-line description
allowed-tools: Read, Glob, Grep, Bash(command:*)
argument-hint: [optional-arg]
---
```

**Agents**:
```yaml
---
name: agent-name
description: When to use this agent (include examples)
model: inherit
color: blue|green|purple|orange
tools: ["Read", "Grep", "Bash", ...]
---
```

**Skills**:
```yaml
---
name: Skill Name
description: When this skill should load automatically
version: X.Y.Z
---
```

### JSON Configuration

- Use 2-space indentation
- Maintain consistent key ordering (name → version → description → metadata)
- Include required fields: name, version, description
- Optional fields: keywords, license, author, owner

### Markdown Content

- Use ATX-style headings (`#`, `##`, `###`)
- Code blocks with language specifiers: ```javascript, ```bash, ```python
- Tables for structured data (alignment, scope breakdowns, quick references)
- Numbered lists for step-by-step processes
- Bullet points for unordered information

### Scripts (Bash, Python)

**Bash**:
- Shebang: `#!/bin/bash` at line 1
- Use quotes around variables: `"${VAR}"`
- Portable syntax (avoid bashisms when possible)
- Exit on errors: `set -e` when appropriate

**Python**:
- Shebang: `#!/usr/bin/env python3` at line 1
- Type hints for functions: `def func(arg: str) -> dict:`
- Docstrings (Google or numpy style)
- argparse for CLI scripts

### Naming Conventions

- **Files**: kebab-case (`analyze.md`, `green-advisor.md`)
- **Plugin names**: lowercase, single word (`ecoscore`)
- **Command names**: kebab-case (`quick-check`, `report`)
- **Agent names**: kebab-case (`ecoscore-analyzer`)
- **Skill names**: Title Case with spaces (`Green IT Analysis`)
- **JSON keys**: camelCase (`pluginName`, `allowedTools`)
- **YAML frontmatter fields**: lowercase with hyphens (`allowed-tools`, `argument-hint`)

### Error Handling

**Scripts**:
- Use `set -e` for bash to fail fast
- Check command existence: `command -v node &> /dev/null`
- Redirect stderr for cleanup: `2>/dev/null`
- Provide usage instructions on error

**JSON/YAML**:
- Validate syntax before committing
- Use `jq .` for JSON, `yamllint` for YAML if available

### Import and Reference Patterns

- Commands reference skills: "Use the skill-name skill for detailed methodology"
- Hooks reference commands: "Consider running /pluginname:commandname after changes"
- Skills use relative paths: `See references/file.md for detailed information`
- Script execution: `${CLAUDE_PLUGIN_ROOT}/skills/skill-name/scripts/script.sh`

### Commit Messages

Keep commit messages brief and concise. Do not mention AI assistance, models, or agents as authors. No Co-Authored-By lines referencing AI.

Examples:
- "Add ecoscore plugin for environmental impact analysis"
- "Update README with marketplace documentation"
- "Fix GitHub URL in README"

## Plugin Development Workflow

1. Create plugin directory: `plugins/plugin-name/`
2. Create manifest: `.claude-plugin/plugin.json`
3. Add components: `commands/`, `agents/`, `hooks/`, `skills/`
4. Update marketplace: `.claude-plugin/marketplace.json`
5. Validate JSON syntax
6. Test commands/agents/scripts if applicable

## Tool Usage Patterns

- **File discovery**: Use Glob for finding files (`**/*.md`, `package.json`)
- **Content search**: Use Grep for patterns in code (`SELECT \*`, `moment\.`)
- **File reading**: Use Read for content (never bash cat/head)
- **Commands**: Bash for scripts, git, npm, python execution
- **Multi-tool calls**: Batch independent operations in single message
