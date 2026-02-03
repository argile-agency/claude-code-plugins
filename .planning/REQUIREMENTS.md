# Requirements: Claude Code Plugin Marketplace

**Defined:** 2026-02-03
**Core Value:** Plugins that measure and optimize the environmental impact of AI-assisted development workflows

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Token Tracking

- [ ] **TOK-01**: Track input and output tokens per API call
- [ ] **TOK-02**: Aggregate token counts across session
- [ ] **TOK-03**: Persist metrics across sessions for historical tracking

### Carbon Estimation

- [ ] **CARB-01**: Estimate CO2 emissions (grams) from token usage
- [ ] **CARB-02**: Estimate energy consumption (Wh/kWh) from API calls
- [ ] **CARB-03**: Apply regional carbon intensity factors (AWS regions)
- [ ] **CARB-04**: Document estimation methodology with accuracy disclaimers

### Visibility

- [ ] **VIS-01**: Provide on-demand status command to check current session metrics
- [ ] **VIS-02**: Generate session summary report at workflow completion
- [ ] **VIS-03**: Display real-time running totals during execution

### Cost Correlation

- [ ] **COST-01**: Correlate carbon/energy metrics with estimated API costs

### Documentation

- [ ] **DOC-01**: Create README with clear explanation of plugin purpose
- [ ] **DOC-02**: Document methodology with formulas and data sources
- [ ] **DOC-03**: Include example outputs and usage scenarios

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advanced Attribution

- **ATTR-01**: Break down metrics by tool type (Read, Write, Bash, etc.)
- **ATTR-02**: Track which agent/subagent generated each request

### Advanced Features

- **ADV-01**: Set carbon/cost budget thresholds with alerts
- **ADV-02**: Provide optimization recommendations
- **ADV-03**: Compare efficiency across different models
- **ADV-04**: Export to carbon accounting platforms

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Carbon offsetting integration | Focus on measurement, not mitigation |
| Real-time grid intensity API | Complexity; static regional factors sufficient for v1 |
| Training emissions tracking | Out of user control; focus on inference only |
| Blocking/enforcement | Users will disable if intrusive; visibility-first approach |
| Gamification/social comparison | Can backfire; focus on actionable insights |
| Hardware-level profiling | API abstraction; no access to backend hardware |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| TOK-01 | Phase 1 | Pending |
| TOK-02 | Phase 1 | Pending |
| TOK-03 | Phase 1 | Pending |
| CARB-01 | Phase 1 | Pending |
| CARB-02 | Phase 1 | Pending |
| CARB-03 | Phase 1 | Pending |
| CARB-04 | Phase 1 | Pending |
| VIS-01 | Phase 2 | Pending |
| VIS-02 | Phase 2 | Pending |
| VIS-03 | Phase 2 | Pending |
| COST-01 | Phase 2 | Pending |
| DOC-01 | Phase 3 | Pending |
| DOC-02 | Phase 3 | Pending |
| DOC-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0

---
*Requirements defined: 2026-02-03*
*Last updated: 2026-02-03 after roadmap creation*
