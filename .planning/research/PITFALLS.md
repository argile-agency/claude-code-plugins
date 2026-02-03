# PITFALLS.md - Common Mistakes in AI Environmental Impact Tracking

## Research Date: 2026-02-03

## Overview

This document catalogs common mistakes, misconceptions, and pitfalls when tracking AI/LLM environmental impact, along with prevention strategies specific to Claude Code plugin development.

## 1. Accuracy Overconfidence

### The Mistake

**What**: Claiming or implying that carbon estimates are precise measurements

**Examples**:
- "Your session emitted exactly 8.73421 grams of CO2"
- "Accurate to ±5% with our proprietary algorithm"
- "Certified carbon accounting for corporate reporting"
- Displaying 6+ significant figures in results

**Why It's Wrong**:
- Token-to-energy conversion factors are research averages (±50% variation)
- No access to actual hardware utilization or datacenter PUE
- Carbon intensity varies by time of day (using static averages)
- Can't know which specific datacenter served the request
- Embodied carbon is excluded (5-30% of total)

**Real Accuracy**: ±50-100% for operational emissions, ±200%+ for total lifecycle

### The Impact

- **User Trust**: Overstating accuracy destroys credibility when users investigate
- **Misuse**: Companies might use inaccurate data for regulatory reporting
- **Greenwashing**: False precision enables "carbon neutral" claims without real action
- **Legal Risk**: Incorrect carbon accounting could have compliance implications

### Prevention Strategies

#### Display Formatting
```javascript
// ❌ BAD: False precision
console.log(`Carbon: ${carbonGrams.toFixed(6)} gCO2e`);
// Output: "Carbon: 8.734210 gCO2e"

// ✅ GOOD: Appropriate rounding
console.log(`Carbon: ~${Math.round(carbonGrams)} gCO2e`);
// Output: "Carbon: ~9 gCO2e"
```

#### Always Include Disclaimers
```markdown
📊 Session Impact
================
Tokens:  45,234
Energy:  ~23 Wh
Carbon:  ~9 gCO2e
Cost:    $1.23

⚠️  ESTIMATES ONLY
These are rough approximations based on research averages, not precise
measurements. Actual emissions may vary by ±50-100%. Do not use for
regulatory compliance or carbon offset calculations.

Learn more: /impact:methodology
```

#### In Documentation
```markdown
## Accuracy Expectations

This plugin provides **order-of-magnitude estimates**, not precise measurements.

| Metric | Confidence Level |
|--------|-----------------|
| Token counts | High (±5%) - direct from API |
| Relative comparison | Medium (±20%) - Opus > Sonnet > Haiku |
| Energy per token | Low (±50-100%) - based on research averages |
| Absolute carbon | Very Low (±100-200%) - too many unknowns |

**What we DON'T know:**
- Actual datacenter location serving your request
- Real-time hardware utilization and batching
- Specific GPU generation (A100? H100? H200?)
- Datacenter PUE at time of request
- Grid carbon intensity at time of request
- Embodied carbon from hardware manufacturing

**What we DO provide:**
- Directionally correct estimates for awareness
- Useful for comparing your sessions over time
- Educational tool for understanding AI environmental impact
```

#### Code Comments
```javascript
// WARNING: These conversion factors are ROUGH ESTIMATES based on 2025 research
// papers. Actual energy consumption varies by:
// - Hardware generation (H100 vs A100 vs older GPUs)
// - Batch size and server utilization
// - Prompt length (prefill) vs completion length (decode)
// - Model-specific optimizations (quantization, pruning)
// - Datacenter infrastructure (cooling, PUE)
//
// Use these for educational purposes and relative comparisons ONLY.
// Do NOT use for regulatory reporting or carbon offset purchasing.

const MODEL_FACTORS_WH_PER_1K_TOKENS = {
  'claude-opus-4-5': { input: 1.2, output: 1.5 },  // ±100% margin of error
  'claude-sonnet-4-5': { input: 0.5, output: 0.7 }, // ±100% margin of error
  'claude-haiku-3-5': { input: 0.1, output: 0.15 }  // ±100% margin of error
};
```

## 2. Missing Scope 3 Emissions

### The Mistake

**What**: Only counting operational emissions (electricity), ignoring embodied carbon

**Examples**:
- Tracking only runtime energy consumption
- Ignoring hardware manufacturing emissions
- Excluding network infrastructure
- Missing datacenter construction and maintenance

**Why It's Wrong**:
According to 2025 research:
- Operational logistics (construction, maintenance): up to 66% of datacenter lifetime emissions
- Chip manufacturing for AI accelerators: significant but hard to quantify
- Network infrastructure: routers, switches, undersea cables
- E-waste from hardware refresh cycles (2-3 year GPU lifecycles)

**Scope Breakdown**:
- **Scope 1**: Direct emissions (on-premises generators) - 0% for cloud API
- **Scope 2**: Indirect emissions from electricity - ~50-70% of total
- **Scope 3**: Everything else (manufacturing, transport, disposal) - ~30-50% of total

### The Impact

- **Underestimation**: Real carbon footprint is 1.5-2x higher than operational alone
- **Incomplete Picture**: Users think they're seeing full impact, but it's partial
- **Misaligned Incentives**: Optimizing only operational emissions misses bigger picture

### Prevention Strategies

#### Acknowledge What's Missing
```markdown
## What This Plugin Tracks

✅ **Operational Emissions (Scope 2)**
- Electricity consumed by GPUs/CPUs processing your requests
- Datacenter cooling and power distribution (PUE)
- Estimated based on token usage and regional grid carbon intensity

❌ **Embodied Emissions (Scope 3) - NOT INCLUDED**
- Hardware manufacturing (GPU fabrication, transport)
- Datacenter construction and decommissioning
- Network infrastructure (routers, cables)
- E-waste disposal

**Why not included?**
- Embodied carbon is amortized over billions of API calls
- Per-request impact is negligible (<5% of operational)
- No public data available for Anthropic's hardware lifecycle
- Would create false precision without improving actionability

**Full lifecycle estimate:**
If operational emissions are ~10 gCO2, add ~30-50% for embodied carbon:
Total lifecycle: ~13-15 gCO2 (rough approximation)
```

#### Optional: Add Multiplier
```javascript
// OPTIONAL: Include embodied carbon rough estimate
const EMBODIED_CARBON_MULTIPLIER = 1.35; // +35% for Scope 3

function calculateFullLifecycleCarbon(operationalCarbonG) {
  const fullLifecycleG = operationalCarbonG * EMBODIED_CARBON_MULTIPLIER;

  return {
    operational: Math.round(operationalCarbonG),
    embodied: Math.round(fullLifecycleG - operationalCarbonG),
    total: Math.round(fullLifecycleG)
  };
}

// Display
console.log(`Operational: ~${operational} gCO2e`);
console.log(`Embodied (est): ~${embodied} gCO2e`);
console.log(`Total lifecycle: ~${total} gCO2e`);
console.log(`⚠️  Embodied carbon is very rough estimate (+35% rule of thumb)`);
```

#### In Comparisons
```markdown
💡 Context
==========
This session (~9 gCO2 operational, ~12 gCO2 total lifecycle) is equivalent to:

- Driving a gas car ~0.03 miles (30 meters)
- Charging a smartphone ~4 times
- 18 minutes of streaming 1080p video

Note: These comparisons also include both operational and embodied emissions
for fair comparison.
```

## 3. Stale Emission Factors

### The Mistake

**What**: Using outdated carbon intensity values or energy conversion factors

**Examples**:
- Using 2020 grid carbon intensity data in 2026
- Not updating energy factors when new GPU generations release
- Hardcoding values that change quarterly/annually

**Why It's Wrong**:
- **Grid Decarbonization**: US grid carbon intensity dropped from ~450 to ~400 gCO2/kWh (2020-2025)
- **Hardware Efficiency**: H100 GPUs are 3-4x more efficient than A100 per inference operation
- **Model Optimization**: Newer model versions use less energy per token (quantization, pruning)
- **Renewable Energy**: Cloud providers increasing renewable procurement (AWS 100% renewable target 2025)

**Rate of Change**:
- Grid carbon intensity: ~2-5% annual reduction
- GPU efficiency: ~2-3x improvement per generation (every 2 years)
- Model efficiency: ~10-30% per major version

### The Impact

- **Over/Underestimation**: Using 2020 data in 2026 could overstate by 20-30%
- **Lost Trust**: Users catch outdated data, question entire methodology
- **Missed Improvements**: Can't show progress if baseline is stale

### Prevention Strategies

#### Version and Date Emission Factors
```javascript
// Carbon intensity data (gCO2/kWh)
// Source: EPA eGRID 2024, IEA 2025
// Last updated: 2026-01-15
// Next update: 2026-04-15 (quarterly)
const REGIONAL_CARBON_INTENSITY = {
  'us-east-1': { value: 340, year: 2025, source: 'EPA eGRID 2024' },
  'us-west-2': { value: 250, year: 2025, source: 'EPA eGRID 2024' },
  'eu-west-1': { value: 280, year: 2025, source: 'IEA 2025' },
  'global-avg': { value: 400, year: 2025, source: 'IEA 2025' }
};

// Model energy factors (Wh per 1K tokens)
// Source: "How Hungry is AI?" (arxiv.org/abs/2505.09598)
// Last updated: 2026-01-15
// Based on: H100 GPU generation, 2025 model versions
const MODEL_ENERGY_FACTORS = {
  'claude-opus-4-5': {
    input: 1.2,
    output: 1.5,
    source: 'Estimated from GPT-4 class benchmarks',
    hardware_generation: 'H100',
    last_updated: '2026-01-15'
  },
  // ...
};
```

#### Include Update Reminder
```markdown
## Maintenance Tasks

### Quarterly Updates (Every 3 months)
- [ ] Update regional carbon intensity values (EPA eGRID, IEA)
- [ ] Check for new model releases (Anthropic changelog)
- [ ] Review latest research papers for updated energy factors
- [ ] Update version in plugin.json

### Annual Updates (Yearly)
- [ ] Full methodology review
- [ ] Hardware generation assumptions (new GPU releases?)
- [ ] Benchmarking against published data (if Anthropic releases metrics)

### Triggered Updates (As needed)
- [ ] New Claude model family released → update energy factors
- [ ] AWS announces major renewable energy milestone → update regional factors
- [ ] New research paper with better methodology → review and integrate
```

#### Display Data Freshness
```markdown
📊 Session Impact
================
Carbon:  ~9 gCO2e

📅 Data Freshness
- Carbon intensity: US average 400 gCO2/kWh (IEA 2025)
- Model factors: Estimated from 2025 H100 benchmarks
- Last plugin update: 2026-01-15 (v1.2.0)

⚠️  If this data is >6 months old, check for plugin updates!
```

#### Automated Staleness Warning
```javascript
const PLUGIN_VERSION_DATE = '2026-01-15';
const WARN_AFTER_DAYS = 180; // 6 months

function checkDataFreshness() {
  const daysSinceUpdate = Math.floor(
    (Date.now() - new Date(PLUGIN_VERSION_DATE)) / (1000 * 60 * 60 * 24)
  );

  if (daysSinceUpdate > WARN_AFTER_DAYS) {
    console.log(`⚠️  WARNING: Emission factors are ${daysSinceUpdate} days old!`);
    console.log(`Check for plugin updates: /impact:update or visit marketplace`);
    console.log(`Carbon estimates may be outdated by 10-30%`);
  }
}
```

## 4. Ignoring Regional Variation

### The Mistake

**What**: Using global average carbon intensity for all users, regardless of location

**Examples**:
- Hardcoding 475 gCO2/kWh (global average) for everyone
- Not considering renewable energy regions
- Ignoring time-of-day grid variations

**Why It's Wrong**:
According to 2025 data, regional carbon intensity varies 3-5x:
- **Oregon (us-west-2)**: ~250 gCO2/kWh (high hydro/wind)
- **Virginia (us-east-1)**: ~340 gCO2/kWh (mixed grid)
- **Singapore (ap-southeast-1)**: ~420 gCO2/kWh (natural gas heavy)
- **India**: ~650 gCO2/kWh (coal heavy)

Using global average for Oregon user: 475 / 250 = **1.9x overestimate**
Using global average for Singapore user: 475 / 420 = **13% underestimate**

### The Impact

- **Misleading Comparisons**: Users in different regions can't compare fairly
- **Missed Opportunities**: Can't show benefit of choosing low-carbon regions
- **Accuracy**: Single biggest improvement is using regional factors (30-50% better)

### Prevention Strategies

#### Implement Regional Detection
```javascript
// Map AWS regions to carbon intensity
// Source: AWS Customer Carbon Footprint Tool 2025
const AWS_REGION_CARBON = {
  'us-east-1': 340,      // Virginia (coal+gas+nuclear)
  'us-east-2': 470,      // Ohio (coal heavy)
  'us-west-1': 280,      // California (renewables mandated)
  'us-west-2': 250,      // Oregon (hydro+wind)
  'eu-west-1': 280,      // Ireland (wind)
  'eu-central-1': 320,   // Germany (transitioning)
  'ap-southeast-1': 420, // Singapore (gas)
  'ap-northeast-1': 480  // Japan (mixed post-nuclear)
};

// Attempt to detect region from user's Anthropic API endpoint
// Or allow manual configuration
function getCarbonIntensity(userRegion) {
  return AWS_REGION_CARBON[userRegion] || 400; // Global average fallback
}
```

#### Configuration Command
```markdown
## /impact:configure region

Set your AWS region for more accurate carbon estimates:

/impact:configure region us-west-2

Available regions:
- us-west-2 (Oregon): 250 gCO2/kWh - LOWEST (hydro/wind)
- eu-west-1 (Ireland): 280 gCO2/kWh - LOW (wind)
- us-west-1 (California): 280 gCO2/kWh - LOW (renewables)
- us-east-1 (Virginia): 340 gCO2/kWh - MEDIUM
- ap-southeast-1 (Singapore): 420 gCO2/kWh - MEDIUM-HIGH
- us-east-2 (Ohio): 470 gCO2/kWh - HIGH
- ap-northeast-1 (Japan): 480 gCO2/kWh - HIGH

💡 TIP: Choose lower-carbon regions when performance allows!
```

#### Show Regional Context
```markdown
📊 Session Impact
================
Carbon:  ~9 gCO2e (based on Virginia grid: 340 gCO2/kWh)

💡 Regional Comparison
If this session ran in:
- Oregon (hydro):  ~7 gCO2e  ⬇ 22% lower
- California:      ~7 gCO2e  ⬇ 22% lower
- Ohio (coal):    ~12 gCO2e  ⬆ 33% higher
- Japan:          ~13 gCO2e  ⬆ 44% higher

Configure your region: /impact:configure region us-west-2
```

## 5. Overfitting to Anthropic's Stack

### The Mistake

**What**: Hardcoding assumptions specific to Anthropic that may change or limit portability

**Examples**:
- Assuming AWS infrastructure only
- Hardcoding model names without extensibility
- Assuming H100 GPUs forever
- Not planning for other LLM providers (OpenAI, Cohere)

**Why It's Wrong**:
- **Anthropic may switch providers**: GCP, Azure partnerships
- **New models released frequently**: Claude 5, Claude Opus 5.5, etc.
- **Hardware upgrades**: H200, B100, next-gen accelerators
- **Users may want multi-provider tracking**: Compare Anthropic vs OpenAI

### Prevention Strategies

#### Abstraction Layer
```javascript
// Provider-agnostic carbon tracking
class LLMProvider {
  constructor(name, models, defaultRegion) {
    this.name = name;
    this.models = models;
    this.defaultRegion = defaultRegion;
  }

  getCarbonIntensity(region) {
    // Provider-specific logic
  }
}

const ANTHROPIC = new LLMProvider('Anthropic', {
  'claude-opus-4-5': { input: 1.2, output: 1.5 },
  'claude-sonnet-4-5': { input: 0.5, output: 0.7 },
  // ...
}, 'us-east-1');

const OPENAI = new LLMProvider('OpenAI', {
  'gpt-4-turbo': { input: 1.0, output: 1.3 },
  'gpt-3.5-turbo': { input: 0.2, output: 0.3 },
  // ...
}, 'us-east-1');

// Usage
const provider = ANTHROPIC; // Easy to swap
const carbonG = calculateCarbon(tokens, provider);
```

#### Future-Proof Model Matching
```javascript
// ❌ BAD: Exact model name matching
if (model === 'claude-sonnet-4-5-20250929') {
  factors = { input: 0.5, output: 0.7 };
}

// ✅ GOOD: Pattern matching with fallback
function getModelFactors(modelName) {
  // Exact match first
  if (MODEL_FACTORS[modelName]) {
    return MODEL_FACTORS[modelName];
  }

  // Pattern matching
  if (modelName.includes('opus')) return MODEL_FACTORS['claude-opus-4-5'];
  if (modelName.includes('sonnet')) return MODEL_FACTORS['claude-sonnet-4-5'];
  if (modelName.includes('haiku')) return MODEL_FACTORS['claude-haiku-3-5'];

  // Conservative fallback (assume Opus)
  console.warn(`Unknown model ${modelName}, using Opus factors (conservative)`);
  return MODEL_FACTORS['claude-opus-4-5'];
}
```

#### Configuration File for Easy Updates
```json
// .claude/impact-tracker-config.json
{
  "version": "1.2.0",
  "last_updated": "2026-01-15",
  "providers": {
    "anthropic": {
      "infrastructure": "AWS",
      "default_region": "us-east-1",
      "pue": 1.2,
      "models": {
        "claude-opus-4-5": { "input_wh_per_1k": 1.2, "output_wh_per_1k": 1.5 },
        "claude-sonnet-4-5": { "input_wh_per_1k": 0.5, "output_wh_per_1k": 0.7 },
        "claude-haiku-3-5": { "input_wh_per_1k": 0.1, "output_wh_per_1k": 0.15 }
      }
    }
  },
  "regions": {
    "us-east-1": { "name": "Virginia", "carbon_g_per_kwh": 340 },
    "us-west-2": { "name": "Oregon", "carbon_g_per_kwh": 250 }
  }
}
```

## 6. Performance Overhead

### The Mistake

**What**: Adding so much tracking logic that it slows down the user's workflow

**Examples**:
- Synchronous file I/O on every API call
- Complex calculations blocking tool execution
- Excessive logging to disk
- UI updates that freeze terminal

**Why It's Wrong**:
- Users will disable plugin if it adds noticeable latency
- Target: <50ms overhead per API call
- File I/O can take 10-100ms, calculation should be <1ms

### Prevention Strategies

#### Async Operations
```javascript
// ❌ BAD: Synchronous file write on every call
function trackApiCall(tokenData) {
  const state = readFileSync('.claude/impact-state.json');
  state.total_tokens += tokenData.total;
  writeFileSync('.claude/impact-state.json', JSON.stringify(state));
}

// ✅ GOOD: In-memory accumulation, periodic async write
let sessionState = { total_tokens: 0, calls: [] };

function trackApiCall(tokenData) {
  // Fast in-memory update (~0.1ms)
  sessionState.total_tokens += tokenData.total;
  sessionState.calls.push(tokenData);
}

// Async write every 10 calls or on session end
async function persistState() {
  await writeFile('.claude/impact-state.json', JSON.stringify(sessionState));
}
```

#### Lightweight Calculation
```javascript
// ✅ GOOD: Simple arithmetic, no loops or external calls
function calculateCarbon(inputTokens, outputTokens, model) {
  const factors = MODEL_FACTORS[model] || DEFAULT_FACTORS;

  const energyWh =
    (inputTokens / 1000) * factors.input +
    (outputTokens / 1000) * factors.output;

  const carbonG = (energyWh / 1000) * CARBON_INTENSITY * PUE;

  return Math.round(carbonG);
}

// Benchmark: ~0.01ms per call
```

#### Batched Display Updates
```javascript
// Only update UI on user request, not every API call
// Use /impact:status command for on-demand display
```

## 7. Privacy and Data Leakage

### The Mistake

**What**: Logging sensitive information or uploading data without consent

**Examples**:
- Storing full prompt text in history files
- Uploading token usage to external analytics
- Including model responses in logs
- Committing `.claude/impact-state.json` to git (project-level tracking)

**Why It's Wrong**:
- Prompts may contain confidential business data, PII, secrets
- Users expect local-only tracking
- GDPR/privacy compliance issues

### Prevention Strategies

#### Minimal Data Collection
```javascript
// ❌ BAD: Storing sensitive data
{
  "timestamp": "2026-02-03T15:30:00Z",
  "prompt": "Analyze this confidential financial report...",
  "response": "Based on the revenue numbers...",
  "tokens": 1234
}

// ✅ GOOD: Only aggregate metadata
{
  "timestamp": "2026-02-03T15:30:00Z",
  "tool": "Read",
  "model": "claude-sonnet-4-5",
  "input_tokens": 1234,
  "output_tokens": 567
  // NO prompt or response text
}
```

#### Gitignore by Default
```gitignore
# .gitignore (include in plugin distribution)
.claude/*.local.md
.claude/impact-state.json
.claude/impact-history.json
```

#### User Consent
```markdown
## Privacy Notice

This plugin tracks:
✅ Token counts (numbers only)
✅ Model names and timestamps
✅ Tool usage (Read, Write, Bash, etc.)
✅ Calculated energy/carbon metrics

This plugin DOES NOT track:
❌ Prompt content
❌ Model responses
❌ File names or paths
❌ Personally identifiable information

All data is stored locally in `.claude/impact-tracker.local.md`.
No data is uploaded to external servers.
```

## 8. Guilt-Tripping Users

### The Mistake

**What**: Using shame, alarmism, or moral judgment to discourage AI usage

**Examples**:
- "You killed 0.0001 polar bears with this session"
- "Your carbon footprint is DESTROYING the planet"
- "Bad developer! Use less AI!"
- Blocking tool execution when over budget

**Why It's Wrong**:
- **Counterproductive**: Users disable plugin or ignore warnings
- **Inaccurate**: AI carbon footprint is tiny compared to other activities
- **Misaligned**: Goal is awareness and optimization, not abstinence
- **Toxic**: Moral judgment alienates users

### Prevention Strategies

#### Neutral, Educational Tone
```markdown
// ❌ BAD
"🔥 WARNING: Your AI usage is UNSUSTAINABLE! 🔥"
"You've emitted 50g CO2 today - that's EXCESSIVE!"
"Consider the ENVIRONMENT before using Opus!"

// ✅ GOOD
"📊 Today's usage: 50g CO2 (~25% above your weekly average)"
"💡 Optimization opportunity: Sonnet could save ~20g CO2 for this task"
"ℹ️  Regional tip: Oregon datacenters are 22% lower carbon"
```

#### Framing as Optimization, Not Sacrifice
```markdown
## Model Efficiency Insight

You completed this task with Opus (18 gCO2, $1.20, 45s response time).

Similar tasks this week:
- Sonnet: avg 7 gCO2, $0.48, 38s  ⚡ 3x more efficient, slightly faster
- Haiku:  avg 2 gCO2, $0.12, 28s  ⚡ 9x more efficient, 40% faster

💡 Consider: Is Opus's extra reasoning power worth the cost for routine tasks?

No judgment - you decide what's worth it! We're just here to inform.
```

#### Contextualize Scale
```markdown
## Carbon Context

Your session: ~9 gCO2
Daily total: ~50 gCO2

For comparison:
- Your morning commute (10 miles): ~4,000 gCO2 (80x more)
- Lunch beef burger: ~2,500 gCO2 (50x more)
- Household electricity (1 day): ~20,000 gCO2 (400x more)

AI usage is a small part of your carbon footprint. Every bit helps, but
don't stress too much - focus on the big wins (transport, food, heating).
```

## Summary: Prevention Checklist

Before releasing plugin, verify:

- [ ] **Accuracy**: Disclaimers in all displays, rounded to 1-2 sig figs
- [ ] **Scope**: Documented what's included/excluded (operational only)
- [ ] **Data Freshness**: Version numbers, last updated dates, staleness warnings
- [ ] **Regional Factors**: Support for regional carbon intensity, not just global average
- [ ] **Extensibility**: Abstraction layer for future models/providers
- [ ] **Performance**: <50ms overhead per API call
- [ ] **Privacy**: No sensitive data logged, local-only storage, gitignore
- [ ] **Tone**: Neutral, educational, empowering (not guilt-tripping)
- [ ] **Documentation**: Methodology, sources, limitations clearly explained
- [ ] **Testing**: Validate calculations, edge cases, error handling

## References

### Accuracy and Methodology
- [Cornell: Roadmap shows the environmental impact of AI data center boom (November 2025)](https://news.cornell.edu/stories/2025/11/roadmap-shows-environmental-impact-ai-data-center-boom)
- [Nature Sustainability: Environmental impact and net-zero pathways for sustainable AI servers in USA (2025)](https://www.nature.com/articles/s41893-025-01681-y)

### Best Practices
- [World Economic Forum: How to cut the environmental impact of your company's AI use (June 2025)](https://www.weforum.org/stories/2025/06/how-ai-use-impacts-the-environment/)
- [PwC: The environmental impact of AI and how to mitigate it (2025)](https://www.pwc.be/en/news-publications/2025/responsible-ai-environmental-impact.html)

### Pitfalls and Challenges
- [UNEP: AI has an environmental problem. Here's what the world can do about that.](https://www.unep.org/news-and-stories/story/ai-has-environmental-problem-heres-what-world-can-do-about)
- [Online Learning Consortium: The Real Environmental Footprint of Generative AI (December 2025)](https://onlinelearningconsortium.org/olc-insights/2025/12/the-real-environmental-footprint-of-generative-ai/)
- [Wikipedia: Environmental impact of artificial intelligence](https://en.wikipedia.org/wiki/Environmental_impact_of_artificial_intelligence)
