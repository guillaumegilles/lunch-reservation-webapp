# Contract: CSS Design Token API

**Feature**: `002-modern-website-styling`
**File**: `reservations/static/custom.css`
**Contract type**: CSS custom-property public interface

> This document defines the stable public surface of the design system. Any template or future CSS that references tokens listed here may do so without risk of breakage. Tokens not listed here are considered internal implementation details and may change.

---

## Stable Token API

### Colour Tokens

```css
/* === PUBLIC: safe to reference in templates or future CSS === */

--color-primary          /* Berry — primary actions, links */
--color-primary-dark     /* Plum — headings, hover states */
--color-accent           /* Apricot — secondary/success actions */
--color-bg               /* Warm off-white — page background */
--color-surface          /* Warm white — card / panel background */
--color-surface-success  /* Sun-tinted — success/info alert surface */
--color-surface-error    /* Berry-tinted — error/danger/warning alert surface */
--color-navbar-bg        /* Berry fill — navbar background */
--color-navbar-text      /* Near-white — navbar text/icons */
--color-text             /* Ink — body text */
--color-text-muted       /* Muted ink — secondary labels */
--color-border           /* Plum-tinted — borders */
--color-focus-ring       /* Berry-tinted — focus ring glow */
```

### Typography Tokens

```css
--font-heading           /* "Archivo Black" + fallback stack */
--font-body              /* "DM Sans" + fallback stack */
--font-size-sm           /* 0.875rem */
--font-size-base         /* 1rem */
--font-size-lg           /* 1.125rem */
--font-size-xl           /* 1.5rem */
--font-size-2xl          /* 2rem */
--font-weight-normal     /* 400 */
--font-weight-medium     /* 500 */
--font-weight-bold       /* 700 */
```

### Shape & Spacing Tokens

```css
--space-xs   /* 0.25rem */
--space-sm   /* 0.5rem */
--space-md   /* 1rem */
--space-lg   /* 1.5rem */
--space-xl   /* 2rem */
--space-2xl  /* 3rem */

--radius-sm  /* 8px */
--radius-md  /* 12px */
--radius-lg  /* 16px */
--radius-pill /* 999px — buttons */

--shadow-card   /* soft card drop shadow */
--shadow-navbar /* navbar bottom shadow */
--shadow-focus  /* focus ring box-shadow */

--transition-fast /* 0.15s ease — all interactive transitions */
```

---

## Usage Contract

### In Django templates

Templates MUST NOT reference specific hex colour values. They MAY reference token names via inline style only if necessary (e.g., a one-off background on a dynamically generated element). However, the preferred pattern is always to add a class to `custom.css` and apply the class.

```html
<!-- ✅ Correct: use a CSS class -->
<div class="alert alert-danger">...</div>

<!-- ❌ Incorrect: hardcoded hex -->
<div style="background:#fce8ef;color:#2f1638">...</div>
```

### In `custom.css`

All CSS rules in `custom.css` that set a colour, spacing, radius, or shadow MUST reference a token:

```css
/* ✅ Correct */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
}

/* ❌ Incorrect */
.card {
  background: #fffaf1;
  border: 1px solid rgba(106,44,112,0.15);
}
```

### Bootstrap class compatibility

The following Bootstrap utility classes produce token-consistent output after the `:root` remapping:

| Bootstrap class | Rendered using token |
|----------------|---------------------|
| `.text-primary` | `--color-primary` |
| `.bg-primary` | `--color-primary` |
| `.btn-primary` | `--color-primary` background |
| `.text-muted` | `--color-text-muted` |
| `.text-body` | `--color-text` |
| `.bg-body` | `--color-bg` |
| `.border` | `--color-border` |
| `.rounded` | `--radius-md` |

---

## Breaking-change policy

- Renaming any token listed above is a **breaking change** and requires updating all consumers (templates + custom.css rules).
- Adding new tokens is non-breaking.
- Removing unused tokens is non-breaking if no template references them.
- Changing a token's *value* (e.g., retuning `--color-primary` hex) is non-breaking for structure but may affect visual QA and accessibility — a contrast re-audit is required.

---

## Excluded from public API (internal / unstable)

```css
--color-accent-hover     /* internal hover calculation */
--color-sun              /* decorative only; do not use as text or border */
```
