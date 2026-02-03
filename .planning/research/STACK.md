# STACK.md - AI/LLM Environmental Impact Tracking Stack

## Research Date: 2026-02-03

## Overview

This document outlines the standard 2025-2026 stack for tracking AI/LLM environmental impact, focusing on carbon estimation methodologies, tools, and data sources relevant for Claude Code plugin development.

## Carbon Estimation Libraries & Tools

### CodeCarbon (Recommended)
- **Source**: mlco2/codecarbon (GitHub)
- **Version**: 3.2.1 (released January 2, 2025)
- **Language**: Python
- **Use Case**: Hardware electricity power consumption estimation (GPU + CPU + RAM)

**Key Features**:
- Tracks emissions using `@track_emissions()` decorator
- Supports independent monitoring via CLI: `codecarbon monitor`
- Online dashboard integration with experiment tracking
- Regional carbon intensity data (per cloud provider or country)
- Fallback to world average: 475 gCO2.eq/KWh

**Methodology**:
```
Energy (kWh) = Power (W) × Time (s) / 3600
Emissions (kgCO2e) = Energy (kWh) × Carbon Intensity (kgCO2e/kWh)
```

**Limitations for Our Use**:
- Python-only (Claude Code plugins are JavaScript/Node.js)
- Designed for training workloads, not API-based inference
- Cannot track external API calls (Anthropic API)
- Requires hardware access (not available for cloud API usage)

### ML CO2 Impact
- **Purpose**: Research framework for ML carbon footprint
- **Status**: Academic reference, not production library
- **Use Case**: Methodology reference only

## Carbon Estimation Methodologies (2025-2026)

### 1. Infrastructure-Aware Benchmarking Framework (May 2025)

**Paper**: "How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference"

**Key Findings**:
- GPT-4o: 0.42 Wh per short query (40% more than Google search at 0.30 Wh)
- Most energy-intensive models: 29 Wh per long prompt (65x more than efficient systems)
- Combines API performance data with infrastructure-level environmental multipliers

**Formula**:
```
E_query = Model_Performance × Infrastructure_Multiplier × Statistical_Hardware_Config
```

### 2. One-Token Model (OTM)

**Source**: antarctica.io research
**Purpose**: Energy consumption on per-token basis

**Formula**:
```
Energy_per_token = (Server_Power_W × Token_Latency_s) / Number_of_Tokens
```

**For Inference**:
```
Total_Energy_kWh = (Tokens_Generated × Energy_per_token) / 3600000
CO2_emissions_kg = Total_Energy_kWh × Grid_Carbon_Intensity_kgCO2/kWh
```

### 3. LLMCarbon Framework (2023, Updated 2025)

**Components**:
1. **Parameter Models**: Architecture details (model size, layers, attention heads)
2. **Neural Scaling Law**: Computational requirements based on model scale
3. **FLOP Models**: Floating-point operations for inference
4. **Hardware Efficiency**: GPU utilization, batch size effects
5. **Operational Carbon**: Runtime emissions from electricity
6. **Embodied Carbon**: Manufacturing emissions (hardware lifecycle)

**Accuracy**: 8.2% error for operational, 3.6% for embodied carbon

**Scope Breakdown**:
- **Scope 1**: Direct emissions (on-premises generators) - N/A for API usage
- **Scope 2**: Indirect emissions from purchased electricity
- **Scope 3**: Embodied carbon from hardware manufacturing

### 4. Time-Based Methodology (Gravity Climate, 2025)

**Inputs**:
- Query processing time (seconds)
- Maximum server power (Watts)
- Server utilization (percentage)
- Datacenter Power Usage Effectiveness (PUE)

**Formula**:
```
Energy_kWh = (Max_Power_W × Utilization × Time_s × PUE) / 3600
```

**Typical PUE Values**:
- Modern hyperscale datacenters: 1.1-1.2
- Average datacenter: 1.5-1.7
- Older facilities: 2.0+

### 5. Simulation Framework (July 2025)

**Tools**: Vidur (LLM inference simulator) + Vessim (grid-aware energy co-simulator)

**Features**:
- GPU power model for varying parameters
- Dynamic grid condition evaluation
- Prefill vs. decode phase attribution

**Use Case**: Academic research, not production implementation

## Data Sources for Emission Factors

### Carbon Intensity by Region

**Global Databases**:
1. **Electricity Maps** (electricitymaps.com)
   - Real-time grid carbon intensity
   - API available for 70+ countries
   - 5-minute update intervals

2. **IEA Emission Factors** (International Energy Agency)
   - Annual country-level averages
   - Historical data back to 1990

3. **EPA eGRID** (US Environmental Protection Agency)
   - US regional grid data
   - Updated annually
   - Subregion-level granularity

4. **Cloud Provider Specific**:
   - AWS: Regional carbon intensity published
   - Google Cloud: Carbon-free energy percentage by region
   - Azure: Sustainability data per datacenter region

### Token-to-Energy Conversion Factors

**Research-Based Estimates (2025)**:

| Model Class | Energy per 1K Tokens | Source |
|------------|---------------------|--------|
| GPT-4 class | 0.5-2 Wh | Infrastructure-Aware Benchmark |
| GPT-3.5 class | 0.1-0.5 Wh | TokenPowerBench |
| Claude 3 Opus | 0.8-1.5 Wh | Estimated (similar to GPT-4) |
| Claude 3 Sonnet | 0.3-0.8 Wh | Estimated |
| Claude 3 Haiku | 0.05-0.2 Wh | Estimated |

**Note**: These are rough estimates. Actual values depend on:
- Prompt length (prefill energy cost)
- Generation length (decode energy cost)
- Batch size and server utilization
- Hardware generation (H100 vs A100 vs older GPUs)

### Anthropic-Specific Considerations

**Known Data**:
- Anthropic uses AWS infrastructure (primarily)
- Multi-region deployment (us-east-1, us-west-2, eu-west-1, etc.)
- No public per-token energy metrics

**Estimation Approach**:
1. Use token count as primary metric
2. Apply model-class energy factors
3. Use AWS regional carbon intensity
4. Include PUE multiplier (assume 1.2 for AWS)

## What NOT to Use and Why

### ❌ CodeCarbon Directly
**Why**: Python-only, requires hardware access, designed for training not API calls

### ❌ Hardware-Level Monitoring Tools
**Examples**: NVIDIA SMI, Intel Power Gadget, `powerstat`
**Why**: No access to Anthropic's infrastructure, measures local machine not API backend

### ❌ Training-Focused Carbon Calculators
**Examples**: ML CO2 Impact Calculator (web form)
**Why**: Training emissions >> inference emissions (orders of magnitude different)

### ❌ Overly Detailed FLOP Calculations
**Why**:
- No access to Anthropic's model architecture details
- FLOP-based estimates require knowing exact hardware utilization
- Too complex for real-time tracking in plugin

### ❌ Stale Academic Papers (Pre-2024)
**Why**:
- LLM efficiency improving rapidly
- New hardware generations (H100, H200) significantly more efficient
- Outdated grid carbon intensity data

### ❌ Embodied Carbon in Real-Time Tracking
**Why**:
- Amortized over billions of queries
- Negligible per-query impact (<5% of operational)
- Creates false precision

### ❌ Water Usage Tracking
**Why**:
- Highly datacenter-specific
- No public data for Anthropic/AWS facilities
- Cooling efficiency varies wildly (air vs. water vs. evaporative)
- Scope creep for initial plugin

## Recommended Stack for Claude Code Plugin

### Data Collection Layer
- **Tool**: Custom JavaScript/TypeScript module
- **Method**: Hook into Anthropic API responses to extract token counts
- **Storage**: In-memory session aggregation, optional file persistence

### Calculation Engine
- **Language**: JavaScript/Node.js (Claude Code native)
- **Model**: Simplified token-to-energy conversion factors
- **Formula**:
  ```javascript
  const energyWh = (inputTokens * inputFactor + outputTokens * outputFactor) / 1000;
  const carbonKg = (energyWh / 1000) * carbonIntensity * PUE;
  ```

### Carbon Intensity Data
- **Source**: Static JSON file with AWS region mappings
- **Update Frequency**: Quarterly manual updates
- **Fallback**: Global average (475 gCO2/kWh) if region unknown

### Display Layer
- **Format**: Real-time terminal display (via Claude Code UI)
- **Metrics**: Token count, energy (Wh), carbon (gCO2), cost ($)
- **Aggregation**: Per-session, per-command, cumulative

### No External Dependencies
- **Rationale**: Plugins are markdown-based, no npm packages
- **Approach**: Inline calculation logic in hooks/scripts
- **Benefit**: Zero installation friction, portable across systems

## Estimation Accuracy Expectations

### Confidence Levels

**High Confidence (±10-20%)**:
- Token count (direct from API)
- Relative model comparison (Opus > Sonnet > Haiku)
- Cost tracking (known pricing)

**Medium Confidence (±50-100%)**:
- Energy per token (model-class averages)
- Regional carbon intensity (annual averages)

**Low Confidence (±200%+)**:
- Absolute carbon emissions (too many unknowns)
- Real-time grid conditions
- Hardware-specific efficiency

### Transparency Requirements

**Must Communicate**:
- "Estimates are rough approximations, not precise measurements"
- "Based on research averages, not Anthropic-specific data"
- "Actual emissions vary by datacenter location, time of day, and hardware"

**Must NOT Claim**:
- "Accurate to the gram"
- "Certified carbon accounting"
- "Auditable emissions reporting"

## References

### Academic Papers
- [How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference (May 2025)](https://arxiv.org/abs/2505.09598)
- [LLMCarbon: Modeling the end-to-end Carbon Footprint of Large Language Models (2023)](https://arxiv.org/abs/2309.14393)
- [Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations (July 2025)](https://arxiv.org/html/2507.11417v1)
- [TokenPowerBench: Benchmarking the Power Consumption of LLM Inference (December 2025)](https://arxiv.org/html/2512.03024v1)
- [From Prompts to Power: Measuring the Energy Footprint of LLM Inference (November 2025)](https://arxiv.org/html/2511.05597)

### Tools & Frameworks
- [CodeCarbon GitHub Repository](https://github.com/mlco2/codecarbon)
- [CodeCarbon Methodology Documentation](https://mlco2.github.io/codecarbon/methodology.html)
- [The One-Token Model - Antarctica.io](https://antarctica.io/research/one-token-model)

### Industry Resources
- [Gravity Climate: Developing An Emissions Accounting Methodology for AI](https://www.gravityclimate.com/blog/developing-an-emissions-accounting-methodology-for-ai)
- [Arbor: AI's Environmental Impact: Calculated and Explained](https://www.arbor.eco/blog/ai-environmental-impact)
- [MIT News: Explained - Generative AI's environmental impact (January 2025)](https://news.mit.edu/2025/explained-generative-ai-environmental-impact-0117)

### Data Sources
- Electricity Maps: Real-time carbon intensity
- EPA eGRID: US regional emissions factors
- IEA: Global electricity carbon intensity database
