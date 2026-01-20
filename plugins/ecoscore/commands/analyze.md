---
description: Full environmental impact analysis with benchmarks
allowed-tools: Read, Glob, Grep, Bash(npm:*, node:*, python:*, pip:*, go:*, cargo:*, git:*)
argument-hint: [scope]
---

Perform comprehensive environmental impact analysis of this codebase using Green IT principles.

## Analysis Configuration

Optional scope filter: $ARGUMENTS (if empty, analyze all scopes)

## Analysis Process

### Phase 1: Project Discovery

Identify project type and gather context:
1. Find package managers: package.json, requirements.txt, go.mod, Cargo.toml
2. Check CI/CD configs: .github/workflows/, Dockerfile, docker-compose.yml
3. Identify frameworks and major dependencies
4. Note cloud/infrastructure configurations

### Phase 2: Static Analysis (All 9 Scopes)

**1. Code Efficiency**
- Search for O(n²) patterns (nested loops over same collection)
- Find synchronous blocking operations
- Identify inefficient string operations in loops

**2. Dependencies**
- Count total dependencies
- Flag heavy packages (moment, lodash full, axios when fetch works)
- Check for unused dependencies patterns

**3. Data Transfer**
- Find API endpoints returning full objects (SELECT *)
- Check for missing pagination patterns
- Look for uncompressed response patterns

**4. AI/LLM Usage**
- Find AI SDK imports (openai, anthropic, @google/generative-ai)
- Check for hardcoded large model names
- Look for missing caching around AI calls

**5. Build & CI/CD**
- Analyze CI workflow complexity
- Check for build caching configuration
- Measure Dockerfile layer efficiency

**6. Frontend/UX**
- Check image formats (png vs webp/avif)
- Find lazy loading patterns (or lack thereof)
- Check for dark mode support
- Analyze bundle configuration

**7. Database**
- Find SELECT * patterns
- Check for N+1 query patterns
- Look for missing index hints

**8. Network**
- Check for HTTP/2 configuration
- Find CDN configuration
- Look for request batching patterns

**9. Infrastructure**
- Check cloud region configuration
- Find resource sizing hints
- Look for auto-scaling configuration

### Phase 3: Benchmarks (if applicable)

Run measurements where possible:
- Build time: Execute build and measure
- Bundle size: Check dist/build output sizes
- Test suite duration: Run tests and measure
- Startup time: If entry point identifiable

### Phase 4: Score Calculation

For each scope:
1. Count issues by severity (critical=3, major=2, minor=1)
2. Calculate: Score = 100 - min(100, weighted_issues × 5)
3. Apply scope weights for overall score

### Phase 5: Generate Report

Output format:
```
## EcoScore Analysis Report

**Overall Score: XX/100** (Rating)

### Scope Breakdown
| Scope | Score | Issues |
|-------|-------|--------|
| Code Efficiency | XX | X critical, X major |
| Dependencies | XX | ... |
...

### Critical Issues (fix first)
1. [Location] Issue description - Impact estimate

### Major Issues
...

### Minor Issues
...

### Benchmark Results
- Build time: Xs
- Bundle size: XMB
...
```

Use the green-it-analysis skill knowledge for scoring methodology and anti-pattern detection.
