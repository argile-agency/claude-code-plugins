---
name: Green IT Analysis
description: This skill should be used when the user asks about "environmental impact", "carbon footprint", "green IT", "sustainability analysis", "ecoscore", "energy efficiency", "carbon-aware development", "AI token efficiency", "reduce environmental impact", or wants to analyze code for sustainability. Provides comprehensive methodology for environmental impact analysis across 9 scopes.
version: 0.1.0
---

# Green IT Analysis

Comprehensive methodology for analyzing software environmental impact based on Green IT principles and carbon-aware practices.

## Purpose

Analyze codebases to estimate environmental impact and generate actionable recommendations for reducing carbon footprint. Cover all aspects of software sustainability from code efficiency to AI usage patterns.

## Scoring Methodology

### EcoScore Scale (0-100)

Calculate a numeric score where higher is better:

| Range | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | Industry-leading sustainability |
| 70-89 | Good | Meets green IT standards |
| 50-69 | Fair | Room for improvement |
| 30-49 | Poor | Significant issues |
| 0-29 | Critical | Urgent action needed |

### Per-Scope Scoring

Each of the 9 scopes receives an individual score. The overall EcoScore is a weighted average:

```
Overall = (CodeEff × 15 + Deps × 10 + Data × 10 + AI × 15 + Build × 10 +
           Frontend × 15 + Database × 10 + Network × 10 + Infra × 5) / 100
```

Weights reflect typical environmental impact. Adjust based on project type.

## Analysis Scopes

### 1. Code Efficiency

Analyze algorithmic complexity and resource usage patterns.

**Check for:**
- O(n²) or worse algorithms where O(n) possible
- Unnecessary iterations and redundant computations
- Memory allocation patterns (excessive object creation)
- Blocking operations that waste CPU cycles
- Inefficient string concatenation in loops

**Tools:** Static analysis, complexity metrics, profiling data

### 2. Dependencies

Analyze package bloat and alternatives.

**Check for:**
- Unused dependencies in package.json/requirements.txt
- Heavy packages with lighter alternatives (moment.js → date-fns)
- Duplicate functionality across dependencies
- Dependencies pulling large transitive trees
- Outdated packages with known inefficiencies

**Reference:** See `references/dependency-alternatives.md` for common swaps

### 3. Data Transfer

Analyze payload sizes and caching.

**Check for:**
- Uncompressed API responses
- Over-fetching (returning unused fields)
- Missing pagination on large datasets
- Redundant API calls that could be batched
- Missing cache headers

### 4. AI/LLM Usage

Analyze token efficiency and model selection.

**Check for:**
- Verbose prompts that could be compressed
- Missing prompt caching opportunities
- Using large models for simple tasks (Opus for summarization)
- Repeated identical queries without caching
- Streaming responses when batch would suffice

**Estimation:** ~0.0003 kg CO2e per 1K tokens (varies by provider/region)

**Reference:** See `references/ai-carbon-estimation.md` for detailed methodology

### 5. Build & CI/CD

Analyze build efficiency and artifact sizes.

**Check for:**
- Unnecessarily long build times
- Missing build caches
- Running full test suites on every commit
- Large artifacts uploaded to registries
- Redundant CI jobs that could be parallelized

### 6. Frontend/UX

Analyze client-side resource usage.

**Check for:**
- Unoptimized images (missing WebP/AVIF)
- Missing lazy loading for below-fold content
- Large JavaScript bundles blocking render
- Missing dark mode (OLED energy savings)
- Excessive DOM nodes impacting rendering
- Missing preload/prefetch hints

**Reference:** See `references/frontend-patterns.md` for optimization patterns

### 7. Database

Analyze query efficiency and storage.

**Check for:**
- Missing indexes on frequently queried columns
- SELECT * instead of specific columns
- N+1 query patterns
- Missing query result caching
- Excessive data retention without archival
- Unoptimized JOIN operations

### 8. Network

Analyze protocol and CDN usage.

**Check for:**
- HTTP/1.1 instead of HTTP/2 or HTTP/3
- Missing CDN for static assets
- No edge computing for region-specific logic
- Individual requests instead of batching
- Missing compression (gzip/brotli)

### 9. Infrastructure

Analyze cloud resource efficiency.

**Check for:**
- Over-provisioned instances (low CPU utilization)
- Resources in high-carbon regions
- Missing auto-scaling policies
- Always-on resources that could be serverless
- Missing spot/preemptible instances for batch jobs

**Reference:** See `references/carbon-regions.md` for regional carbon intensity

## Analysis Process

### Step 1: Gather Context

Read project configuration files:
- `package.json`, `requirements.txt`, `go.mod` (dependencies)
- `.env`, config files (infrastructure hints)
- CI/CD configs (`.github/workflows/`, `Dockerfile`)
- Build configs (webpack, vite, tsconfig)

### Step 2: Run Static Analysis

For each applicable scope:
1. Identify relevant files using Glob
2. Search for anti-patterns using Grep
3. Read flagged files for context
4. Score based on findings

### Step 3: Run Benchmarks (if requested)

For full analysis with benchmarks:
- Build the project and measure time/size
- Run test suite and measure duration
- Analyze bundle sizes
- Profile startup time if applicable

### Step 4: Calculate Scores

For each scope:
1. Count issues found
2. Weight by severity (critical=3, major=2, minor=1)
3. Calculate: `Score = 100 - min(100, weighted_issues × 5)`
4. Record specific issues for checklist

### Step 5: Generate Checklist

Output prioritized actionable items:

```markdown
## EcoScore Report

**Overall Score: 67/100** (Fair)

### Priority Actions

1. **[Critical] Replace moment.js with date-fns** (Dependencies: -15 points)
   - Location: package.json
   - Impact: Reduces bundle by 200KB
   - Fix: `npm uninstall moment && npm install date-fns`

2. **[Major] Add index to users.email column** (Database: -10 points)
   - Location: src/models/user.ts
   - Impact: 10x faster user lookups
   - Fix: Add migration with index creation
```

## Utility Scripts

### Analysis Helpers

Located in `scripts/`:

- **`analyze-dependencies.sh`** - Scan for unused/heavy dependencies
- **`estimate-carbon.py`** - Calculate carbon estimates from metrics

Execute scripts using:
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/green-it-analysis/scripts/analyze-dependencies.sh
```

## Quick Reference Tables

### Common Anti-Patterns by Scope

| Scope | Anti-Pattern | Better Alternative |
|-------|--------------|-------------------|
| Code | Nested loops O(n²) | Hash maps O(n) |
| Deps | moment.js (300KB) | date-fns (13KB) |
| Data | No pagination | Cursor pagination |
| AI | GPT-4 for classification | GPT-3.5 or fine-tuned |
| Build | No cache | Layer caching |
| Frontend | PNG images | WebP/AVIF |
| Database | SELECT * | SELECT specific cols |
| Network | HTTP/1.1 | HTTP/2+ |
| Infra | us-east-1 always | eu-west-1 (greener) |

### Carbon Intensity by Region

| Region | gCO2/kWh | Rating |
|--------|----------|--------|
| eu-north-1 (Sweden) | 8 | Excellent |
| eu-west-1 (Ireland) | 316 | Good |
| us-west-2 (Oregon) | 78 | Good |
| us-east-1 (Virginia) | 379 | Fair |
| ap-south-1 (Mumbai) | 708 | Poor |

## Additional Resources

### Reference Files

For detailed patterns and methodologies:

- **`references/dependency-alternatives.md`** - Heavy packages and lightweight alternatives
- **`references/ai-carbon-estimation.md`** - AI/LLM carbon calculation methodology
- **`references/frontend-patterns.md`** - Frontend optimization patterns
- **`references/carbon-regions.md`** - Cloud region carbon intensity data

### Scripts

- **`scripts/analyze-dependencies.sh`** - Dependency analysis utility
- **`scripts/estimate-carbon.py`** - Carbon estimation calculator

## Integration with Commands

This skill provides the knowledge base for:

- `/ecoscore:analyze` - Full analysis using all scopes
- `/ecoscore:quick-check` - Fast static analysis only
- `/ecoscore:report` - Generate formatted checklist

Commands will load this skill automatically when executing.
