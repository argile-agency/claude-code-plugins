# EcoScore - Environmental Impact Analysis Plugin

Analyze codebases for environmental impact and sustainability using Green IT principles and carbon-aware practices.

## Features

- **Comprehensive Analysis**: 9 analysis scopes covering code, infrastructure, dependencies, and more
- **Numeric Scoring**: 0-100 EcoScore with per-scope breakdown
- **Actionable Checklists**: Prioritized improvements with estimated environmental impact
- **AI Usage Analysis**: Token efficiency, model recommendations, caching opportunities
- **Proactive Guidance**: Green advisor triggers on commit preparation

## Analysis Scopes

| Scope | What it analyzes |
|-------|------------------|
| Code efficiency | Algorithmic complexity, resource patterns, unnecessary computations |
| Infrastructure | Cloud sizing, server utilization, regional carbon intensity |
| Dependencies | Package bloat, unused deps, lightweight alternatives |
| Data transfer | API payloads, caching, compression |
| AI/LLM usage | Token consumption, model efficiency, prompt optimization |
| Build & CI/CD | Build times, test efficiency, artifact sizes |
| Frontend/UX | Image optimization, lazy loading, dark mode, DOM complexity |
| Database | Query efficiency, indexing, retention policies, storage |
| Network | CDN usage, edge computing, request batching, protocols |

## Commands

- `/ecoscore:analyze` - Full codebase analysis with benchmarks
- `/ecoscore:quick-check` - Fast static-only scan
- `/ecoscore:report` - Generate prioritized actionable checklist

## Agents

- **ecoscore-analyzer** - Deep analysis when you ask about environmental impact
- **green-advisor** - Reviews changes on commit preparation

## Configuration

Create `.claude/ecoscore.local.md` in your project to configure:

```yaml
---
# EcoScore Configuration
thresholds:
  overall: 70        # Minimum passing score (0-100)
  per_scope: 50      # Minimum per-scope score

enabled_scopes:
  - code_efficiency
  - dependencies
  - data_transfer
  - ai_usage
  - frontend
  - database
  - network
  - build_cicd
  - infrastructure

output_format: checklist  # checklist | detailed | json

carbon_region: europe-west  # For carbon intensity calculations

custom_rules: []  # Add project-specific rules
---

# Project-specific notes
Add any project context that affects environmental analysis here.
```

## Installation

```bash
# From marketplace
claude /plugin ecoscore

# Or clone and install locally
claude --plugin-dir /path/to/ecoscore
```

## License

MIT
