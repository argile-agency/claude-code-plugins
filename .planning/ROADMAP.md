# Roadmap: Token Tracking Plugin

## Overview

This roadmap delivers a Claude Code plugin that tracks token usage and estimates carbon emissions from AI-assisted development sessions. Starting with foundational tracking and carbon calculation, then adding visibility commands, and completing with comprehensive documentation to showcase sustainable agentic engineering practices.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation** - Token tracking, carbon formulas, and persistence
- [ ] **Phase 2: Visibility** - Commands for metrics display and cost correlation
- [ ] **Phase 3: Documentation** - README, methodology, and examples

## Phase Details

### Phase 1: Foundation
**Goal**: Token usage is tracked across sessions with carbon/energy estimates calculated
**Depends on**: Nothing (first phase)
**Requirements**: TOK-01, TOK-02, TOK-03, CARB-01, CARB-02, CARB-03, CARB-04
**Success Criteria** (what must be TRUE):
  1. Token counts are automatically captured from every API call (input and output tokens)
  2. Session metrics persist across Claude Code restarts and can be retrieved later
  3. Carbon emissions (grams CO2) are calculated from token usage using documented formulas
  4. Energy consumption (Wh) is estimated based on model type and token counts
  5. Regional carbon intensity factors are applied based on AWS region configuration
**Plans**: TBD

Plans:
- [ ] 01-01: TBD
- [ ] 01-02: TBD

### Phase 2: Visibility
**Goal**: Users can view token, carbon, and cost metrics on demand and at session completion
**Depends on**: Phase 1
**Requirements**: VIS-01, VIS-02, VIS-03, COST-01
**Success Criteria** (what must be TRUE):
  1. User can run a command to check current session metrics (tokens, CO2, energy)
  2. Session completion generates a summary report with full metrics breakdown
  3. Running totals display during multi-step workflows without manual commands
  4. Carbon and energy metrics show alongside estimated API costs for correlation
**Plans**: TBD

Plans:
- [ ] 02-01: TBD

### Phase 3: Documentation
**Goal**: Plugin purpose, methodology, and usage are clearly documented for external showcase
**Depends on**: Phase 2
**Requirements**: DOC-01, DOC-02, DOC-03
**Success Criteria** (what must be TRUE):
  1. README explains plugin purpose and value proposition for sustainable AI development
  2. Methodology documentation includes carbon estimation formulas with data sources cited
  3. Example outputs demonstrate realistic usage scenarios with sample metrics
  4. Accuracy disclaimers and estimation limitations are clearly stated
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/TBD | Not started | - |
| 2. Visibility | 0/TBD | Not started | - |
| 3. Documentation | 0/TBD | Not started | - |
