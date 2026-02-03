# Codebase Structure

**Analysis Date:** 2026-02-03

## Directory Layout

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace registry (owner, plugins list, metadata)
├── .planning/
│   └── codebase/                     # GSD analysis documents (auto-generated)
├── .claude/                          # Local overrides (not versioned)
├── README.md                         # Project overview
├── CLAUDE.md                         # Plugin development guidelines
├── LICENSE                           # MIT license
└── plugins/
    ├── ecoscore/                     # Environmental impact analysis plugin
    │   ├── .claude-plugin/
    │   │   └── plugin.json           # Manifest: name, version, description, keywords
    │   ├── README.md                 # Plugin usage documentation
    │   ├── commands/                 # User-invocable slash commands
    │   │   ├── analyze.md            # Full analysis with benchmarks
    │   │   ├── quick-check.md        # Fast static-only scan
    │   │   └── report.md             # Prioritized improvement checklist
    │   ├── agents/                   # NLP-triggered background processors
    │   │   ├── ecoscore-analyzer.md  # Environmental impact analysis agent
    │   │   └── green-advisor.md      # Commit-time sustainability guidance
    │   ├── skills/                   # Domain knowledge bases
    │   │   └── green-it-analysis/
    │   │       ├── SKILL.md          # Green IT methodology and scoring
    │   │       ├── references/       # Detailed documentation
    │   │       │   ├── ai-carbon-estimation.md
    │   │       │   ├── carbon-regions.md
    │   │       │   ├── dependency-alternatives.md
    │   │       │   └── frontend-patterns.md
    │   │       └── scripts/          # Utility scripts
    │   │           └── (future automation)
    │   └── hooks/
    │       ├── hooks.json            # Pre-tool hooks for write/edit warnings
    │       └── scripts/              # Hook supporting scripts
    │
    └── comply/                        # GDPR + CSRD compliance automation plugin
        ├── .claude-plugin/
        │   └── plugin.json           # Manifest: name, version, description, keywords
        ├── README.md                 # Plugin usage documentation
        ├── commands/                 # User-invocable slash commands
        │   ├── scan.md               # Quick compliance scan (free tier)
        │   ├── audit.md              # Deep audit with remediation (premium)
        │   └── report.md             # Generate audit-ready documentation
        ├── agents/                   # NLP-triggered background processors
        │   ├── gdpr-analyzer.md      # GDPR compliance analysis
        │   ├── csrd-analyzer.md      # CSRD sustainability reporting
        │   └── compliance-advisor.md # Educational guidance
        ├── skills/                   # Domain knowledge bases
        │   └── eu-compliance/
        │       ├── SKILL.md          # GDPR articles + CSRD standards
        │       ├── references/       # Detailed compliance documentation
        │       │   ├── gdpr-articles.md
        │       │   ├── csrd-esrs.md
        │       │   ├── pii-detection.md
        │       │   └── data-protection-patterns.md
        │       └── scripts/          # Utility scripts
        │           └── detect-pii.py # Automated PII detection
        └── hooks/
            └── hooks.json            # Pre-tool hooks for compliance warnings
```

## Directory Purposes

**`.claude-plugin/`:**
- Purpose: Marketplace metadata at root level
- Contains: `marketplace.json` with owner info, plugin registry, version
- Key files: `marketplace.json` (registry source of truth)

**`plugins/`:**
- Purpose: All plugin implementations
- Contains: Subdirectories named by plugin identifier
- Key files: Each plugin's `.claude-plugin/plugin.json` manifest

**`plugins/<plugin-name>/`:**
- Purpose: Plugin root directory with manifest and all components
- Contains: `.claude-plugin/plugin.json` + `commands/`, `agents/`, `skills/`, `hooks/`
- Key files: `plugin.json` (plugin identity), `README.md` (user documentation)

**`commands/`:**
- Purpose: User-invocable slash commands
- Contains: Markdown files with YAML frontmatter
- Key files: One `.md` file per command (e.g., `analyze.md`, `scan.md`)
- Pattern: Each file defines description, allowed-tools, argument-hint in frontmatter

**`agents/`:**
- Purpose: NLP-triggered autonomous processors
- Contains: Markdown files with YAML frontmatter defining agent metadata
- Key files: One `.md` file per agent (e.g., `ecoscore-analyzer.md`, `gdpr-analyzer.md`)
- Pattern: Each file includes trigger examples and system prompt

**`skills/`:**
- Purpose: Domain knowledge bases
- Contains: Skill-specific subdirectories with `SKILL.md` + `references/` + optional `scripts/`
- Key files: `SKILL.md` (methodology), files in `references/` (detailed docs)
- Pattern: Automatically loaded when keywords match in command/agent

**`skills/<skill-name>/references/`:**
- Purpose: Detailed supporting documentation
- Contains: Markdown reference files on specific topics
- Key files: Topic-specific docs (e.g., `dependency-alternatives.md`)
- Usage: Loaded on-demand within analysis context

**`hooks/`:**
- Purpose: Event-driven code analysis and warnings
- Contains: `hooks.json` configuration file
- Key files: `hooks.json` (hook definitions)
- Pattern: PreToolUse matchers trigger on Write/Edit operations

## Key File Locations

**Entry Points:**

- `/.claude-plugin/marketplace.json`: Plugin discovery endpoint; defines all registered plugins
- `plugins/ecoscore/commands/analyze.md`: Full environmental impact analysis command
- `plugins/comply/commands/scan.md`: Quick compliance scan command
- `plugins/ecoscore/agents/ecoscore-analyzer.md`: Autonomous environmental impact agent
- `plugins/comply/agents/gdpr-analyzer.md`: Autonomous GDPR compliance agent

**Configuration:**

- `plugins/ecoscore/.claude-plugin/plugin.json`: EcoScore plugin metadata
- `plugins/comply/.claude-plugin/plugin.json`: Comply plugin metadata
- `plugins/ecoscore/hooks/hooks.json`: EcoScore pre-write environmental warnings
- `plugins/comply/hooks/hooks.json`: Comply pre-write compliance warnings

**Core Logic:**

- `plugins/ecoscore/skills/green-it-analysis/SKILL.md`: 9-scope environmental analysis methodology
- `plugins/comply/skills/eu-compliance/SKILL.md`: GDPR articles + CSRD standards knowledge
- `plugins/ecoscore/commands/analyze.md`: Phase-by-phase analysis orchestration (discovery → static → benchmarks → scoring → reporting)
- `plugins/comply/commands/scan.md`: Free-tier scan logic (project discovery → GDPR check → CSRD check)

**Testing:**

- Not applicable; plugins are markdown-based with no build step

**Documentation:**

- `README.md`: Project overview and plugin marketplace description
- `CLAUDE.md`: Plugin architecture and development guidelines
- `plugins/ecoscore/README.md`: EcoScore plugin usage, features, commands, agents, configuration
- `plugins/comply/README.md`: Comply plugin usage, GDPR coverage, CSRD support, pricing

## Naming Conventions

**Files:**

- Plugin manifests: `plugin.json`
- Skill definitions: `SKILL.md`
- Commands: lowercase action names (e.g., `analyze.md`, `scan.md`, `report.md`)
- Agents: lowercase with hyphens (e.g., `ecoscore-analyzer.md`, `gdpr-analyzer.md`)
- Hooks: `hooks.json` (standard name)
- References: lowercase with hyphens (e.g., `ai-carbon-estimation.md`, `dependency-alternatives.md`)

**Directories:**

- Plugin names: lowercase (e.g., `ecoscore`, `comply`)
- Skill names: lowercase with hyphens (e.g., `green-it-analysis`, `eu-compliance`)
- Standard sections: `commands/`, `agents/`, `skills/`, `hooks/`, `references/`

**Identifiers in Markdown:**

- Commands invoked as: `/pluginname:commandname`
- Agent names in frontmatter: lowercase with hyphens (e.g., `ecoscore-analyzer`)
- Skill triggers: keywords in YAML frontmatter match Claude's context

## Where to Add New Code

**New Command:**
1. Create `plugins/<plugin-name>/commands/<commandname>.md`
2. Add YAML frontmatter: `description`, `allowed-tools`, `argument-hint`
3. Include step-by-step instruction prompt
4. Register in plugin README and marketplace.json if needed

**New Agent:**
1. Create `plugins/<plugin-name>/agents/<agentname>.md`
2. Add YAML frontmatter: `name`, `description`, `model`, `color`, `tools`
3. Include trigger examples in frontmatter (`<example>` tags)
4. Add system prompt explaining agent expertise and analysis framework
5. Reference skills by keyword matching

**New Skill:**
1. Create `plugins/<plugin-name>/skills/<skillname>/`
2. Create `SKILL.md` with frontmatter (name, description, version, trigger keywords)
3. Add detailed methodology in markdown
4. Create `references/` subdirectory with topic-specific docs
5. Skill auto-loads when keywords appear in command/agent descriptions

**New Hook:**
1. Add entry to `plugins/<plugin-name>/hooks/hooks.json`
2. Define `matcher` (tool names like "Write|Edit|Bash")
3. Write `prompt` that checks code for violations
4. Return JSON with `permissionDecision: "allow"` and optional warning in `systemMessage`
5. Set appropriate `timeout` (15-30 seconds typical)

**New Reference Document:**
1. Create file in `plugins/<plugin-name>/skills/<skillname>/references/`
2. Use descriptive lowercase hyphenated name (e.g., `security-patterns.md`)
3. Write as detailed markdown documentation
4. Link from SKILL.md or reference in skill content

## Special Directories

**`.claude-plugin/`:**
- Purpose: Plugin metadata (not code)
- Generated: No
- Committed: Yes (contains plugin.json manifest)
- Content: Plugin identity, version, keywords, license

**`references/`:**
- Purpose: Detailed topic documentation
- Generated: No
- Committed: Yes (part of knowledge base)
- Content: Markdown reference files loaded on-demand

**`.planning/codebase/`:**
- Purpose: GSD analysis documents
- Generated: Yes (by GSD mapper commands)
- Committed: Yes (analysis outputs)
- Content: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, CONCERNS.md, STACK.md, INTEGRATIONS.md

**`scripts/`:**
- Purpose: Utility automation scripts (Python, shell, etc.)
- Generated: No
- Committed: Yes (skill-specific automation)
- Content: Support scripts for skills (e.g., `detect-pii.py`)

---

*Structure analysis: 2026-02-03*
