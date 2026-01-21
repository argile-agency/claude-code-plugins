# Argile Skills - Claude Code Plugins

Premium Claude Code plugins for professional workflows by [Argile Agency](https://argile.agency).

## Available Plugins

### ecoscore

Environmental impact analysis for sustainable software development based on Green IT principles.

**Features:**
- 9 analysis scopes: code efficiency, dependencies, data transfer, AI/LLM usage, build/CI-CD, frontend/UX, database, network, infrastructure
- Numeric scoring (0-100) with per-scope breakdown
- Prioritized actionable checklists with estimated impact
- AI usage analysis: token efficiency, model recommendations, caching opportunities
- Proactive green advisor on commit preparation

**Commands:**
- `/ecoscore:analyze` - Full codebase analysis with benchmarks
- `/ecoscore:quick-check` - Fast static-only scan
- `/ecoscore:report` - Generate prioritized improvement checklist

**Agents:**
- `ecoscore-analyzer` - Deep environmental impact analysis
- `green-advisor` - Reviews changes before commit

### comply

GDPR and CSRD compliance automation for European SaaS applications.

**Features:**
- PII detection and data flow mapping
- GDPR violation scanning (consent, retention, cross-border transfers)
- CSRD/ESRS sustainability reporting guidance
- Automated compliance checklists and remediation suggestions

**Commands:**
- `/comply:scan` - Scan codebase for compliance issues

**Agents:**
- `gdpr-analyzer` - Deep GDPR compliance analysis

## Installation

Install plugins from this marketplace using the Claude Code CLI:

```bash
# Install a specific plugin
claude /plugin https://github.com/argile-agency/claude-code-plugins ecoscore

# Or install from local path
claude /plugin /path/to/claude-code-plugins ecoscore
```

## Repository Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json    # Marketplace configuration
├── plugins/
│   ├── ecoscore/           # EcoScore plugin
│   │   ├── .claude-plugin/
│   │   ├── commands/
│   │   ├── agents/
│   │   ├── hooks/
│   │   └── skills/
│   └── comply/             # Comply plugin
│       ├── .claude-plugin/
│       ├── commands/
│       ├── agents/
│       ├── hooks/
│       └── skills/
├── LICENSE
└── README.md
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contact

- **Argile Agency**: [https://argile.agency](https://argile.agency)
- **Email**: aloha@argile.agency
