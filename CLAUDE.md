# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace repository containing premium plugins for professional workflows. Plugins are markdown-based with no build step required.

## Architecture

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace metadata (owner, plugin list)
└── plugins/
    └── <plugin-name>/
        ├── .claude-plugin/
        │   └── plugin.json   # Plugin manifest (name, version, description)
        ├── commands/         # Slash commands (*.md with YAML frontmatter)
        ├── agents/           # Subagents (*.md with YAML frontmatter)
        ├── hooks/            # Event hooks (hooks.json)
        └── skills/           # Knowledge skills (SKILL.md + references/)
```

### Plugin Components

- **Commands**: User-invocable via `/pluginname:commandname`. Define with YAML frontmatter (`description`, `allowed-tools`, `argument-hint`).
- **Agents**: Background processors triggered by natural language. Frontmatter includes `name`, `description`, `model`, `color`, `tools`.
- **Hooks**: Event-driven prompts defined in `hooks.json`. Support `PreToolUse`, `PostToolUse` matchers.
- **Skills**: Knowledge bases in `SKILL.md` files. Loaded automatically when relevant context detected. Can include `references/` subdirectories for detailed documentation.

### Marketplace Configuration

`/.claude-plugin/marketplace.json` registers available plugins with their paths and metadata. Each plugin's `plugin.json` contains its individual manifest.

## Commit Messages

- Keep commit messages brief and concise
- Do not mention AI assistance, models, or agents as authors
- Do not include Co-Authored-By lines referencing AI

## Current Plugins

### ecoscore

Environmental impact analysis plugin with 9 analysis scopes (code efficiency, dependencies, data transfer, AI/LLM usage, build/CI-CD, frontend/UX, database, network, infrastructure). Provides numeric scoring (0-100) and actionable checklists.

Commands: `analyze`, `quick-check`, `report`
Agents: `ecoscore-analyzer`, `green-advisor`
