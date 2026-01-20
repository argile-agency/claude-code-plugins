---
description: Generate prioritized actionable improvement checklist
allowed-tools: Read, Glob, Grep
argument-hint: [format]
---

Generate a prioritized actionable checklist for environmental improvements.

Output format preference: $ARGUMENTS (default: markdown, options: markdown, json, minimal)

## Report Generation Process

### Step 1: Load Previous Analysis

Check if recent analysis exists in conversation context. If not, perform quick static analysis to identify issues.

### Step 2: Prioritize by Impact

Rank all identified issues by environmental impact:

**Impact Scoring:**
- Carbon reduction potential (high/medium/low)
- Effort to implement (quick/moderate/significant)
- Scope of improvement (localized/widespread)

**Priority Formula:**
```
Priority = (Carbon_Impact × 3) + (Effort_Inverse × 2) + (Scope × 1)
```

### Step 3: Generate Actionable Items

For each issue, provide:
1. **What**: Clear description of the problem
2. **Where**: Specific file(s) and line number(s)
3. **Why**: Environmental impact explanation
4. **How**: Step-by-step fix instructions
5. **Impact**: Estimated carbon/efficiency improvement

### Step 4: Format Output

**Markdown format (default):**
```markdown
# EcoScore Improvement Checklist

Generated: [date]
Project: [name]
Current Score: XX/100

## Priority 1: Quick Wins (High Impact, Low Effort)

### 1. Replace moment.js with date-fns
- **Location**: package.json, src/utils/date.ts
- **Impact**: -287KB bundle size, ~15% faster builds
- **Effort**: 1-2 hours
- **Steps**:
  1. `npm uninstall moment`
  2. `npm install date-fns`
  3. Update imports in src/utils/date.ts
  4. Replace moment() calls with date-fns equivalents

### 2. ...

## Priority 2: Medium Effort Improvements

...

## Priority 3: Larger Refactoring

...

## Summary

| Priority | Count | Est. Score Impact |
|----------|-------|-------------------|
| Quick Wins | X | +Y points |
| Medium | X | +Y points |
| Larger | X | +Y points |

**Potential new score: XX/100**
```

**JSON format:**
```json
{
  "generated": "ISO-date",
  "currentScore": 65,
  "potentialScore": 82,
  "items": [
    {
      "priority": 1,
      "title": "Replace moment.js",
      "category": "dependencies",
      "location": ["package.json", "src/utils/date.ts"],
      "impact": "high",
      "effort": "low",
      "scoreImpact": 5,
      "steps": ["...", "..."]
    }
  ]
}
```

**Minimal format:**
```
EcoScore: 65 → 82 (potential)

Quick Wins:
[ ] Replace moment.js with date-fns (dependencies)
[ ] Add lazy loading to images (frontend)
[ ] Use WebP format for hero.png (frontend)

Medium Effort:
[ ] Add Redis caching for AI responses (ai-usage)
[ ] Implement cursor pagination (data-transfer)
```

Use green-it-analysis skill for impact estimation methodology.
