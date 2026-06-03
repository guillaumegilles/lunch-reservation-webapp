# Data Model: Design System

**Feature**: `002-modern-website-styling`
**Phase**: 1 — Design

> In this purely front-end feature, "entities" are the CSS design tokens (custom properties) and component-style definitions that make up the design system. There are no database schema changes.

---

## Entity 1 — Design Tokens (`:root` custom properties)

All values live in the `:root` block of `custom.css`. No value may be hardcoded elsewhere in the file — every rule must reference a token.

### 1.1 Colour Tokens

| Token | Value | Role | WCAG note |
|-------|-------|------|-----------|
| `--color-primary` | `#B83B5E` | Primary action (buttons, links, navbar) | 5.49:1 on white ✅ |
| `--color-primary-dark` | `#6A2C70` | Primary hover / heading text | 9.51:1 on white ✅ |
| `--color-accent` | `#F08A5D` | Secondary/success action bg | Use with `--color-text` (6.57:1) ✅ |
| `--color-accent-hover` | `#d96e3f` | Secondary action hover | Darker apricot |
| `--color-sun` | `#F9ED69` | Decorative accent only — **never use as text colour** | N/A |
| `--color-bg` | `#fff7f0` | Page body background (warm off-white) | — |
| `--color-surface` | `#fffaf1` | Card, table, alert surfaces | — |
| `--color-surface-success` | `#fffbdd` | Success / info alert background | 15:1 with `--color-text` ✅ |
| `--color-surface-error` | `#fce8ef` | Error / danger / warning alert background | 13.6:1 with `--color-text` ✅ |
| `--color-navbar-bg` | `#B83B5E` | Navbar solid fill (berry) | — |
| `--color-navbar-text` | `#ffe8ee` | Navbar text / icon (near-white) | ~7:1 on navbar bg ✅ |
| `--color-text` | `#2f1638` | Body text (ink) | 15.62:1 on `--color-surface` ✅ |
| `--color-text-muted` | `rgba(47,22,56,0.58)` | Secondary / muted text | Use only for large text or decorative labels |
| `--color-border` | `rgba(106,44,112,0.15)` | Card, form, table borders | Subtle plum tint |
| `--color-focus-ring` | `rgba(184,59,94,0.35)` | Focus ring colour for form controls and buttons | — |

### 1.2 Typography Tokens

| Token | Value | Role |
|-------|-------|------|
| `--font-heading` | `"Archivo Black", "Arial Black", system-ui, sans-serif` | H1–H6, `.card-title` |
| `--font-body` | `"DM Sans", "Helvetica Neue", Arial, sans-serif` | Body, inputs, buttons |
| `--font-size-base` | `1rem` | 16 px equivalent |
| `--font-size-sm` | `0.875rem` | Small / caption text |
| `--font-size-lg` | `1.125rem` | Large body / sub-headings |
| `--font-size-xl` | `1.5rem` | Page section titles |
| `--font-size-2xl` | `2rem` | Hero / page title (H1) |
| `--line-height-base` | `1.6` | Body text |
| `--line-height-heading` | `1.2` | Headings |
| `--letter-spacing-heading` | `0.03em` | Heading tracking |
| `--font-weight-normal` | `400` | — |
| `--font-weight-medium` | `500` | — |
| `--font-weight-bold` | `700` | Button labels, emphasis |

### 1.3 Spacing Tokens

| Token | Value | Role |
|-------|-------|------|
| `--space-xs` | `0.25rem` | 4 px — tight gaps |
| `--space-sm` | `0.5rem` | 8 px — small padding |
| `--space-md` | `1rem` | 16 px — standard padding |
| `--space-lg` | `1.5rem` | 24 px — section gaps |
| `--space-xl` | `2rem` | 32 px — page margins |
| `--space-2xl` | `3rem` | 48 px — hero spacing |

### 1.4 Shape & Shadow Tokens

| Token | Value | Role |
|-------|-------|------|
| `--radius-sm` | `8px` | Form inputs, small tags |
| `--radius-md` | `12px` | Cards, alerts |
| `--radius-lg` | `16px` | Calendar day cells |
| `--radius-pill` | `999px` | Buttons |
| `--shadow-card` | `0 2px 8px rgba(106,44,112,0.12)` | Card / container drop shadow |
| `--shadow-navbar` | `0 2px 6px rgba(106,44,112,0.18)` | Navbar bottom shadow |
| `--shadow-focus` | `0 0 0 0.22rem var(--color-focus-ring)` | Focus ring box-shadow |
| `--transition-fast` | `0.15s ease` | Hover / focus state transitions (≤ 200 ms per SC-004) |

---

## Entity 2 — Component Styles

Each component maps to one or more Bootstrap classes that `custom.css` overrides. All values reference tokens.

### 2.1 Navbar

| Property | Value / Token |
|----------|--------------|
| Background | `var(--color-navbar-bg)` |
| Text / icon colour | `var(--color-navbar-text)` |
| Position | `sticky top: 0` |
| Bottom shadow | `var(--shadow-navbar)` |
| Brand font | `var(--font-heading)` |
| Brand font-size | `var(--font-size-lg)` |
| Padding (block) | `var(--space-sm) var(--space-md)` |

**Template addition in `base.html`**:
```html
<nav class="navbar navbar-dark sticky-top" style="...">  <!-- no inline; class only -->
  <div class="container-fluid">
    <a class="navbar-brand" href="/">🍽 Lunch Réservation</a>
    {% if user.is_authenticated %}
    <a class="btn btn-outline-light btn-sm" href="{% url 'logout' %}">Se déconnecter</a>
    {% endif %}
  </div>
</nav>
```

### 2.2 Card / Container

| Property | Value / Token |
|----------|--------------|
| Background | `var(--color-surface)` (opaque) |
| Border | `1px solid var(--color-border)` |
| Border radius | `var(--radius-md)` |
| Box shadow | `var(--shadow-card)` |
| `backdrop-filter` | **none** (glassmorphism removed) |
| Padding | Bootstrap default via `card-body` |

### 2.3 Buttons

| Variant | BG | Text | Border | Hover BG |
|---------|----|----|--------|---------|
| `.btn-primary` | `--color-primary` | `--color-navbar-text` | `--color-primary` | `--color-primary-dark` |
| `.btn-success` | `--color-accent` | `--color-text` | `--color-accent` | `--color-accent-hover` |
| `.btn-outline-primary` | transparent | `--color-primary-dark` | `--color-primary-dark` | `--color-primary-dark` fill |
| `.btn-outline-secondary` | transparent | `--color-primary` | `--color-border` solid 2px | `--color-surface-success` fill |
| `.btn-outline-danger` | transparent | `--color-primary` | `--color-primary` | `--color-surface-error` fill |
| `.btn-outline-light` | transparent | `--color-navbar-text` | `--color-navbar-text` | white/10% fill |

Common button properties:
- Border radius: `var(--radius-pill)`
- Font weight: `var(--font-weight-bold)`
- Transition: `var(--transition-fast)`
- Min tap height (mobile): `44px` (enforced via `min-height: 44px` at ≤ 576 px)

### 2.4 Form Controls

| Property | Value / Token |
|----------|--------------|
| Border | `1.5px solid var(--color-border)` |
| Border radius | `var(--radius-sm)` |
| Background | `#ffffff` |
| Focus border | `var(--color-accent)` |
| Focus box-shadow | `var(--shadow-focus)` |
| Padding | `0.6rem 0.9rem` |

### 2.5 Alerts

| Variant | Background | Text | Left border |
|---------|-----------|------|------------|
| `.alert-success`, `.alert-info` | `var(--color-surface-success)` | `var(--color-text)` | `3px solid var(--color-primary-dark)` |
| `.alert-danger`, `.alert-warning`, `.alert-error` | `var(--color-surface-error)` | `var(--color-text)` | `3px solid var(--color-primary)` |

All alerts: border radius `var(--radius-md)`, box-shadow `var(--shadow-card)`.

### 2.6 Table

| Property | Value / Token |
|----------|--------------|
| Container border radius | `var(--radius-md)` |
| Container overflow | `hidden` (clips thead corners) |
| `thead th` background | `var(--color-primary-dark)` (plum) |
| `thead th` text | `var(--color-navbar-text)` |
| Striped odd row | `rgba(249,237,105,0.12)` (sun tint) |
| Cell border colour | `var(--color-border)` |
| Container box-shadow | `var(--shadow-card)` |
| `backdrop-filter` | none |

### 2.7 Calendar Day Cells

| State | Style |
|-------|-------|
| Default (`.selectable-day`) | `background: var(--color-surface)` · `border: 1.5px solid var(--color-border)` · `border-radius: var(--radius-lg)` · `box-shadow: var(--shadow-card)` |
| Hover | `border-color: var(--color-accent)` · `transform: translateY(-1px)` |
| Selected (`.bg-primary`) | `background: var(--color-primary)` → `var(--color-primary-dark)` flat fill · `color: var(--color-navbar-text)` |
| Locked (`.locked-day`) | `opacity: 0.45` · `cursor: default` (moved from `calendar.html` inline `<style>`) |

---

## Entity 3 — Breakpoints

Three breakpoints align exactly with Bootstrap 5's `sm` and `lg`:

| Name | Range | Media Query |
|------|-------|------------|
| Mobile | ≤ 575.98 px | `@media (max-width: 575.98px)` |
| Tablet | 576–991.98 px | `@media (min-width: 576px) and (max-width: 991.98px)` |
| Desktop | ≥ 992 px | Bootstrap default (no override needed) |

**Mobile-specific rules** (inside `@media (max-width: 575.98px)`):
- `.btn { min-height: 44px; }` — SC-003 tap target
- Reduce card / alert border-radius to `var(--radius-sm)` for tighter mobile feel
- Reduce heading sizes by one step for viewport fit

---

## Entity 4 — File Structure

```text
reservations/static/custom.css
│
├── /* === 1. DESIGN TOKENS === */        ← :root { --color-* --font-* --space-* --radius-* --shadow-* --transition-* }
├── /* === 2. GLOBAL RESET === */         ← body, a, h1-h6
├── /* === 3. NAVBAR === */               ← .navbar override
├── /* === 4. CARDS & CONTAINERS === */   ← .card, .card-body, .table-responsive
├── /* === 5. BUTTONS === */              ← .btn, .btn-primary, .btn-success, etc.
├── /* === 6. FORM CONTROLS === */        ← .form-control, .form-select
├── /* === 7. ALERTS === */               ← .alert, .alert-success, .alert-danger, etc.
├── /* === 8. TABLE === */                ← .table, thead th, striped rows
├── /* === 9. CALENDAR === */             ← .selectable-day, .locked-day, .calendar-day, #statusMsg
└── /* === 10. RESPONSIVE === */          ← @media (max-width: 575.98px)
```

### Validation rules

- Every CSS colour value MUST reference a `var(--*)` token — no hex literals outside `:root`
- No `backdrop-filter` rules permitted
- No `background: linear-gradient(...)` or `radial-gradient(...)` on `.card`, `.alert`, `body`, or `.selectable-day`
- No `style=` attribute markup in templates
- All `transition` durations MUST be ≤ `var(--transition-fast)` (0.15s) to satisfy SC-004
