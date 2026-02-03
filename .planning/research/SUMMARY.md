# Research Summary: AI/LLM Environmental Impact Tracking

**Research Date:** 2026-02-03

## Key Findings

### Stack Recommendation
- **No external dependencies** — use inline JavaScript/Python for calculations
- **Token-to-energy formulas** — research-based estimates (0.05-2 Wh per 1K tokens depending on model)
- **Static carbon intensity data** — AWS region-specific values, update quarterly
- **Avoid**: CodeCarbon (Python-only, hardware-focused), real-time grid APIs (complexity), training calculators (wrong scope)

### Table Stakes Features
1. Token counting (input + output per tool call)
2. Basic carbon estimate (gCO2e)
3. Session totals
4. Per-tool attribution
5. Cost correlation ($/kWh/gCO2)

### Differentiators
- Real-time status display during execution
- Regional carbon factors (AWS regions vary 3-5x)
- Historical tracking across sessions
- Comparison benchmarks

### Architecture Approach
- **PostToolUse hooks** — capture token counts after each API call
- **File-based persistence** — store session data in `.ecoscore-session.json`
- **Commands** — `/ecoscore:status`, `/ecoscore:report`, `/ecoscore:reset`
- **Extend existing ecoscore plugin** — don't create new plugin

### Critical Pitfalls to Avoid
1. **Accuracy overconfidence** — estimates have ±50-100% margins, be transparent
2. **Stale emission factors** — version all data sources, update quarterly
3. **Ignoring regional variation** — Iceland (28g) vs Australia (820g) per kWh
4. **Guilt-tripping users** — neutral educational tone, optimization framing
5. **Performance overhead** — keep <50ms, async operations

## Build Order (Quick Depth)

**Phase 1: Foundation**
- Token counting hook (PostToolUse)
- Basic energy/carbon formulas
- Session state persistence

**Phase 2: Visibility**
- Real-time status command
- Session summary report
- On-demand check

**Phase 3: Documentation**
- README with methodology transparency
- Example outputs
- External showcase ready

## Sources
- Infrastructure-Aware Benchmarking (May 2025)
- CodeCarbon methodology
- Electricity Maps data
- AWS region carbon intensity reports

---
*Research completed: 2026-02-03*
