---
description: Fast static-only environmental scan
allowed-tools: Read, Glob, Grep
model: haiku
argument-hint: [path]
---

Perform a quick environmental impact check using static analysis only.

Target path: $ARGUMENTS (default: entire project)

## Quick Check Process

Focus on the highest-impact, fastest-to-detect issues:

### 1. Dependency Quick Scan

Check package.json or requirements.txt for known heavy packages:
- moment.js (suggest date-fns or dayjs)
- lodash full import (suggest lodash-es or native)
- axios (suggest native fetch)
- large UI frameworks without tree-shaking

### 2. Image Format Check

Search for image references:
- .png files that could be .webp
- .jpg files that could be .avif
- Missing lazy loading attributes

### 3. AI Model Usage

Quick scan for:
- Hardcoded "gpt-4" or "claude-opus" for simple tasks
- Missing response caching patterns

### 4. Database Patterns

Search for:
- SELECT * statements
- Missing LIMIT clauses

### 5. Bundle Size Indicators

Check for:
- Missing tree-shaking configuration
- Importing entire libraries vs specific functions

## Output Format

```
## EcoScore Quick Check

**Estimated Score: XX/100**

### Top 5 Issues Found

1. **[Critical]** Issue description
   - File: path/to/file.ts:line
   - Fix: Specific recommendation
   - Impact: Estimated improvement

2. **[Major]** ...

...

### Quick Wins
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

Run `/ecoscore:analyze` for full analysis with benchmarks.
```

Keep analysis fast - limit file reads, use Grep for pattern detection.
