# Testing Patterns

**Analysis Date:** 2026-02-03

## Overview

This codebase is markdown-based with no traditional unit tests or test runner. Testing is achieved through:
1. **JSON validation** - Structural correctness of manifest and config files
2. **Script validation** - Bash and Python scripts in skills
3. **Manual testing** - Agent and command functionality verification
4. **Declarative testing** - Validation via documentation and examples

## Test Framework

**Test Execution:**
- No formal test runner (Jest, Vitest, pytest, etc.)
- Manual validation via command-line tools
- CI/CD testing would occur at plugin installation/usage time

**Validation Approach:**
- JSON syntax validation: `jq . <file>`
- YAML frontmatter validation: Manual parsing of `---` delimiters
- Bash script validation: `bash -n <script>` (syntax check only)
- Python script validation: `python3 -m py_compile <script>`

**Run Commands** (as documented in AGENTS.md):
```bash
# Validate JSON syntax
jq . .claude-plugin/marketplace.json
jq . plugins/ecoscore/.claude-plugin/plugin.json
jq . plugins/ecoscore/hooks/hooks.json

# Validate YAML frontmatter syntax
grep -A 5 "^---" plugins/ecoscore/commands/analyze.md

# Test scripts if present
bash plugins/ecoscore/skills/green-it-analysis/scripts/analyze-dependencies.sh /path/to/project
python3 plugins/ecoscore/skills/green-it-analysis/scripts/estimate-carbon.py --tokens 10000 --model medium
```

## Test File Organization

**Validation Location:**
- JSON files: In root and `.claude-plugin/` directories
- Scripts: In `skills/<skill-name>/scripts/` directories
- Documentation: Co-located with component files

**Naming Pattern:**
- Manifest files: `plugin.json` (singular, required)
- Hook configuration: `hooks.json` (singular, required)
- Marketplace registry: `marketplace.json` (singular, root only)

**Structure by Component Type:**
```
plugins/<plugin>/
├── .claude-plugin/plugin.json        # Validated with jq
├── hooks/hooks.json                  # Validated with jq
├── commands/                         # Validated by checking YAML frontmatter
│   ├── command1.md
│   └── command2.md
├── agents/                           # Validated by checking YAML frontmatter
│   ├── agent1.md
│   └── agent2.md
└── skills/
    └── <skill>/
        ├── SKILL.md                  # Validated by checking YAML frontmatter
        ├── references/               # Markdown validation (referenced paths exist)
        │   ├── file1.md
        │   └── file2.md
        └── scripts/
            ├── script1.sh            # Syntax check: bash -n
            └── script2.py            # Syntax check: python3 -m py_compile
```

## Frontmatter Validation Pattern

**YAML Frontmatter Structure:**
Every command, agent, and skill must start with YAML metadata block:
```yaml
---
key: value
key2: value2
---
```

**Validation checks:**
1. File starts with `---` on first line
2. Contains closing `---` marker
3. All required keys present for component type
4. No syntax errors in YAML

**Examples from codebase:**
- `plugins/ecoscore/commands/analyze.md`:
  ```yaml
  ---
  description: Full environmental impact analysis with benchmarks
  allowed-tools: Read, Glob, Grep, Bash(npm:*, node:*, python:*, pip:*, go:*, cargo:*, git:*)
  argument-hint: [scope]
  ---
  ```

- `plugins/comply/agents/gdpr-analyzer.md`:
  ```yaml
  ---
  name: gdpr-analyzer
  description: Use when user asks about GDPR compliance...
  model: inherit
  color: blue
  tools: ["Read", "Glob", "Grep", "Bash"]
  ---
  ```

## JSON Validation Patterns

**Plugin Manifest** (`plugins/<plugin>/.claude-plugin/plugin.json`):
```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "...",
  "author": { "name": "..." },
  "keywords": [...],
  "license": "MIT"
}
```

**Marketplace Registry** (`.claude-plugin/marketplace.json`):
```json
{
  "name": "marketplace-name",
  "owner": { "name": "...", "email": "...", "website": "..." },
  "metadata": { "description": "...", "version": "..." },
  "plugins": [
    {
      "name": "plugin-name",
      "path": "plugins/plugin-name",
      "description": "...",
      "version": "0.1.0",
      "category": "...",
      "tags": [...]
    }
  ]
}
```

**Hooks Configuration** (`plugins/<plugin>/hooks/hooks.json`):
```json
{
  "description": "...",
  "hooks": {
    "PreToolUse|PostToolUse": [
      {
        "matcher": "Tool1|Tool2",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "...",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

**Validation syntax:**
```bash
# Quick syntax check
jq . .claude-plugin/marketplace.json

# Validate all JSON files
jq . plugins/ecoscore/.claude-plugin/plugin.json
jq . plugins/ecoscore/hooks/hooks.json
jq . plugins/comply/.claude-plugin/plugin.json
jq . plugins/comply/hooks/hooks.json
```

## Script Testing Patterns

**Bash Scripts** (`*.sh`):
- Located in `skills/<skill>/scripts/` directories
- Shebang required: `#!/bin/bash`
- Syntax validation: `bash -n script.sh`
- Runtime testing: Execute with sample inputs

**Example structure from AGENTS.md documentation:**
```bash
#!/bin/bash
set -e  # Fail on errors

# Check command exists
command -v node &> /dev/null || { echo "Node.js required"; exit 1; }

# Main logic
echo "Processing..."
exit 0
```

**Python Scripts** (`*.py`):
- Located in `skills/<skill>/scripts/` directories
- Shebang required: `#!/usr/bin/env python3`
- Type hints in function signatures: `def func(arg: str) -> dict:`
- Docstrings for functions
- Syntax validation: `python3 -m py_compile script.py`
- Runtime testing: Execute with sample parameters

**Example testing approach (from AGENTS.md line 33-39):**
```bash
# Test dependency analysis
bash plugins/ecoscore/skills/green-it-analysis/scripts/analyze-dependencies.sh /path/to/project

# Test carbon estimation
python3 plugins/ecoscore/skills/green-it-analysis/scripts/estimate-carbon.py --tokens 10000 --model medium
```

## Manual Testing Patterns

**Command Testing:**
1. Verify YAML frontmatter is valid
2. Test with sample arguments via Claude interface
3. Verify output format matches documented markdown structure
4. Check tool permissions match allowed-tools list

**Agent Testing:**
1. Verify trigger conditions in description
2. Test with natural language matching examples
3. Verify output structure and timing
4. Check color/model assignments

**Hook Testing:**
1. Verify JSON syntax in hooks.json
2. Test matcher patterns (PreToolUse/PostToolUse)
3. Verify timeout values are reasonable
4. Check prompt logic makes sense

**Examples from codebase:**
- `plugins/ecoscore/hooks/hooks.json` defines PreToolUse hook for Write/Edit operations
  - Matcher: "Write|Edit"
  - Prompt checks for: heavy dependencies, AI inefficiency, database issues
  - Permission decision: Always "allow" (warn-only)

## Test Data and Fixtures

**Not applicable** - No traditional fixtures or test data.

**Documentation Examples** serve as test cases:
- Agent descriptions include `<example>` blocks with sample user messages
- Commands include example output formats
- Skills include regex patterns and code examples

**Examples from codebase:**
- `plugins/ecoscore/agents/ecoscore-analyzer.md`: Three `<example>` blocks showing trigger contexts
- `plugins/comply/agents/gdpr-analyzer.md`: Extensive code examples showing BAD ❌ and GOOD ✅ patterns
- `plugins/comply/commands/scan.md`: Detailed output format template in markdown

## Coverage Requirements

**Coverage Approach:**
- No automated code coverage measurement (not applicable to markdown)
- Manual verification that all components have documentation
- Verification that all external references are valid (skills exist, scripts are callable)

**Completeness checks:**
1. All plugins listed in marketplace.json exist in plugins/ directory
2. All commands in commands/ are properly frontmatted
3. All agents in agents/ are properly frontmatted
4. All skills referenced in commands/agents exist as SKILL.md files
5. All scripts referenced in documentation are callable

**Example verification pattern:**
```bash
# Verify marketplace plugins exist
jq -r '.plugins[].path' .claude-plugin/marketplace.json | while read path; do
  [ -d "$path" ] && echo "✓ $path exists" || echo "✗ $path missing"
done

# Verify all commands have YAML frontmatter
grep -l "^description:" plugins/*/commands/*.md | wc -l
```

## Test Types

**Structural Tests:**
- JSON schema validation (jq with filters)
- YAML frontmatter presence and syntax
- File path existence checks
- Reference integrity (skills, commands, agents)

**Functional Tests:**
- Script syntax validation (bash -n, python3 -m py_compile)
- Command argument hint parsing
- Tool permission verification against allowed-tools

**Documentation Tests:**
- Example code blocks have proper formatting
- Code examples show BAD and GOOD patterns
- Regulatory references (GDPR articles, CSRD standards) are accurate
- Markdown formatting is consistent

**Integration Tests:**
- Skills are properly referenced and loaded
- Commands invoke correct tools
- Agents trigger on expected language patterns
- Hooks execute without errors

## Common Test Patterns

**Validating a New Command:**
1. Create file: `plugins/<plugin>/commands/command-name.md`
2. Add frontmatter with required fields
3. Run: `grep -A 3 "^---" plugins/<plugin>/commands/command-name.md`
4. Verify: description, allowed-tools, optional argument-hint present
5. Check markdown formatting (headings, code blocks, tables)

**Validating a New Agent:**
1. Create file: `plugins/<plugin>/agents/agent-name.md`
2. Add frontmatter with all required fields
3. Run: `grep -A 5 "^---" plugins/<plugin>/agents/agent-name.md`
4. Verify: name, description, model, color, tools all present
5. Check description includes `<example>` blocks
6. Ensure color value is valid (blue|green|purple|orange|yellow)

**Validating a New Skill:**
1. Create directory: `plugins/<plugin>/skills/skill-name/`
2. Create: `plugins/<plugin>/skills/skill-name/SKILL.md` with frontmatter
3. Add references in: `plugins/<plugin>/skills/skill-name/references/`
4. Verify: name, description, version in frontmatter
5. Check markdown sections match description context

**Validating a New Hook:**
1. Create/edit: `plugins/<plugin>/hooks/hooks.json`
2. Run: `jq . plugins/<plugin>/hooks/hooks.json`
3. Verify: description, hooks, matcher, type, prompt, timeout all present
4. Check: timeout value is reasonable (5-30 seconds typical)
5. Test: prompt logic with sample scenarios

## Validation Checklist

Before committing changes:

- [ ] All JSON files pass `jq . <file>`
- [ ] All markdown files have proper YAML frontmatter (start/end with `---`)
- [ ] All commands have `allowed-tools` in frontmatter
- [ ] All agents have `name`, `model`, `color`, `tools` in frontmatter
- [ ] All skills have `name`, `description`, `version` in frontmatter
- [ ] File names use kebab-case (not camelCase)
- [ ] Plugin names are lowercase
- [ ] Marketplace.json lists all plugins with correct paths
- [ ] All referenced skills exist in the codebase
- [ ] Code examples use BAD ❌ and GOOD ✅ markers consistently
- [ ] Markdown uses ATX-style headings only
- [ ] Tables are properly formatted with pipes and dashes
- [ ] Scripts have correct shebangs (`#!/bin/bash`, `#!/usr/bin/env python3`)
- [ ] Hook matchers are valid (PreToolUse, PostToolUse)
- [ ] Agent colors are valid (blue|green|purple|orange|yellow)
- [ ] Commit message does not mention AI assistance (per CLAUDE.md)

---

*Testing analysis: 2026-02-03*
