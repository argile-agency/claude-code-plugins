# Dependency Alternatives Guide

Lightweight alternatives to common heavy dependencies.

## JavaScript/Node.js

### Date/Time Libraries

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| moment.js | 300KB | date-fns | 13KB | 96% |
| moment.js | 300KB | dayjs | 2KB | 99% |
| moment-timezone | 900KB | luxon | 70KB | 92% |

### Utility Libraries

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| lodash (full) | 530KB | lodash-es (tree-shake) | varies | 80%+ |
| lodash | 530KB | native ES6+ | 0KB | 100% |
| underscore | 60KB | native ES6+ | 0KB | 100% |
| ramda | 230KB | native + small utils | varies | 90%+ |

### HTTP Clients

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| axios | 45KB | fetch (native) | 0KB | 100% |
| request (deprecated) | 1.2MB | node-fetch | 8KB | 99% |
| superagent | 60KB | ky | 10KB | 83% |

### UI Component Libraries

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| antd | 1.2MB | headlessui + tailwind | 50KB | 96% |
| material-ui | 800KB | radix-ui | 100KB | 87% |
| bootstrap | 300KB | tailwindcss | tree-shaken | 90%+ |

### Form Libraries

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| formik | 45KB | react-hook-form | 10KB | 78% |
| redux-form | 70KB | react-hook-form | 10KB | 86% |

### State Management

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| redux + toolkit | 60KB | zustand | 3KB | 95% |
| mobx | 55KB | jotai | 4KB | 93% |
| recoil | 70KB | zustand | 3KB | 96% |

### Validation

| Heavy Package | Size | Alternative | Size | Savings |
|--------------|------|-------------|------|---------|
| joi | 140KB | zod | 13KB | 91% |
| yup | 40KB | zod | 13KB | 68% |
| ajv | 120KB | valibot | 6KB | 95% |

## Python

### Data Processing

| Heavy Package | Note | Alternative | When to Use |
|--------------|------|-------------|-------------|
| pandas | Large, C deps | polars | Large datasets |
| pandas | Large | built-in csv | Simple CSV ops |
| numpy | Large, C deps | list comprehensions | Simple math |

### HTTP

| Heavy Package | Note | Alternative | When to Use |
|--------------|------|-------------|-------------|
| requests | External dep | httpx | Async support needed |
| requests | External dep | urllib3 | Already a dep |
| aiohttp | Large | httpx | Simpler API |

### CLI

| Heavy Package | Note | Alternative | When to Use |
|--------------|------|-------------|-------------|
| click | Large | typer | Modern, typing |
| argparse | Built-in but verbose | typer | Better UX |

## Detection Patterns

### Finding Unused Dependencies

```bash
# JavaScript - find unused deps
npx depcheck

# Python - find unused imports
pip install vulture && vulture .

# General - check import statements vs dependencies
```

### Finding Heavy Dependencies

```bash
# JavaScript - analyze bundle
npx bundle-analyzer
npx source-map-explorer

# Check package size before install
npx package-size <package-name>
```

### Native Replacements

Many lodash functions have native equivalents:

```javascript
// Instead of: _.map(arr, fn)
arr.map(fn)

// Instead of: _.filter(arr, fn)
arr.filter(fn)

// Instead of: _.find(arr, fn)
arr.find(fn)

// Instead of: _.includes(arr, val)
arr.includes(val)

// Instead of: _.flatten(arr)
arr.flat()

// Instead of: _.flattenDeep(arr)
arr.flat(Infinity)

// Instead of: _.uniq(arr)
[...new Set(arr)]

// Instead of: _.groupBy(arr, key)
Object.groupBy(arr, item => item[key])  // ES2024
```

## Migration Checklist

When replacing a dependency:

1. [ ] Identify all import locations
2. [ ] Check for feature parity needed
3. [ ] Update imports progressively
4. [ ] Run tests after each file migration
5. [ ] Remove old package after full migration
6. [ ] Update lockfile and verify bundle size reduction
