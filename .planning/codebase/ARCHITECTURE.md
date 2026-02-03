# Architecture

**Analysis Date:** 2026-02-03

## Pattern Overview

**Overall:** Plugin Marketplace Architecture with Declarative Components

**Key Characteristics:**
- Markdown-based plugin system with YAML frontmatter (no build step)
- Event-driven hook system for pre/post-tool triggers
- Skill-based knowledge loading with automatic context detection
- Command/agent dual interface (slash commands for manual invocation, agents for NLP-driven)
- Centralized marketplace registry with per-plugin isolation

## Layers

**Marketplace Layer:**
- Purpose: Central plugin registry and discovery
- Location: `/.claude-plugin/marketplace.json`
- Contains: Plugin metadata, version info, owner details, tags
- Depends on: Individual plugin manifests
- Used by: Claude Code plugin system for installation/activation

**Plugin Layer:**
- Purpose: Self-contained functional units with CLI and NLP interfaces
- Location: `plugins/<plugin-name>/`
- Contains: Plugin manifest, commands, agents, hooks, skills
- Depends on: Marketplace registry
- Used by: User commands and natural language triggers

**Command Layer:**
- Purpose: User-invocable slash commands for explicit actions
- Location: `plugins/<plugin-name>/commands/*.md`
- Contains: YAML frontmatter (description, allowed-tools, argument-hint) + prompt/instructions
- Depends on: Skills knowledge, allowed tools
- Used by: `/pluginname:commandname` syntax

**Agent Layer:**
- Purpose: Background processors triggered by natural language patterns
- Location: `plugins/<plugin-name>/agents/*.md`
- Contains: Agent metadata (name, description, model, color, tools), system prompt
- Depends on: Skills knowledge
- Used by: Claude Code NLP detection (examples in frontmatter)

**Skill Layer:**
- Purpose: Domain knowledge bases for contextual enhancement
- Location: `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`
- Contains: YAML frontmatter (name, description, version, trigger keywords), markdown content
- Depends on: Reference documentation
- Used by: Commands and agents (loaded automatically on keyword match)

**Hook Layer:**
- Purpose: Event-driven interventions during tool usage
- Location: `plugins/<plugin-name>/hooks/hooks.json`
- Contains: PreToolUse/PostToolUse matchers with prompt-based handlers
- Depends on: Tool calls (Read, Write, Edit, Bash, etc.)
- Used by: Pre-commit warnings, compliance checking

**Reference Layer:**
- Purpose: Detailed documentation for skill enrichment
- Location: `plugins/<plugin-name>/skills/<skill-name>/references/`
- Contains: Markdown documentation files on specific topics
- Depends on: Nothing (static knowledge)
- Used by: Skills (via markdown includes or context references)

## Data Flow

**Command Invocation Flow:**

1. User types `/pluginname:commandname [args]`
2. Claude Code parses command name from marketplace registry
3. Loads command file from `commands/<commandname>.md`
4. Extracts allowed-tools from YAML frontmatter
5. Substitutes `$ARGUMENTS` in prompt
6. Executes prompt with restricted tool access
7. Returns result to user

**Agent Trigger Flow:**

1. User asks a question or mentions trigger keywords
2. Claude Code evaluates agent `description` and examples
3. If match detected, spawns agent subthread with agent system prompt
4. Agent has access to declared tools only
5. Agent loads relevant skills based on keyword matching
6. Agent runs analysis and returns findings
7. Results presented as agent-branded output

**Hook Intervention Flow:**

1. User calls a tool (Read, Write, Edit, Bash, etc.)
2. Tool execution enters pre-hook phase
3. If matcher matches tool name (e.g., "Write|Edit"), trigger prompt
4. Hook prompt analyzes code being written
5. Hook returns JSON with `permissionDecision` ("allow"/"deny") and optional `systemMessage`
6. Tool execution continues or stops based on decision
7. System message appears as warning to user (warn-only pattern: always "allow")

**Skill Auto-Loading Flow:**

1. Command or agent begins execution
2. Claude Code detects keywords in its description or prompt
3. Matches against skill frontmatter `description` field
4. Loads skill SKILL.md content into context
5. Skill knowledge available for use in analysis
6. References/ subdirectory provides detailed information on demand

## Key Abstractions

**Plugin:**
- Purpose: Standalone functional module with manifest-defined interface
- Examples: `plugins/ecoscore`, `plugins/comply`
- Pattern: Directory structure with `.claude-plugin/plugin.json` manifest containing name, version, description, keywords, license
- Encapsulation: Commands, agents, skills, hooks isolated per plugin
- Extension: New plugins follow same directory structure pattern

**Command:**
- Purpose: Explicit, user-invoked analysis or action
- Examples: `commands/analyze.md`, `commands/scan.md`, `commands/report.md`
- Pattern: Markdown file with YAML frontmatter specifying description, allowed-tools, argument-hint
- Execution: Runs with restricted tool access (allowlist in frontmatter)
- Arguments: Passed via `$ARGUMENTS` substitution in prompt

**Agent:**
- Purpose: Conversational trigger for domain-specific analysis
- Examples: `agents/ecoscore-analyzer.md`, `agents/gdpr-analyzer.md`
- Pattern: Markdown with YAML defining name, description, model, color, tools, plus trigger examples
- Detection: NLP matching on user intent based on examples in frontmatter
- Execution: Full system prompt + available tools + auto-loaded skills

**Skill:**
- Purpose: Domain knowledge base for enhanced analysis
- Examples: `skills/green-it-analysis/SKILL.md`, `skills/eu-compliance/SKILL.md`
- Pattern: SKILL.md contains frontmatter with trigger keywords + markdown methodology
- Composition: May include `references/` subdirectory with detailed docs
- Loading: Automatic when keywords in command/agent description match

**Hook:**
- Purpose: Pre/post-tool event handler for warnings or enforcement
- Examples: `hooks/hooks.json` with PreToolUse matchers for Write/Edit
- Pattern: JSON config with hooks array containing matcher, type ("prompt"), and timeout
- Execution: Runs prompt-based analysis, returns JSON with decision and message
- Pattern: Warn-only (always "allow" for permission, but may warn in systemMessage)

## Entry Points

**Marketplace Registration:**
- Location: `/.claude-plugin/marketplace.json`
- Triggers: Plugin discovery and installation via Claude Code
- Responsibilities: Register available plugins with paths, metadata, tags

**Plugin Commands:**
- Location: `plugins/<plugin-name>/commands/<commandname>.md`
- Triggers: `/pluginname:commandname [scope]` user invocation
- Responsibilities: Execute bounded analysis with explicit parameters, return structured output

**Agent Detection:**
- Location: `plugins/<plugin-name>/agents/<agentname>.md`
- Triggers: Natural language matching on user intent (evaluates examples)
- Responsibilities: Autonomously analyze context, load skills, provide domain-specific guidance

**Pre-Commit Hooks:**
- Location: `plugins/<plugin-name>/hooks/hooks.json`
- Triggers: When Write/Edit tools are used during code change
- Responsibilities: Detect anti-patterns, warn developer, never block (warn-only)

## Error Handling

**Strategy:** Fail-open with user guidance

**Patterns:**
- Commands: Return structured output with score + issues list; always include severity labels (critical, major, minor)
- Agents: Provide fallback guidance if full analysis fails; return partial results with confidence indicators
- Hooks: Never block on hook failure; treat hook errors as "allow" decision with no systemMessage
- Tools: Report missing allowed tools clearly; guide users to upgrade for premium features

## Cross-Cutting Concerns

**Logging:** Commands and agents provide detailed findings with file paths and line numbers (pattern: `filename.ext:line` format)

**Validation:** All findings categorized by severity (critical=3 points, major=2 points, minor=1 point) for consistent scoring

**Authentication:** Handled via `.claude-plugin/marketplace.json` owner email verification for marketplace access

**Scoping:** Commands use optional `$ARGUMENTS` to filter analysis scope (e.g., `/comply:scan gdpr` vs `/comply:scan csrd`)

---

*Architecture analysis: 2026-02-03*
