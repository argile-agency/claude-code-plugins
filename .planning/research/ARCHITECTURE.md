# ARCHITECTURE.md - Claude Code Plugin Integration Architecture

## Research Date: 2026-02-03

## Overview

This document outlines the architecture for integrating AI/LLM environmental impact tracking into the Claude Code plugin system, detailing components, data flow, and build order.

## Claude Code Plugin System Recap

### Available Components

1. **Commands** (`/commands/*.md`): User-invocable via `/plugin:command`
2. **Agents** (`/agents/*.md`): Background processors triggered by natural language
3. **Hooks** (`/hooks/hooks.json`): Event-driven prompts (PreToolUse, PostToolUse, etc.)
4. **Skills** (`/skills/SKILL.md`): Knowledge bases loaded when relevant

### Constraints

- **No Build Step**: Markdown-based, no npm packages or dependencies
- **No External APIs**: Can't call Electricity Maps, CodeCarbon API, etc.
- **Limited State**: No built-in database, must use file system
- **Bash Execution**: Can run shell commands for calculations

## Architecture Components

### 1. Data Collection Layer (Hooks)

**Component**: `hooks/hooks.json` with PostToolUse hook

**Purpose**: Intercept Anthropic API responses to extract token counts

**Hook Configuration**:
```json
{
  "hooks": [
    {
      "name": "track-api-usage",
      "event": "PostToolUse",
      "matcher": {
        "tool": ["*"]
      },
      "prompt": "Extract token usage from the last API response and update session totals. Record: input_tokens, output_tokens, model_name, timestamp. Update in-memory session state."
    }
  ]
}
```

**Data Captured**:
```javascript
{
  "timestamp": "2026-02-03T15:30:00Z",
  "tool_used": "Read",
  "model": "claude-sonnet-4-5-20250929",
  "input_tokens": 1234,
  "output_tokens": 567,
  "total_tokens": 1801
}
```

**Challenges**:
- Access to API response metadata (may require Claude Code API)
- In-memory state persistence between tool calls
- Detecting session start/end

**Alternative**: PreToolUse hook to count input tokens, PostToolUse for output

### 2. Calculation Engine (Scripts)

**Component**: Inline JavaScript/bash in hooks or commands

**Purpose**: Convert token counts to energy, carbon, and cost

**Implementation Options**:

#### Option A: Inline JavaScript in Hook Prompt
```markdown
When PostToolUse event fires, execute this calculation:

const MODEL_FACTORS = {
  'claude-opus-4-5': { input_wh: 1.2, output_wh: 1.5 },
  'claude-sonnet-4-5': { input_wh: 0.5, output_wh: 0.7 },
  'claude-haiku-3-5': { input_wh: 0.1, output_wh: 0.15 }
};

const PUE = 1.2;
const CARBON_INTENSITY_G_PER_KWH = 400;

function calculateImpact(inputTokens, outputTokens, model) {
  const factors = MODEL_FACTORS[model] || MODEL_FACTORS['claude-sonnet-4-5'];

  const inputEnergyWh = (inputTokens / 1000) * factors.input_wh;
  const outputEnergyWh = (outputTokens / 1000) * factors.output_wh;
  const totalEnergyWh = inputEnergyWh + outputEnergyWh;

  const energyKWh = totalEnergyWh / 1000;
  const carbonG = energyKWh * CARBON_INTENSITY_G_PER_KWH * PUE;

  return { energyWh: totalEnergyWh, carbonG: carbonG };
}
```

#### Option B: Bash Script with bc Calculator
```bash
# calculate-impact.sh
INPUT_TOKENS=$1
OUTPUT_TOKENS=$2
MODEL=$3

# Model factors (Wh per 1K tokens)
case $MODEL in
  *opus*) INPUT_FACTOR=1.2; OUTPUT_FACTOR=1.5 ;;
  *sonnet*) INPUT_FACTOR=0.5; OUTPUT_FACTOR=0.7 ;;
  *haiku*) INPUT_FACTOR=0.1; OUTPUT_FACTOR=0.15 ;;
  *) INPUT_FACTOR=0.5; OUTPUT_FACTOR=0.7 ;;
esac

# Constants
PUE=1.2
CARBON_INTENSITY=400

# Energy calculation
INPUT_ENERGY=$(echo "scale=4; $INPUT_TOKENS / 1000 * $INPUT_FACTOR" | bc)
OUTPUT_ENERGY=$(echo "scale=4; $OUTPUT_TOKENS / 1000 * $OUTPUT_FACTOR" | bc)
TOTAL_ENERGY=$(echo "scale=4; $INPUT_ENERGY + $OUTPUT_ENERGY" | bc)

# Carbon calculation
ENERGY_KWH=$(echo "scale=6; $TOTAL_ENERGY / 1000" | bc)
CARBON_G=$(echo "scale=2; $ENERGY_KWH * $CARBON_INTENSITY * $PUE" | bc)

echo "energy_wh=$TOTAL_ENERGY"
echo "carbon_g=$CARBON_G"
```

**Recommended**: Option A (inline) for simplicity, Option B if Claude Code supports script files

### 3. State Management (File Persistence)

**Component**: `.claude/impact-tracker.local.md`

**Purpose**: Store session and historical data

**Format**:
```markdown
---
# Session State (in-memory, written on session end)
session_start: "2026-02-03T15:00:00Z"
session_id: "abc123"
total_input_tokens: 45234
total_output_tokens: 13778
total_energy_wh: 22.5
total_carbon_g: 9.0
total_cost_usd: 1.23
api_calls: 12
models_used:
  - name: "claude-sonnet-4-5"
    calls: 10
  - name: "claude-opus-4-5"
    calls: 2

# Historical Data (accumulated across sessions)
history:
  - date: "2026-02-03"
    tokens: 59012
    carbon_g: 9.0
    cost_usd: 1.23
  - date: "2026-02-02"
    tokens: 42345
    carbon_g: 6.8
    cost_usd: 0.89
---

# Impact Tracker Settings

Carbon intensity: 400 gCO2/kWh (US average)
PUE multiplier: 1.2
Daily budget: None
```

**Operations**:
- **Read on session start**: Load previous session totals
- **Write on session end**: Persist session data to history
- **Append on demand**: When user invokes `/impact:save` command

**Challenges**:
- Detecting session start/end (may need SessionStart/SessionEnd hooks)
- Concurrent access (multiple Claude instances?)
- File size growth (implement rotation/pruning)

### 4. Display Layer (Commands)

**Component**: `commands/*.md` files

**Commands to Implement**:

#### `/impact:status`
Show current session totals in real-time

```markdown
---
description: "Show current session environmental impact"
allowed-tools: ["Read"]
---

# Impact Status Command

Read `.claude/impact-tracker.local.md` and display:

📊 Current Session Impact
========================
Tokens:     45,234 (31,456 in / 13,778 out)
Energy:     22.5 Wh (0.0225 kWh)
Carbon:     ~9 gCO2e
Cost:       $1.23
API Calls:  12
Duration:   18m 34s
Models:     claude-sonnet-4-5 (10), claude-opus-4-5 (2)

💡 Context: This session = charging a smartphone ~3 times
⚠️  Estimate accuracy: ±50-100% (see /impact:methodology)
```

#### `/impact:report`
Generate detailed breakdown by tool, model, time period

```markdown
---
description: "Generate detailed environmental impact report"
allowed-tools: ["Read", "Write"]
argument-hint: "[daily|weekly|monthly]"
---

# Impact Report Command

Arguments: $1 = time period (default: daily)

Generate report with:
1. Session totals
2. Per-tool breakdown
3. Per-model comparison
4. Historical trends (if period specified)
5. Efficiency recommendations

Output format: Markdown table + charts (ASCII art)
Save to: `.claude/impact-report-YYYY-MM-DD.md`
```

#### `/impact:methodology`
Explain calculation methodology and data sources

```markdown
---
description: "Explain how environmental impact is calculated"
allowed-tools: []
---

# Impact Methodology

Display:
1. Token-to-energy conversion factors (with sources)
2. Carbon intensity values (regional breakdown)
3. PUE assumptions
4. Accuracy expectations (±50-100%)
5. What's included/excluded (operational only, no embodied carbon)
6. Links to research papers and tools (STACK.md sources)
```

#### `/impact:reset`
Reset session totals (for testing or manual session boundaries)

```markdown
---
description: "Reset current session impact counters"
allowed-tools: ["Write"]
---

# Impact Reset Command

Prompt user for confirmation, then:
1. Save current session to history
2. Zero out session counters
3. Set new session_start timestamp
4. Display confirmation
```

#### `/impact:configure`
Update settings (carbon intensity, PUE, budget)

```markdown
---
description: "Configure impact tracking settings"
allowed-tools: ["Edit"]
argument-hint: "[setting] [value]"
---

# Impact Configure Command

Settings:
- carbon_intensity: gCO2/kWh (default: 400)
- pue: Power Usage Effectiveness (default: 1.2)
- daily_budget_g: Daily carbon budget in grams (default: none)
- region: AWS region for regional carbon factors (default: us-east-1)

Example: /impact:configure carbon_intensity 250
```

### 5. Knowledge Layer (Skills)

**Component**: `skills/SKILL.md`

**Purpose**: Provide context when user asks about environmental impact

**Skill Trigger**: Natural language queries like:
- "How much energy am I using?"
- "What's the carbon footprint of this session?"
- "How can I reduce my AI environmental impact?"

**Skill Content**:
```markdown
# Environmental Impact Tracking Skill

When the user asks about environmental impact, energy usage, carbon footprint, or sustainability of their Claude Code session:

1. Check if impact tracking is enabled (`.claude/impact-tracker.local.md` exists)
2. If yes, invoke `/impact:status` to show current data
3. If no, explain the plugin and how to enable it
4. Provide actionable tips:
   - Use Sonnet instead of Opus for routine tasks
   - Batch operations to reduce API calls
   - Review ecoscore plugin for code-level optimization
   - Consider regional carbon intensity differences

## References

See `references/methodology.md` for detailed calculation explanations
See `references/research-papers.md` for academic sources
See `references/optimization-tips.md` for reducing environmental impact
```

### 6. Background Agent (Optional)

**Component**: `agents/impact-advisor.md`

**Purpose**: Proactively suggest efficiency improvements

**Agent Configuration**:
```markdown
---
name: "Impact Advisor"
description: "Suggests ways to reduce environmental impact of AI usage"
model: "claude-haiku-3-5"
color: "green"
tools: ["Read"]
autonomous: false
---

# Impact Advisor Agent

Triggered when:
- User completes a high-impact operation (>5 gCO2)
- User approaches carbon budget limit (if set)
- User uses Opus when Sonnet would suffice

Suggestions:
- "Consider using Sonnet for this type of task (3x more efficient)"
- "Batching these operations could reduce API calls by 40%"
- "This session is 2x higher impact than average, review /impact:report"

Tone: Helpful, not nagging. Provide suggestions 1-2 times per session max.
```

**Caution**: Don't over-trigger, avoid annoying users

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ User Interaction (Claude Code CLI)                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Claude Code Tool Execution (Read, Bash, Grep, etc.)        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Anthropic API Call (User's request → Claude Model)         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ PostToolUse Hook (impact-tracker plugin)                   │
│  - Extract: input_tokens, output_tokens, model             │
│  - Trigger: Calculation Engine                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Calculation Engine (inline JS or bash script)              │
│  - Input: Token counts + model + settings                  │
│  - Output: Energy (Wh), Carbon (gCO2), Cost ($)            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ State Management (in-memory session object)                │
│  - Accumulate: Totals, per-tool, per-model                 │
│  - Update: Session timestamp, API call count               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├─────────────► On session end ────────────┐
                 │                                           │
                 ▼                                           ▼
┌───────────────────────────────┐        ┌──────────────────────────────┐
│ User Invokes Command          │        │ File Persistence             │
│  - /impact:status             │        │  .claude/impact-tracker.     │
│  - /impact:report             │        │  local.md                    │
│  - /impact:methodology        │        │   - Append to history[]      │
└────────────────┬──────────────┘        │   - Zero session counters    │
                 │                        └──────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ Display Layer (formatted output)                           │
│  - Current session totals                                  │
│  - Historical trends                                       │
│  - Comparisons and context                                 │
│  - Methodology explanations                                │
└─────────────────────────────────────────────────────────────┘
```

## Integration with Existing Components

### With Commands
- **Read**: Track token usage when reading large files
- **Write**: Track token usage when generating/editing files
- **Bash**: Track token usage for command execution and parsing
- **Grep**: Track token usage for search result processing

**Implementation**: PostToolUse hook captures all tool invocations automatically

### With Agents
- **ecoscore-analyzer**: Correlate code environmental impact with AI usage impact
- **green-advisor**: Extend to suggest AI usage optimization

**Example Integration**:
```markdown
# In ecoscore's green-advisor agent

When providing recommendations, also invoke /impact:status to show:

"Your code has an ecoscore of 75/100, consuming ~50 kWh/year in production.
This analysis session itself used 12 Wh and emitted ~5 gCO2.
Consider both code efficiency AND analysis tool efficiency."
```

### With Hooks
- **PreToolUse**: Warn if approaching carbon budget before executing expensive operation
- **PostToolUse**: Track and accumulate impact data (primary integration point)
- **SessionStart**: Initialize session state, load settings
- **SessionEnd**: Persist session data to history, display summary

**Example SessionEnd Hook**:
```json
{
  "name": "session-end-summary",
  "event": "SessionEnd",
  "prompt": "Display session environmental impact summary using /impact:status. Thank user for being mindful of AI sustainability."
}
```

### With Skills
- **ecoscore**: Cross-reference code analysis with AI analysis impact
- **compliance (GDPR/CSRD)**: Note that carbon tracking may be required for CSRD reporting

**Skill Reference**:
```markdown
# In comply plugin SKILL.md

CSRD (Corporate Sustainability Reporting Directive) requires:
- Scope 3 emissions including purchased cloud services
- AI/LLM usage falls under "purchased cloud computing"
- Use impact-tracker plugin to measure and report AI emissions
```

## Build Order

### Phase 1: Foundation (Week 1)
**Goal**: Basic tracking and display

1. **Day 1-2**: Hook setup
   - Create `hooks/hooks.json` with PostToolUse hook
   - Test token extraction from API responses
   - Implement in-memory session state

2. **Day 3-4**: Calculation engine
   - Implement token-to-energy conversion
   - Add carbon and cost calculations
   - Write unit tests (if possible in plugin framework)

3. **Day 5**: Commands - Status
   - Create `/impact:status` command
   - Display current session totals
   - Add comparison benchmarks

4. **Day 6**: File persistence
   - Create `.claude/impact-tracker.local.md` format
   - Implement session save/load
   - Add SessionEnd hook for auto-save

5. **Day 7**: Testing and documentation
   - End-to-end testing in Claude Code
   - Write user-facing README
   - Document methodology

### Phase 2: Enhancement (Week 2)
**Goal**: Per-tool attribution and historical tracking

1. **Day 8-9**: Per-tool attribution
   - Enhance hook to capture tool name
   - Aggregate by tool type
   - Display in `/impact:status`

2. **Day 10-11**: Historical tracking
   - Implement history[] accumulation
   - Add date-based aggregation
   - Create `/impact:report` command with trends

3. **Day 12-13**: Regional factors
   - Add region detection/configuration
   - Create regional carbon intensity table
   - Implement in calculation engine

4. **Day 14**: Command suite completion
   - Create `/impact:methodology`
   - Create `/impact:reset`
   - Create `/impact:configure`

### Phase 3: Advanced (Week 3-4)
**Goal**: Model comparison, budget mode, agent integration

1. **Day 15-17**: Model efficiency comparison
   - Track per-model metrics
   - Implement efficiency heuristics
   - Add recommendations to `/impact:report`

2. **Day 18-20**: Carbon budget mode
   - Add budget configuration
   - Implement warning logic (75%, 90%, 100%)
   - Create PreToolUse budget check hook

3. **Day 21-23**: Impact advisor agent
   - Create agent with efficiency suggestions
   - Implement trigger logic (high-impact operations)
   - Test autonomous vs. on-demand invocation

4. **Day 24-25**: Ecoscore integration
   - Cross-reference with ecoscore plugin
   - Unified environmental dashboard
   - Combined recommendations

5. **Day 26-28**: Polish and optimization
   - Performance testing (hook overhead)
   - UI/UX refinement
   - Edge case handling

### Phase 4: Launch (Week 5)
1. **Day 29**: Beta testing with users
2. **Day 30**: Bug fixes and feedback incorporation
3. **Day 31**: Documentation finalization
4. **Day 32**: Marketplace submission
5. **Day 33-35**: Marketing and community engagement

## Technical Challenges and Solutions

### Challenge 1: Accessing API Response Metadata

**Problem**: Hook may not have direct access to Anthropic API response headers/metadata

**Solutions**:
1. **Claude Code API**: Check if plugin API exposes token counts
2. **Response Parsing**: Parse response text for token info (if included)
3. **Estimation**: Fallback to token estimation from prompt/completion text length

**Recommendation**: Start with solution 1, fall back to 3 if necessary

### Challenge 2: Session State Persistence

**Problem**: Hooks are stateless, need to maintain running totals

**Solutions**:
1. **In-Memory Object**: If Claude Code maintains plugin state between tool calls
2. **File Read/Write**: Read state file before calculation, write after
3. **Environment Variables**: Export session state to env vars (fragile)

**Recommendation**: Solution 2 (file-based) is most reliable

### Challenge 3: Hook Performance Overhead

**Problem**: PostToolUse hook on every tool call could slow down workflow

**Solutions**:
1. **Async Processing**: Don't block tool return on impact calculation
2. **Batching**: Accumulate data, calculate every N calls
3. **Lightweight Calculation**: Keep math simple, no external calls

**Recommendation**: Solution 1 + 3 (async + simple math)

### Challenge 4: Regional Carbon Intensity Accuracy

**Problem**: No way to know which AWS region served the API request

**Solutions**:
1. **User Configuration**: Let user specify their region
2. **IP Geolocation**: Infer region from user's IP (privacy concerns)
3. **Conservative Estimate**: Use highest-carbon region (encourages efficiency)
4. **Average**: Use US average or global average

**Recommendation**: Solution 1 (user config) with solution 4 (average) as default

### Challenge 5: Model Detection

**Problem**: API response may not always include model name

**Solutions**:
1. **Request Parsing**: Extract model from user's request (if specified)
2. **Default Assumption**: Assume Sonnet if not specified
3. **Claude Code Context**: Access internal tool call metadata

**Recommendation**: Solution 3 if available, else solution 2

## Testing Strategy

### Unit Tests
- Token-to-energy conversion accuracy
- Carbon calculation with various inputs
- Cost calculation across models
- Date/time aggregation logic

### Integration Tests
- Hook triggers on tool execution
- Session state persists across commands
- File read/write operations succeed
- Commands display correct data

### End-to-End Tests
- Complete session: start → multiple tools → status → end
- Historical tracking across multiple days
- Budget mode warnings trigger correctly
- Agent suggestions appear appropriately

### Performance Tests
- Hook overhead latency (<50ms target)
- File I/O performance with large history
- Memory usage for long-running sessions

## Deployment Considerations

### Plugin Distribution
- Include all components in single `.zip` or repo
- Provide installation instructions
- Test on Windows, macOS, Linux

### Versioning
- Semantic versioning (1.0.0, 1.1.0, etc.)
- Changelog for each release
- Backward compatibility for state files

### Updates
- Quarterly carbon intensity data refresh
- Model factor updates as new models release
- Methodology improvements based on research

### Support
- GitHub Issues for bug reports
- Documentation wiki for FAQs
- Community Discord for discussion

## Future Enhancements (Post-Launch)

### Integration Opportunities
- **VS Code Extension**: Real-time dashboard in IDE
- **GitHub Actions**: Track CI/CD AI usage
- **Slack Bot**: Daily/weekly impact reports
- **Carbon Offset APIs**: Optional offset purchasing

### Advanced Features
- **Team Dashboards**: Aggregate across organization
- **ML Model**: Predict impact before execution
- **Benchmark Database**: Compare against community averages
- **Real-Time Grid**: If Anthropic publishes datacenter selection logic

### Research Improvements
- **Anthropic Partnership**: Request actual per-token energy data
- **Hardware Updates**: Track GPU generation improvements
- **Measurement Validation**: Compare estimates to metered data (if available)

## References

### Claude Code Plugin Development
- See `CLAUDE.md` in repository root
- See `AGENTS.md` for agent development guidelines
- See existing plugins (ecoscore, comply) for patterns

### Environmental Impact Research
- See `STACK.md` for methodologies and tools
- See `FEATURES.md` for feature definitions
- See `PITFALLS.md` for common mistakes

### Academic Sources
- LLMCarbon: Modeling the end-to-end Carbon Footprint
- How Hungry is AI? Benchmarking Energy and Carbon Footprint
- TokenPowerBench: Benchmarking Power Consumption of LLM Inference
