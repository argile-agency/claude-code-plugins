# Claude Code Plugin Marketplace

## What This Is

A marketplace of Claude Code plugins for green IT and agentic software engineering, used internally at our agency and showcased externally to demonstrate expertise. The repository itself serves as the marketplace — plugins are discoverable and installable directly from this repo.

## Core Value

Plugins that measure and optimize the environmental impact of AI-assisted development workflows — making sustainable agentic engineering visible and actionable.

## Requirements

### Validated

- ✓ Plugin marketplace structure with commands, agents, hooks, skills — existing
- ✓ Ecoscore plugin for code environmental analysis (9 analysis scopes) — existing
- ✓ Comply plugin for GDPR/CSRD regulatory compliance — existing
- ✓ Markdown-based plugin system (no build step) — existing
- ✓ Event-driven hooks for pre/post tool validation — existing

### Active

- [ ] Track token usage across agentic workflow sessions
- [ ] Estimate carbon emissions (CO2) from Claude Code usage
- [ ] Estimate energy consumption (kWh) from API calls
- [ ] Correlate environmental impact with API costs
- [ ] Real-time visibility of metrics during execution
- [ ] Session summary reports at workflow completion
- [ ] On-demand impact check commands
- [ ] Clear documentation with examples for external showcase

### Out of Scope

- Website or web UI — repo is the marketplace
- User accounts or authentication — open source distribution
- Paid features or licensing — internal/showcase use only
- Mobile or desktop apps — CLI plugin only

## Context

**Agency context:** Used by our development team for sustainable AI development practices. Showcases our Green IT and agentic SE expertise to potential clients.

**Existing plugins:**
- `ecoscore`: Analyzes code for environmental impact across 9 scopes (code efficiency, dependencies, data transfer, AI/LLM usage, build/CI-CD, frontend/UX, database, network, infrastructure)
- `comply`: GDPR/CSRD compliance checking with PII detection

**Technical environment:**
- Claude Code plugin system (markdown-based, no build step)
- Python scripts for analysis utilities
- YAML frontmatter for command/agent metadata
- JSON for plugin manifests and hooks

## Constraints

- **Tech stack**: Must use Claude Code plugin architecture (markdown, YAML, JSON, Python scripts)
- **No external services**: Metrics estimation must work offline using formulas/models
- **Documentation first**: Clear README and examples required before external showcase

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Extend existing plugins vs new | Leverage ecoscore/comply foundation, avoid duplication | — Pending |
| Real-time + summary + on-demand | Users need multiple visibility touchpoints | — Pending |

---
*Last updated: 2026-02-03 after initialization*
