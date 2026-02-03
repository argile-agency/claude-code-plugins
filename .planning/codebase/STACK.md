# Technology Stack

**Analysis Date:** 2026-02-03

## Languages

**Primary:**
- Python 3.x - Utility scripts for carbon estimation and PII detection
- Markdown - Plugin content, documentation, commands, agents, skills

**Secondary:**
- YAML - Configuration for agents, commands, and hooks metadata
- JSON - Plugin manifests, marketplace configuration, hooks definitions
- Bash - CI/CD pipelines and shell automation (referenced in documentation)

## Runtime

**Environment:**
- Claude Code (Cloud-based execution)
- Python 3 runtime (for utility scripts)

**Package Manager:**
- pip (Python packages)
- No lockfile needed - scripts use standard library only

## Frameworks

**Core:**
- Claude Code Plugin System - Plugin architecture with commands, agents, hooks, and skills
- Markdown-based knowledge system - No build step required

**Scripting:**
- Python argparse - CLI argument parsing for utility scripts

## Key Dependencies

**Critical:**
- None - This is a plugin marketplace with no runtime dependencies for the plugin system itself
- Python standard library only (for carbon estimation and PII detection scripts)

**Infrastructure:**
- Claude Code execution environment - Handles tool access (Read, Glob, Grep, Bash)
- GitHub (for plugin distribution) - Plugins installable via GitHub URLs

## Configuration

**Environment:**
- Plugin configuration via YAML frontmatter in `.md` files
- No environment variables required for core plugin functionality
- Scripts accept CLI arguments (--json, --region, --tokens, etc.)

**Build:**
- No build step - Plugins are markdown-based
- Plugin metadata: `.claude-plugin/plugin.json` in each plugin directory
- Marketplace metadata: `.claude-plugin/marketplace.json` at root

## Platform Requirements

**Development:**
- Git for version control
- Text editor (any - markdown and JSON files)
- Python 3.x for running utility scripts locally

**Production:**
- Claude Code platform execution environment
- No additional runtime dependencies
- HTTP client capabilities for API integrations (handled by Claude Code tools)

## Plugin System Architecture

**Components:**
- **Commands** (`.md` files with YAML frontmatter): User-invocable via slash commands
- **Agents** (`.md` files with YAML frontmatter): Background processors triggered by natural language
- **Hooks** (`hooks.json`): Event-driven prompts supporting PreToolUse and PostToolUse matchers
- **Skills** (`SKILL.md` + `references/` subdirectories): Knowledge bases for context-aware assistance
- **Scripts** (Python utilities in `scripts/` directories): Standalone analysis tools

## Package/Manifest Files

**Marketplace Level:**
- `.claude-plugin/marketplace.json` - Owner info, plugin registry, marketplace metadata

**Plugin Level (per plugin):**
- `.claude-plugin/plugin.json` - Plugin name, version, author, description, keywords, license
- `commands/*.md` - Slash command definitions with allowed-tools, argument-hint, description
- `agents/*.md` - Agent definitions with model, color, tools, trigger examples
- `hooks/hooks.json` - Event hooks for PreToolUse/PostToolUse matchers
- `skills/*/SKILL.md` - Knowledge base with references/ subdirectory for detailed docs
- `skills/*/scripts/*.py` - Python utility scripts

## Plugin Tool Access

**Available Tools (per agent/command):**
- Read - File system reading
- Glob - Pattern-based file matching
- Grep - Content searching with regex
- Bash - Shell command execution

**Tool Constraints:**
- PreToolUse hooks in `.hooks.json` validate tool usage (warn-only, never block)
- Hooks support custom prompt logic for environmental and compliance checking

---

*Stack analysis: 2026-02-03*
