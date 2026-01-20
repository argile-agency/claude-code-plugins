# Frontend Optimization Patterns

Patterns for reducing environmental impact of frontend applications.

## Image Optimization

### Format Selection

| Format | Use Case | Savings vs PNG |
|--------|----------|----------------|
| WebP | General images, photos | 25-35% |
| AVIF | High quality photos | 50%+ |
| SVG | Icons, logos, simple graphics | 90%+ |
| CSS | Simple shapes, gradients | 99% |

### Responsive Images

```html
<!-- Anti-pattern: single large image -->
<img src="hero-4k.jpg">

<!-- Optimized: responsive with modern formats -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img
    src="hero.jpg"
    srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
    loading="lazy"
    decoding="async"
    alt="Hero image">
</picture>
```

### Lazy Loading

```html
<!-- Native lazy loading for images -->
<img src="photo.jpg" loading="lazy" alt="...">

<!-- Native lazy loading for iframes -->
<iframe src="video.html" loading="lazy"></iframe>
```

**Impact:** Images below fold don't load until needed, saving bandwidth.

## JavaScript Optimization

### Bundle Size Reduction

**Code splitting:**
```javascript
// Anti-pattern: single large bundle
import { everything } from 'huge-library';

// Optimized: dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

**Tree shaking:**
```javascript
// Anti-pattern: import entire library
import _ from 'lodash';

// Optimized: import only needed functions
import { debounce } from 'lodash-es';
// Or even better: native implementation
```

### Execution Efficiency

**Debouncing/throttling:**
```javascript
// Anti-pattern: runs on every keystroke
input.addEventListener('input', expensiveSearch);

// Optimized: debounced
input.addEventListener('input', debounce(expensiveSearch, 300));
```

**RequestAnimationFrame:**
```javascript
// Anti-pattern: continuous DOM updates
setInterval(updatePosition, 16);

// Optimized: synced with display refresh
function animate() {
  updatePosition();
  requestAnimationFrame(animate);
}
```

## CSS Optimization

### Render Performance

**Avoid layout thrashing:**
```javascript
// Anti-pattern: causes multiple reflows
elements.forEach(el => {
  el.style.width = el.offsetWidth + 10 + 'px';
});

// Optimized: batch reads and writes
const widths = elements.map(el => el.offsetWidth);
elements.forEach((el, i) => {
  el.style.width = widths[i] + 10 + 'px';
});
```

**Use transform/opacity for animations:**
```css
/* Anti-pattern: triggers layout */
.animate {
  left: 100px;
  width: 200px;
}

/* Optimized: GPU-accelerated, no layout */
.animate {
  transform: translateX(100px) scale(1.1);
  opacity: 0.8;
}
```

### Critical CSS

```html
<!-- Inline critical CSS -->
<style>
  /* Above-fold styles only */
  .hero { ... }
  .nav { ... }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'">
```

## Dark Mode Energy Savings

### OLED Displays

Dark pixels on OLED displays use less energy:
- Pure black (#000000): 0% power for that pixel
- Dark gray (#1a1a1a): ~10% power
- White (#ffffff): 100% power

**Potential savings:** 30-60% display energy on OLED devices

### Implementation

```css
/* Respect system preference */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117;
    --text: #c9d1d9;
  }
}

/* Use true black for maximum OLED savings */
.dark-mode {
  background-color: #000000;
}
```

### Detection Pattern

```javascript
// Flag: no dark mode support
// Check for: @media (prefers-color-scheme: dark) in CSS
// Check for: dark mode toggle in UI
```

## Network Optimization

### Resource Hints

```html
<!-- Preconnect to required origins -->
<link rel="preconnect" href="https://api.example.com">

<!-- Prefetch likely next pages -->
<link rel="prefetch" href="/likely-next-page.html">

<!-- Preload critical resources -->
<link rel="preload" href="critical.css" as="style">
<link rel="preload" href="hero.webp" as="image">
```

### Service Workers

```javascript
// Cache static assets
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request);
    })
  );
});
```

**Impact:** Subsequent visits use cached resources, zero network for static assets.

## DOM Optimization

### Virtual Lists

```javascript
// Anti-pattern: render 10,000 items
items.map(item => <ListItem key={item.id} {...item} />)

// Optimized: virtualized list (only render visible)
<VirtualList
  height={400}
  itemCount={items.length}
  itemSize={50}
  renderItem={({ index }) => <ListItem {...items[index]} />}
/>
```

### Fragment Usage

```javascript
// Anti-pattern: wrapper divs
return (
  <div>
    <Header />
    <Content />
  </div>
);

// Optimized: fragments
return (
  <>
    <Header />
    <Content />
  </>
);
```

## Scoring Rubric

### Frontend Score (0-100)

| Criteria | Points |
|----------|--------|
| Modern image formats (WebP/AVIF) | 15 |
| Lazy loading implemented | 10 |
| Bundle size < 200KB (gzipped) | 15 |
| Code splitting used | 10 |
| Dark mode support | 10 |
| Resource hints configured | 10 |
| Service worker caching | 10 |
| Optimized CSS animations | 10 |
| Virtual lists for long data | 10 |

### Detection Checklist

- [ ] Images use WebP/AVIF with fallbacks
- [ ] `loading="lazy"` on below-fold images
- [ ] JavaScript bundle < 200KB gzipped
- [ ] Dynamic imports for heavy components
- [ ] `prefers-color-scheme` media query exists
- [ ] `preconnect`/`prefetch` hints present
- [ ] Service worker registered
- [ ] No layout-thrashing patterns
- [ ] Large lists use virtualization
