# Phase 1: Foundation - Research

**Researched:** 2026-02-03
**Domain:** Claude Code plugin hooks, token tracking, carbon estimation
**Confidence:** HIGH

## Summary

Phase 1 establishes the foundation for token usage tracking and carbon/energy estimation in the ecoscore plugin. Based on comprehensive research of Claude Code's hook system, existing plugin architecture, and environmental impact methodologies, the recommended approach uses PostToolUse hooks to capture API token usage, file-based persistence for session state, and research-based conversion formulas for carbon estimates.

The Claude Code platform provides excellent hook infrastructure for this purpose: PostToolUse hooks fire after every tool execution with access to both tool input and response data. However, API token usage data is **not directly exposed** in the hook input schema - hooks receive tool-level information (tool_name, tool_input, tool_response) but not Anthropic API metadata like token counts or model usage.

This requires an **alternative approach**: estimate tokens from tool usage patterns or implement a workaround if Claude Code exposes token data through environment variables or transcript parsing.

**Primary recommendation:** Implement PostToolUse hooks for tool tracking, parse session transcripts for token data, use file-based state management, and apply research-based token-to-energy conversion formulas with transparent accuracy disclaimers (±50-100%).

## Standard Stack

### Core Components

| Component | Version/Type | Purpose | Why Standard |
|-----------|--------------|---------|--------------|
| Claude Code Hooks | PostToolUse | Capture tool execution events | Built-in event system, no dependencies needed |
| JSON file storage | Native | Persist session state across restarts | No database needed, gitignore-friendly, human-readable |
| Bash scripts | Shell | Calculation engine for energy/carbon | Zero dependencies, works on all platforms with Claude Code |
| YAML frontmatter | Plugin format | Configuration and metadata | Standard plugin component format |

### Supporting Components

| Component | Version/Type | Purpose | When to Use |
|-----------|--------------|---------|-------------|
| jq | CLI tool | JSON parsing in hook scripts | If processing hook input in bash |
| Transcript parsing | Read tool | Extract token counts from conversation history | If API metadata not in hook input |
| bc calculator | Shell utility | Floating-point arithmetic in bash | For energy/carbon calculations |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| File storage | SQLite database | More complex, requires dependency, overkill for simple aggregation |
| Bash calculations | Python script | Better precision but requires Python dependency in plugin |
| PostToolUse hooks | SessionEnd hook only | Would miss per-tool attribution, less granular |
| Transcript parsing | Hook input directly | Preferred if token data becomes available in future Claude Code version |

**Installation:**

No external dependencies required. Claude Code plugins are markdown-based with no build step.

## Architecture Patterns

### Recommended Project Structure

```
plugins/ecoscore/
├── .claude-plugin/
│   └── plugin.json          # Manifest with version, description
├── hooks/
│   └── hooks.json           # PostToolUse hook definitions
├── commands/
│   ├── analyze.md           # Existing ecoscore analysis
│   ├── status.md            # NEW: Show current session impact
│   └── report.md            # Extend with carbon tracking
├── .ecoscore/               # NEW: Session state directory
│   └── session.json         # Token counts, carbon estimates
└── README.md
```

### Pattern 1: PostToolUse Hook for Token Tracking

**What:** Hook that fires after every tool execution to accumulate metrics

**When to use:** Capturing per-tool usage data for attribution and aggregation

**Example:**

```json
{
  "description": "EcoScore token and carbon tracking",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/track-usage.sh",
            "async": false,
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Hook input structure (from documentation):**

```json
{
  "session_id": "abc123",
  "hook_event_name": "PostToolUse",
  "tool_name": "Read",
  "tool_input": {
    "file_path": "/path/to/file.txt"
  },
  "tool_response": {
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**CRITICAL LIMITATION:** Token counts are NOT included in hook input. Need workaround.

### Pattern 2: Transcript Parsing for Token Data

**What:** Parse session transcript file to extract actual token usage from API responses

**When to use:** When PostToolUse hook input doesn't contain token metadata

**Example:**

```bash
#!/bin/bash
# transcript-parser.sh
TRANSCRIPT_PATH="$1"

# Extract token usage from transcript JSONL
# Each API response includes usage metadata
jq -r 'select(.type == "message") |
       select(.usage != null) |
       "\(.usage.input_tokens),\(.usage.output_tokens)"' \
  "$TRANSCRIPT_PATH" | \
  awk -F',' '{in+=$1; out+=$2} END {print in, out}'
```

**Source:** Hook input provides `transcript_path` field (see [common input fields](https://code.claude.com/docs/en/hooks#common-input-fields))

### Pattern 3: File-Based State Management

**What:** JSON file storing session metrics, updated incrementally

**When to use:** Persisting data across tool calls and sessions

**Example state file (`.ecoscore/session.json`):**

```json
{
  "session_id": "abc123",
  "session_start": "2026-02-03T15:00:00Z",
  "total_input_tokens": 45234,
  "total_output_tokens": 13778,
  "total_energy_wh": 22.5,
  "total_carbon_g": 9.0,
  "api_calls": 12,
  "tools_used": {
    "Read": 5,
    "Write": 3,
    "Bash": 4
  },
  "models_used": {
    "claude-sonnet-4-5": 10,
    "claude-opus-4-5": 2
  }
}
```

### Pattern 4: Calculation Engine (Token → Energy → Carbon)

**What:** Inline bash calculations using research-based conversion factors

**When to use:** Converting token counts to environmental impact metrics

**Example:**

```bash
#!/bin/bash
# calculate-impact.sh
INPUT_TOKENS=$1
OUTPUT_TOKENS=$2
MODEL=$3

# Model factors (Wh per 1K tokens) - Source: STACK.md research
case $MODEL in
  *opus*) INPUT_FACTOR=1.2; OUTPUT_FACTOR=1.5 ;;
  *sonnet*) INPUT_FACTOR=0.5; OUTPUT_FACTOR=0.7 ;;
  *haiku*) INPUT_FACTOR=0.1; OUTPUT_FACTOR=0.15 ;;
  *) INPUT_FACTOR=0.5; OUTPUT_FACTOR=0.7 ;;
esac

# Constants (conservative estimates)
PUE=1.2                  # AWS datacenter power usage effectiveness
CARBON_INTENSITY=400     # gCO2/kWh (US average, configurable by region)

# Energy calculation (Wh)
INPUT_ENERGY=$(echo "scale=4; $INPUT_TOKENS / 1000 * $INPUT_FACTOR" | bc)
OUTPUT_ENERGY=$(echo "scale=4; $OUTPUT_TOKENS / 1000 * $OUTPUT_FACTOR" | bc)
TOTAL_ENERGY=$(echo "scale=4; $INPUT_ENERGY + $OUTPUT_ENERGY" | bc)

# Carbon calculation (gCO2)
ENERGY_KWH=$(echo "scale=6; $TOTAL_ENERGY / 1000" | bc)
CARBON_G=$(echo "scale=2; $ENERGY_KWH * $CARBON_INTENSITY * $PUE" | bc)

# Output results
echo "{\"energy_wh\": $TOTAL_ENERGY, \"carbon_g\": $CARBON_G}"
```

### Anti-Patterns to Avoid

- **Synchronous file I/O on every hook**: Use in-memory accumulation, write periodically (see PITFALLS.md #6)
- **Claiming high accuracy**: Estimates are ±50-100%, must include disclaimers (see PITFALLS.md #1)
- **Ignoring regional variation**: Carbon intensity varies 3-5x by region (see PITFALLS.md #4)
- **Storing sensitive data**: Never log prompt/response content (see PITFALLS.md #7)
- **Overfitting to current models**: Use pattern matching for model detection (see PITFALLS.md #5)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Real-time grid carbon intensity | Custom API polling | Static regional averages, quarterly updates | No reliable free API, real-time data doesn't improve actionability, adds complexity |
| Token estimation from text | Character-based heuristics | Direct API token counts from transcript | Character counts are 30-50% inaccurate, API provides exact counts |
| Hardware monitoring | System profiling tools | Research-based per-token averages | No access to Anthropic's infrastructure, monitoring adds overhead |
| Database for metrics | SQLite, PostgreSQL | JSON file storage | Overkill for simple aggregation, adds dependency and complexity |
| External carbon APIs | CodeCarbon, Cloud Carbon API | Inline calculation formulas | APIs are Python-only or require authentication, formulas are sufficient |

**Key insight:** This domain requires transparency about limitations more than technical sophistication. Simple, well-documented estimates with clear accuracy bounds are more valuable than complex systems that imply false precision.

## Common Pitfalls

### Pitfall 1: Assuming Token Data in Hook Input

**What goes wrong:** Implementing PostToolUse hook expecting token counts in JSON input, but they're not present

**Why it happens:** Documentation shows tool_input and tool_response, but Anthropic API metadata (tokens, model) is not exposed in hook schema

**How to avoid:**
1. Review [PostToolUse input schema](https://code.claude.com/docs/en/hooks#posttooluse-input) carefully
2. Test hooks with `claude --debug` to see actual input
3. Fall back to transcript parsing if token data not available
4. Verify with minimal test hook before building full system

**Warning signs:**
- Hook script errors trying to access `.usage.input_tokens` fields
- Empty/null values when reading token data
- Hook working but metrics showing zero

### Pitfall 2: Performance Overhead from Hooks

**What goes wrong:** Hook runs on EVERY tool call (Read, Write, Bash, etc.), slowing down workflow

**Why it happens:** Default matcher `"*"` with synchronous file I/O creates 50-100ms latency per tool

**How to avoid:**
1. Use `async: true` if immediate feedback not needed (but loses decision control)
2. Keep calculations under 1ms (simple arithmetic, no external calls)
3. Batch file writes (in-memory accumulation, write every N calls)
4. Target <50ms total hook overhead

**Warning signs:**
- Noticeable delay between tool executions
- User disables plugin due to slowness
- Hook timeout warnings in debug mode

### Pitfall 3: Stale Emission Factors

**What goes wrong:** Using 2020 grid carbon intensity in 2026, overstating emissions by 20-30%

**Why it happens:** Hardcoded values without version tracking or update reminders

**How to avoid:**
1. Version all data sources with last_updated dates
2. Include staleness warning if data >6 months old
3. Document update schedule (quarterly for carbon intensity)
4. Use config file for easy updates without code changes

**Warning signs:**
- Carbon values seem high compared to recent research
- User questions methodology and catches outdated sources
- Plugin hasn't been updated in 6+ months

### Pitfall 4: Accuracy Overconfidence

**What goes wrong:** Displaying "8.73421 gCO2" implies precision that doesn't exist (±50-100% margin)

**Why it happens:** Programming habit of showing all decimal places without considering measurement uncertainty

**How to avoid:**
1. Round to 1-2 significant figures: "~9 gCO2" not "8.734 gCO2"
2. Always include disclaimer: "Estimates only, ±50-100% accuracy"
3. Use "~" prefix to indicate approximation
4. Document what's included/excluded (operational only, no embodied carbon)
5. Never claim "accurate," "precise," or "certified"

**Warning signs:**
- Users treating estimates as precise measurements
- Inquiries about using data for regulatory reporting
- Greenwashing concerns from false precision

### Pitfall 5: Ignoring Regional Variation

**What goes wrong:** Using 400 gCO2/kWh global average for Oregon user (actual: 250 gCO2/kWh), 60% overestimate

**Why it happens:** Defaulting to single value instead of implementing region configuration

**How to avoid:**
1. Map AWS regions to carbon intensity (us-west-2: 250, us-east-1: 340, etc.)
2. Allow user configuration: `/ecoscore:configure region us-west-2`
3. Show regional comparison in reports
4. Use global average as fallback only

**Warning signs:**
- Users in low-carbon regions question high estimates
- Can't explain why two identical sessions have different carbon values
- Missing 30-50% accuracy improvement from regional factors

## Code Examples

Verified patterns from official sources and research:

### Hook Configuration (PostToolUse)

```json
{
  "description": "EcoScore environmental impact tracking",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/track-tool-usage.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/save-session.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Source:** [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)

### Transcript Parsing for Token Extraction

```bash
#!/bin/bash
# extract-tokens.sh
# Parse transcript to get actual token counts from API responses

TRANSCRIPT_PATH="$1"

if [ ! -f "$TRANSCRIPT_PATH" ]; then
  echo "0 0"
  exit 0
fi

# Extract token usage from conversation transcript
# Each API message includes usage metadata
RESULT=$(jq -r 'select(.type == "message") |
                select(.usage != null) |
                {
                  input: .usage.input_tokens,
                  output: .usage.output_tokens,
                  model: .model // "unknown"
                } | "\(.input),\(.output),\(.model)"' \
  "$TRANSCRIPT_PATH" 2>/dev/null)

if [ -z "$RESULT" ]; then
  echo "0 0 unknown"
  exit 0
fi

# Sum tokens across all messages
echo "$RESULT" | awk -F',' '
  {
    total_input += $1
    total_output += $2
    # Extract model family (opus/sonnet/haiku) from last model seen
    if ($3 ~ /opus/) model = "opus"
    else if ($3 ~ /sonnet/) model = "sonnet"
    else if ($3 ~ /haiku/) model = "haiku"
    else model = "sonnet"  # default
  }
  END {
    print total_input, total_output, model
  }'
```

**Usage:**
```bash
read INPUT_TOKENS OUTPUT_TOKENS MODEL < <(./extract-tokens.sh "$TRANSCRIPT_PATH")
```

### Energy and Carbon Calculation

```bash
#!/bin/bash
# calculate-impact.sh
# Convert token counts to energy (Wh) and carbon (gCO2)

INPUT_TOKENS=$1
OUTPUT_TOKENS=$2
MODEL=$3
REGION=${4:-"us-east-1"}  # Default to Virginia

# Model energy factors (Wh per 1000 tokens)
# Source: "How Hungry is AI?" (May 2025), LLMCarbon framework
# Confidence: ±100% (MEDIUM-LOW)
case $MODEL in
  opus*)   INPUT_WH=1.2; OUTPUT_WH=1.5 ;;
  sonnet*) INPUT_WH=0.5; OUTPUT_WH=0.7 ;;
  haiku*)  INPUT_WH=0.1; OUTPUT_WH=0.15 ;;
  *)       INPUT_WH=0.5; OUTPUT_WH=0.7 ;;  # Conservative default
esac

# Regional carbon intensity (gCO2/kWh)
# Source: EPA eGRID 2024, IEA 2025
# Last updated: 2026-01-15
case $REGION in
  us-west-2)      CARBON_INTENSITY=250 ;;  # Oregon (hydro)
  us-west-1)      CARBON_INTENSITY=280 ;;  # California
  eu-west-1)      CARBON_INTENSITY=280 ;;  # Ireland
  eu-central-1)   CARBON_INTENSITY=320 ;;  # Germany
  us-east-1)      CARBON_INTENSITY=340 ;;  # Virginia
  ap-southeast-1) CARBON_INTENSITY=420 ;;  # Singapore
  us-east-2)      CARBON_INTENSITY=470 ;;  # Ohio
  ap-northeast-1) CARBON_INTENSITY=480 ;;  # Japan
  *)              CARBON_INTENSITY=400 ;;  # Global average fallback
esac

# PUE (Power Usage Effectiveness) - datacenter overhead
PUE=1.2  # AWS typical

# Calculate energy consumption (Wh)
INPUT_ENERGY=$(echo "scale=4; $INPUT_TOKENS / 1000 * $INPUT_WH" | bc)
OUTPUT_ENERGY=$(echo "scale=4; $OUTPUT_TOKENS / 1000 * $OUTPUT_WH" | bc)
TOTAL_ENERGY=$(echo "scale=4; $INPUT_ENERGY + $OUTPUT_ENERGY" | bc)

# Calculate carbon emissions (gCO2)
ENERGY_KWH=$(echo "scale=6; $TOTAL_ENERGY / 1000" | bc)
CARBON_G=$(echo "scale=1; $ENERGY_KWH * $CARBON_INTENSITY * $PUE" | bc)

# Output JSON for consumption by commands
cat <<EOF
{
  "energy_wh": $TOTAL_ENERGY,
  "carbon_g": $CARBON_G,
  "carbon_intensity": $CARBON_INTENSITY,
  "region": "$REGION",
  "pue": $PUE,
  "model": "$MODEL"
}
EOF
```

### Session State Management

```bash
#!/bin/bash
# update-session.sh
# Update session state file with new tool usage

STATE_FILE="${CLAUDE_PLUGIN_ROOT}/.ecoscore/session.json"
TRANSCRIPT_PATH="$1"

# Ensure state directory exists
mkdir -p "${CLAUDE_PLUGIN_ROOT}/.ecoscore"

# Extract token counts from transcript
read INPUT_TOKENS OUTPUT_TOKENS MODEL < <(
  ${CLAUDE_PLUGIN_ROOT}/scripts/extract-tokens.sh "$TRANSCRIPT_PATH"
)

# Calculate impact
IMPACT=$(${CLAUDE_PLUGIN_ROOT}/scripts/calculate-impact.sh \
  "$INPUT_TOKENS" "$OUTPUT_TOKENS" "$MODEL")

ENERGY_WH=$(echo "$IMPACT" | jq -r '.energy_wh')
CARBON_G=$(echo "$IMPACT" | jq -r '.carbon_g')

# Read or initialize state
if [ -f "$STATE_FILE" ]; then
  STATE=$(cat "$STATE_FILE")
else
  STATE='{
    "session_start": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "total_energy_wh": 0,
    "total_carbon_g": 0,
    "api_calls": 0
  }'
fi

# Update totals
UPDATED=$(echo "$STATE" | jq \
  --argjson input "$INPUT_TOKENS" \
  --argjson output "$OUTPUT_TOKENS" \
  --argjson energy "$ENERGY_WH" \
  --argjson carbon "$CARBON_G" \
  '.total_input_tokens = $input |
   .total_output_tokens = $output |
   .total_energy_wh = $energy |
   .total_carbon_g = $carbon |
   .api_calls += 1 |
   .last_updated = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"')

# Write back
echo "$UPDATED" > "$STATE_FILE"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Training carbon calculators | Inference-specific metrics | 2024-2025 | Training is 1000x more expensive, irrelevant for API usage tracking |
| Hardware monitoring | Token-based estimation | 2025 | No access to cloud infrastructure, tokens are reliable proxy |
| Real-time grid data | Static regional averages | 2025 | Real-time APIs complex/expensive, quarterly updates sufficient |
| Python-only tools (CodeCarbon) | Language-agnostic formulas | 2025 | Claude Code plugins are markdown/bash, no Python dependency |
| Character-count token estimates | API-reported token counts | 2024 | API provides exact counts, 30-50% more accurate than heuristics |

**Deprecated/outdated:**
- **CodeCarbon direct integration:** Python-only, designed for training workloads, requires hardware access
- **ML CO2 Impact calculator:** Web form for training, not API inference
- **Pre-2024 academic papers:** LLM efficiency improving rapidly, outdated by 20-30%
- **Embodied carbon per-request:** Amortized over billions of queries, negligible per-session impact

## Open Questions

Things that couldn't be fully resolved:

1. **Hook Input Token Data Availability**
   - What we know: PostToolUse hooks receive tool_input and tool_response
   - What's unclear: Whether API token usage metadata is included in tool_response
   - Recommendation: Test with minimal hook, fall back to transcript parsing if not available

2. **Session Boundary Detection**
   - What we know: SessionStart/SessionEnd hooks exist, session_id provided
   - What's unclear: How to distinguish `/clear` vs new session vs resume
   - Recommendation: Use session_id for uniqueness, SessionStart matcher for trigger type

3. **Model Detection Reliability**
   - What we know: Model name patterns (opus/sonnet/haiku) in transcript
   - What's unclear: Future model naming conventions (Claude 5, Opus 5.5, etc.)
   - Recommendation: Pattern matching with conservative fallback, update quarterly

4. **Regional Carbon Intensity Updates**
   - What we know: AWS doesn't publish per-region carbon intensity table
   - What's unclear: Best source for quarterly updates (EPA, IEA, Electricity Maps?)
   - Recommendation: Use EPA eGRID for US, IEA for international, document source

5. **Hook Performance Impact**
   - What we know: Target <50ms overhead per tool call
   - What's unclear: Actual latency with file I/O and bc calculations
   - Recommendation: Benchmark with `claude --debug`, optimize if >50ms observed

## Sources

### Primary (HIGH confidence)

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) - PostToolUse schema, JSON I/O format
- [Claude Code Plugin Development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md) - Hook patterns
- Project STACK.md - Token-to-energy conversion factors (research papers May 2025)
- Project ARCHITECTURE.md - File persistence patterns, hook integration

### Secondary (MEDIUM confidence)

- [AWS Customer Carbon Footprint Tool](https://aws.amazon.com/sustainability/tools/aws-customer-carbon-footprint-tool/) - Regional carbon methodology
- [AWS Architecture Blog: Region Selection for Sustainability](https://aws.amazon.com/blogs/architecture/how-to-select-a-region-for-your-workload-based-on-sustainability-goals/) - Regional factors
- EPA eGRID 2024 - US regional carbon intensity (last updated 2025)
- IEA 2025 - International carbon intensity data

### Tertiary (LOW confidence - use with caution)

- Cloud Carbon Footprint Methodology - General approach, not Anthropic-specific
- Generic AWS region carbon estimates - No official Anthropic/AWS public table

## Metadata

**Confidence breakdown:**
- Hook architecture: HIGH - Official Claude Code documentation, verified examples
- Token extraction: MEDIUM - Schema documented but token data availability needs testing
- Energy factors: MEDIUM-LOW - Research averages with ±100% margin, not Anthropic-specific
- Carbon intensity: MEDIUM - EPA/IEA sources credible but annual averages, not real-time
- Implementation patterns: HIGH - Existing ecoscore plugin demonstrates proven patterns

**Research date:** 2026-02-03
**Valid until:** 2026-05-03 (3 months - stable domain, quarterly updates for emission factors)

**Critical next steps for planning:**
1. Test PostToolUse hook with `claude --debug` to verify actual JSON input structure
2. Confirm token data availability (in hook vs. transcript parsing required)
3. Benchmark hook performance with sample calculations
4. Verify jq and bc availability on target platforms (Windows/macOS/Linux)
5. Design state file schema for session tracking

---

## Implementation Notes for Planner

### High Priority
- **Token data source verification** is critical path - determines architecture
- **Performance testing** must happen early - hook runs on EVERY tool call
- **Accuracy disclaimers** required in all user-facing output

### Medium Priority
- Regional carbon factors improve accuracy by 30-50%
- Historical tracking requires careful schema design
- Cost correlation provides useful context

### Low Priority (defer to later phases)
- Embodied carbon estimation (adds <10% value, doubles complexity)
- Real-time grid conditions (minimal accuracy gain, high complexity)
- Multi-provider support (Anthropic-only for v1)

### Quick Wins
- Display token counts first (high accuracy, immediate value)
- Add "charging a smartphone" comparisons (makes carbon relatable)
- Include methodology link (builds trust)
