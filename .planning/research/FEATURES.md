# FEATURES.md - AI/LLM Environmental Impact Tracking Features

## Research Date: 2026-02-03

## Overview

This document defines the feature set for tracking environmental impact of AI/LLM usage within Claude Code plugins, focusing on what makes a compelling, honest, and useful tool for developers.

## Table Stakes (Must-Have Features)

### 1. Token Counting

**Description**: Accurate tracking of input and output tokens per API call

**Requirements**:
- Extract token counts from Anthropic API response metadata
- Track both prompt tokens (input) and completion tokens (output)
- Accumulate totals per session
- Handle both streaming and non-streaming responses

**Complexity**: Low
- API already returns token counts
- Simple arithmetic aggregation
- No external dependencies

**Data Tracked**:
```javascript
{
  inputTokens: 1234,
  outputTokens: 567,
  totalTokens: 1801,
  timestamp: "2026-02-03T15:30:00Z",
  model: "claude-sonnet-4-5-20250929"
}
```

### 2. Basic Carbon Estimate

**Description**: Rough CO2 emissions estimate based on token usage

**Requirements**:
- Token-to-energy conversion factors per model class
- Regional carbon intensity (AWS region-based)
- PUE multiplier (datacenter efficiency)
- Clear disclaimer about estimate accuracy

**Complexity**: Medium
- Requires research-based conversion factors
- Static carbon intensity data (updated quarterly)
- Transparent about ±50-100% margin of error

**Formula**:
```javascript
// Energy estimation
const inputEnergyWh = (inputTokens / 1000) * MODEL_INPUT_FACTOR;
const outputEnergyWh = (outputTokens / 1000) * MODEL_OUTPUT_FACTOR;
const totalEnergyWh = inputEnergyWh + outputEnergyWh;

// Carbon estimation
const energyKWh = totalEnergyWh / 1000;
const carbonGrams = energyKWh * CARBON_INTENSITY_G_PER_KWH * PUE;
```

**Model Factors** (Wh per 1K tokens):
- Claude Opus 4/4.5: Input 1.2, Output 1.5
- Claude Sonnet 3.5/4.5: Input 0.5, Output 0.7
- Claude Haiku 3/3.5: Input 0.1, Output 0.15

**Default Values**:
- PUE: 1.2 (modern AWS datacenter)
- Carbon Intensity: 400 gCO2/kWh (US average) or region-specific

### 3. Session Totals

**Description**: Aggregate metrics for current Claude Code session

**Requirements**:
- Running totals updated after each API call
- Persistent across tool invocations within session
- Reset on session end or manual reset command

**Metrics Tracked**:
- Total tokens (input + output)
- Total energy (Wh)
- Total carbon (gCO2)
- Total cost ($)
- Number of API calls
- Session duration
- Models used

**Complexity**: Low
- In-memory state management
- Simple aggregation logic

**Display Format**:
```
📊 Session Impact Summary
========================
Tokens:     45,234 (31,456 in / 13,778 out)
Energy:     22.5 Wh (0.0225 kWh)
Carbon:     9.0 gCO2e (~0.009 kg)
Cost:       $1.23
API Calls:  12
Duration:   18m 34s
Models:     claude-sonnet-4-5 (10), claude-opus-4-5 (2)
```

### 4. Per-Tool Attribution

**Description**: Break down impact by Claude Code tool/command used

**Requirements**:
- Tag each API call with originating tool (Bash, Read, Write, Grep, etc.)
- Aggregate by tool type
- Show which tools consume most resources

**Complexity**: Medium
- Requires integration with Claude Code's internal tool tracking
- May need custom hook to capture tool context

**Use Case**:
- Identify high-impact workflows (e.g., "iterative code editing")
- Optimize tool usage patterns
- Educate users on environmental cost of different operations

**Display**:
```
🔧 Impact by Tool
=================
Read:   5,234 tokens  →  2.1 gCO2  →  $0.15
Bash:   12,456 tokens →  5.0 gCO2  →  $0.38
Grep:   8,901 tokens  →  3.6 gCO2  →  $0.27
Write:  3,445 tokens  →  1.4 gCO2  →  $0.10
```

### 5. Cost Correlation

**Description**: Show monetary cost alongside environmental cost

**Requirements**:
- Up-to-date Anthropic API pricing (per model, per 1M tokens)
- Calculate cost per API call and cumulative
- Display cost and carbon side-by-side

**Pricing Table** (as of 2026-02-03):
| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Opus 4.5 | $15.00 | $75.00 |
| Claude Sonnet 4.5 | $3.00 | $15.00 |
| Claude Haiku 3.5 | $0.80 | $4.00 |

**Complexity**: Low
- Static pricing table (updated manually)
- Simple multiplication

**Rationale**:
- Money is tangible, makes carbon relatable
- "This prompt cost $0.50 and 20g CO2"
- Encourages efficiency for both financial and environmental reasons

## Differentiators (Nice-to-Have Features)

### 1. Real-Time Display in UI

**Description**: Live-updating dashboard showing impact as work progresses

**Requirements**:
- Claude Code UI integration (if API available)
- Status bar or sidebar widget
- Update frequency: after each API call

**Display Elements**:
- Current session totals
- Last API call impact
- Trend indicator (impact increasing/decreasing)

**Complexity**: High
- Requires Claude Code plugin UI capabilities (may not exist yet)
- Persistent rendering in terminal
- Non-intrusive display

**Fallback**: Post-session summary command

### 2. Regional Carbon Factors

**Description**: Use actual AWS region carbon intensity instead of global average

**Requirements**:
- Map Anthropic API endpoint to AWS region
- Static table of regional carbon intensity values
- Auto-detect or manual region selection

**Regional Data** (gCO2/kWh):
- us-east-1 (Virginia): 340
- us-west-2 (Oregon): 250 (high hydro)
- eu-west-1 (Ireland): 280
- ap-southeast-1 (Singapore): 420
- Global Average: 475

**Complexity**: Medium
- Requires region detection logic
- Quarterly data updates

**Impact**: 30-50% accuracy improvement over global average

### 3. Comparison Benchmarks

**Description**: Contextualize carbon emissions with everyday comparisons

**Examples**:
- "This session = driving a car 0.05 miles"
- "This session = charging a smartphone 3 times"
- "This session = 15 minutes of streaming video"

**Conversion Factors**:
- Driving: ~400 gCO2/mile (average gas car)
- Smartphone charge: ~3 gCO2 (15Wh × 0.2 kg/kWh)
- Streaming video: ~0.5 gCO2/minute (Netflix 1080p)
- Google search: ~0.2 gCO2 per search

**Complexity**: Low
- Simple division/multiplication
- Static conversion factors

**Rationale**: Make abstract numbers tangible

**Caution**: Avoid guilt-tripping or alarmism

### 4. Historical Tracking

**Description**: Persist session data across days/weeks/months

**Requirements**:
- File-based storage (JSON or SQLite)
- Privacy-respecting (local only, no cloud upload)
- Aggregation by day, week, month
- Trend analysis (usage increasing/decreasing)

**Storage Location**:
- `~/.claude/impact-history.json` or
- `.claude/plugin-name.local.md` (per project)

**Complexity**: Medium
- File I/O from plugin hooks
- Date/time handling
- Aggregation logic

**Display**:
```
📈 Historical Impact (Last 30 Days)
===================================
Week 1:  1,234 tokens  →  0.5 gCO2  →  $0.37
Week 2:  2,345 tokens  →  0.9 gCO2  →  $0.68  ⬆ 89%
Week 3:  1,890 tokens  →  0.7 gCO2  →  $0.55  ⬇ 19%
Week 4:  3,456 tokens  →  1.4 gCO2  →  $0.99  ⬆ 82%
```

### 5. Model Efficiency Comparison

**Description**: Show which Claude models are most energy-efficient

**Requirements**:
- Track tokens-per-task across models
- Calculate efficiency ratio (task completion / emissions)
- Recommend model switching when appropriate

**Example**:
```
💡 Model Efficiency Insight
===========================
You used Opus for this task (45 gCO2, $1.20)
Sonnet could have done it for ~18 gCO2, $0.48
Consider using Sonnet for similar tasks
```

**Complexity**: High
- Requires task classification (simple vs. complex)
- Heuristics for model recommendation
- Avoid nagging users about model choice

**Ethical Consideration**:
- Don't shame users for using powerful models
- Frame as optimization opportunity, not wasteful behavior

### 6. Carbon Budget Mode

**Description**: Set a carbon budget and get warnings when approaching limit

**Requirements**:
- User-defined budget (e.g., "100 gCO2 per day")
- Warnings at 75%, 90%, 100%
- Suggest efficiency improvements when near limit

**Configuration**:
```yaml
# .claude/impact-tracker.local.md
---
daily_carbon_budget_g: 100
weekly_carbon_budget_g: 500
notify_at_percent: [75, 90, 100]
pause_at_limit: false
---
```

**Complexity**: Medium
- Requires persistent storage
- Time-based reset logic
- Non-blocking warnings

**Use Case**:
- Personal carbon accountability
- Organizational sustainability goals
- Educational tool for students

## Anti-Features (What NOT to Build)

### ❌ Offset Purchasing Integration

**Why NOT**:
- Carbon offsets are controversial and often ineffective
- Creates false sense of absolution
- Plugin should focus on reduction, not offsetting
- Legal/financial complications

**Alternative**:
- Link to third-party offset providers
- Educational content about offset limitations

### ❌ Real-Time Grid Carbon Intensity

**Why NOT**:
- Requires API calls to Electricity Maps or similar (latency, cost, reliability)
- No control over Anthropic's datacenter selection
- False precision (user can't influence which datacenter serves their request)
- Complexity >> value

**Alternative**: Use static regional averages (good enough)

### ❌ Embodied Carbon Tracking

**Why NOT**:
- Amortized over billions of API calls
- Manufacturing emissions are <5% of operational for LLM inference
- No public data for Anthropic's hardware lifecycle
- Creates clutter without actionable insights

**Alternative**: Mention in documentation, exclude from real-time metrics

### ❌ Gamification / Leaderboards

**Why NOT**:
- Encourages competition, not mindfulness
- Privacy concerns (even if anonymous)
- Can backfire (race to bottom = less AI usage = worse productivity)
- Misaligned incentives (using less AI isn't always better)

**Alternative**: Personal goals and trends only

### ❌ Blocking / Limiting API Usage

**Why NOT**:
- Breaks user workflow
- Paternalistic and annoying
- Developer will disable plugin
- Carbon budget should be advisory, not enforced

**Alternative**: Warnings and suggestions, user maintains control

### ❌ Water Usage Tracking

**Why NOT**:
- Highly datacenter-specific (evaporative cooling vs. air cooling)
- No public data for AWS facilities
- Regional water stress is complex (can't use global averages)
- Scope creep for v1

**Alternative**: Consider for v2 if data becomes available

### ❌ Exaggerated Comparisons

**Examples to AVOID**:
- "This session = melting 5 ice cubes" (technically true but silly)
- "This session = killing 0.0001 polar bears" (offensive)
- "This session = destroying rainforest the size of a postage stamp" (alarmist)

**Why NOT**:
- Guilt-tripping is counterproductive
- Trivializes real environmental issues
- Users will ignore/mock the plugin

**Alternative**: Straightforward comparisons (miles driven, phone charges)

### ❌ Fake Precision

**Examples to AVOID**:
- "Your session emitted 8.734521 grams of CO2"
- "Carbon footprint accurate to ±2%"
- "Certified carbon accounting"

**Why NOT**:
- Estimates have ±50-100% margin of error
- Overstates confidence in methodology
- Could be used for greenwashing

**Alternative**:
- Round to 1-2 significant figures
- Always include disclaimer
- Use "~" prefix (e.g., "~9 gCO2")

## Complexity Assessment

### Low Complexity (1-2 days)
- Token counting
- Session totals
- Cost correlation
- Comparison benchmarks

### Medium Complexity (3-5 days)
- Basic carbon estimate
- Per-tool attribution
- Regional carbon factors
- Historical tracking

### High Complexity (1-2 weeks)
- Real-time UI display
- Model efficiency comparison
- Carbon budget mode
- Trend analysis and insights

## Feature Prioritization

### Phase 1 (MVP - 1 week)
1. Token counting
2. Basic carbon estimate
3. Session totals
4. Cost correlation

### Phase 2 (Enhancement - 1 week)
5. Per-tool attribution
6. Regional carbon factors
7. Comparison benchmarks

### Phase 3 (Advanced - 2 weeks)
8. Historical tracking
9. Model efficiency comparison
10. Carbon budget mode

### Phase 4 (Polish)
11. Real-time UI (if Claude Code supports)
12. Export reports
13. Integration with ecoscore plugin

## Success Metrics

### Adoption
- Downloads/installs (if marketplace tracks)
- Active users (session history file creation)

### Engagement
- Commands invoked per user
- Session history retention (users keeping it enabled)

### Impact
- User feedback mentioning behavior change
- Integration with other environmental tools

### Education
- Documentation page views
- User questions about methodology (good sign of engagement)

## User Experience Principles

### 1. Non-Intrusive
- Don't interrupt workflow with warnings/popups
- Display only when user requests (command) or at session end
- Quiet by default, vocal when asked

### 2. Honest
- Clear about estimation uncertainty
- Don't claim precision we don't have
- Cite sources and methodology

### 3. Actionable
- Show what user can do to reduce impact
- Suggest model switching when appropriate
- Link to energy-efficient coding practices

### 4. Respectful
- Don't guilt-trip or shame
- Frame as optimization, not moral failing
- Acknowledge trade-offs (speed vs. efficiency)

### 5. Transparent
- Open-source methodology
- Document assumptions
- Allow user to verify/customize conversion factors

## References

### User Research
- [World Economic Forum: How to cut the environmental impact of your company's AI use (June 2025)](https://www.weforum.org/stories/2025/06/how-ai-use-impacts-the-environment/)
- [PwC: The environmental impact of AI and how to mitigate it (2025)](https://www.pwc.be/en/news-publications/2025/responsible-ai-environmental-impact.html)

### Best Practices
- [UNEP: AI has an environmental problem. Here's what the world can do about that.](https://www.unep.org/news-and-stories/story/ai-has-environmental-problem-heres-what-world-can-do-about)
- [EAB: AI's environmental impact can't be ignored. What can higher ed do?](https://eab.com/resources/blog/strategy-blog/ais-environmental-impact-higher-ed/)

### Technical Implementation
- See STACK.md for methodologies
- See ARCHITECTURE.md for Claude Code integration
