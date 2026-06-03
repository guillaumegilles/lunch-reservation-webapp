# Research: Modern Website Styling

**Feature**: `002-modern-website-styling`
**Phase**: 0 — Pre-design research

---

## 1. Contrast Audit — Existing Palette on Flat Surfaces

### Context

The current `style.css` uses glassmorphism (semi-transparent card backgrounds + `backdrop-filter: blur(12px)`) and a radial/linear gradient body. When these are replaced by flat opaque surfaces (as mandated by FR-007), all text/background pairs must be re-evaluated against WCAG AA.

### Contrast Results

| Pair | Foreground | Background | Ratio | AA Normal (4.5:1) | AA Large/UI (3:1) |
|------|-----------|-----------|-------|-------------------|-------------------|
| Body text | `--ink` #2f1638 | `--paper` #fffaf1 | **15.62:1** | ✅ Pass | ✅ Pass |
| btn-primary label | #fff8f8 | `--berry` #B83B5E | **5.24:1** | ✅ Pass | ✅ Pass |
| btn-success label | `--ink` #2f1638 | `--apricot` #F08A5D | **6.57:1** | ✅ Pass | ✅ Pass |
| Link text | `--berry` #B83B5E | white #ffffff | **5.49:1** | ✅ Pass | ✅ Pass |
| Headings | `--plum` #6A2C70 | white #ffffff | **9.51:1** | ✅ Pass | ✅ Pass |
| alert-danger text | #fffaf1 | blended apricot #F29870* | **2.13:1** | ❌ Fail | ❌ Fail |

\* Blend of `rgba(240,138,93,0.88)` over white `#ffffff` → effective `#F29870`

### Identified Failures

**Only one pair fails: error/danger/warning alert.**

The current alert uses a `linear-gradient(apricot→berry)` with light (#fffaf1) text. On flat opaque surfaces the apricot end of that gradient produces ~2.13:1 contrast — a hard WCAG AA failure.

### Decision: Alert colour fix

- **Decision**: Error/danger/warning alerts MUST use a **solid dark surface** — specifically a light berry-tinted surface (`#fce8ef`, a mix of white and berry) — with `--ink` dark text.
  - `--ink` on `#fce8ef`: luminance of `#fce8ef` ≈ 0.81 → contrast ≈ (0.81+0.05)/(0.013+0.05) = 13.6:1 ✅
- Success/info alerts: light sun-tinted surface (`#fffbdd`) with `--ink` text — contrast ≈ 15:1 ✅
- Both alert styles get a coloured **left border** (3px solid) for semantic differentiation beyond colour alone.
- **Alternatives considered**: Keeping gradient background + switching to dark text (--ink). Rejected — still fails at apricot end because `--ink` on #fce8ef is safe but the gradient approach produces unpredictable intermediate values.

### Palette Stability

All other existing palette values are retained as-is for the flat minimal redesign:

| Token | Value | Role | Flat-surface safe? |
|-------|-------|------|--------------------|
| `--sun` | #F9ED69 | Decorative accent only (never as text) | ✅ (not used as text) |
| `--apricot` | #F08A5D | btn-success bg (with `--ink` text) | ✅ |
| `--berry` | #B83B5E | Primary action, link text, navbar bg | ✅ |
| `--plum` | #6A2C70 | Headings, navbar depth, focus rings | ✅ |
| `--ink` | #2f1638 | Body text, dark labels | ✅ |
| `--paper` | #fffaf1 | Page background, card surface | ✅ (used as bg) |

---

## 2. Bootstrap 5 Override Patterns

### Context

The project uses Bootstrap 5.3.2 loaded from CDN. Custom CSS must override Bootstrap component styles without a build step or Sass.

### Decision: Two-layer override strategy

1. **Layer 1 — Design tokens**: All colour, spacing, radius, shadow, and typography values are declared as CSS custom properties in `:root` (e.g., `--color-primary: #B83B5E`).

2. **Layer 2 — Bootstrap remapping**: Bootstrap 5.2+ exposes its own CSS custom properties (`--bs-primary`, `--bs-body-color`, etc.) at the `:root` level. Remapping these to point at our design tokens propagates changes into Bootstrap components automatically, without overriding every component class.

   ```css
   :root {
     --bs-primary: var(--color-primary);         /* propagates to .btn-primary, .text-primary, etc. */
     --bs-body-color: var(--color-text);          /* propagates to body text */
     --bs-body-bg: var(--color-bg);               /* propagates to body background */
     --bs-link-color: var(--color-primary);       /* propagates to <a> */
   }
   ```

3. **Layer 3 — Component overrides**: For visual treatments not covered by Bootstrap variables (card flat surface, navbar brand fill, alert surfaces, table header), direct class overrides are written in `custom.css` after the `:root` block.

- **Alternatives considered**: Rewriting all Bootstrap component classes from scratch. Rejected — fragile, duplicates Bootstrap's reset/utility logic, increases file size significantly.
- **Alternatives considered**: Loading a Bootstrap theme Sass source and compiling. Rejected — violates §III (no build step).

### Key Bootstrap variable remappings needed

| Bootstrap variable | Maps to our token | Effect |
|-------------------|------------------|--------|
| `--bs-primary` | `--color-primary` (berry) | Propagates to btn-primary, badge-primary, etc. |
| `--bs-body-color` | `--color-text` (ink) | Body text colour |
| `--bs-body-bg` | `--color-bg` (paper) | Page background |
| `--bs-link-color` | `--color-primary` | Link colour |
| `--bs-border-radius` | `--radius-md` | Default component border-radius |
| `--bs-card-bg` | `--color-surface` | Card background |
| `--bs-card-border-color` | `--color-border` | Card border |

### Components requiring direct class overrides (not covered by BS variables)

- `.navbar` — brand fill + sticky; BS variables only theme `.navbar-dark`/`.navbar-light` colours, not background fill
- `.table thead th` — plum background; BS doesn't expose a thead-bg variable
- `.alert-danger`, `.alert-success`, `.alert-warning`, `.alert-info` — custom solid surfaces
- `.selectable-day`, `.calendar-day` — application-specific classes
- `.btn-success` — remapped to apricot (Bootstrap's default green is unwanted)
- `.btn-outline-secondary` — remapped to berry outline (Bootstrap's default is grey)

---

## 3. Responsive Breakpoints

### Context

The spec defines: mobile ≤ 576 px, tablet 577–991 px, desktop ≥ 992 px.

### Decision: Align with Bootstrap 5 breakpoints

Bootstrap 5 breakpoints:

| Breakpoint | Prefix | Min-width |
|-----------|--------|-----------|
| Extra small | (none) | < 576 px |
| Small | `sm` | ≥ 576 px |
| Medium | `md` | ≥ 768 px |
| Large | `lg` | ≥ 992 px |
| Extra large | `xl` | ≥ 1200 px |

Mapping to the spec's three tiers:
- **Mobile** (≤ 576 px) → Bootstrap default / `@media (max-width: 575.98px)`
- **Tablet** (577–991 px) → Bootstrap `sm` and `md` ranges / `@media (min-width: 576px) and (max-width: 991.98px)`
- **Desktop** (≥ 992 px) → Bootstrap `lg` / `@media (min-width: 992px)`

Custom media queries in `custom.css` will use these exact boundaries. Bootstrap's responsive grid utilities (`col-sm-*`, `col-lg-*`) already honour these breakpoints, so no additional grid overrides are needed.

- **Alternatives considered**: Defining completely custom breakpoints. Rejected — would conflict with Bootstrap's grid class names used in existing templates.

---

## 4. Navbar Addition

### Context

The current `base.html` has no navbar — it renders a plain container with messages and a content block. The spec requires a sticky, coloured brand navbar (FR-013).

### Decision: Minimal Bootstrap navbar in `base.html`

Add a `<nav class="navbar navbar-dark sticky-top">` above the main container in `base.html`. It will contain:
- Brand name / logo text ("Lunch Reservation") linking to `/`
- Logout button (visible when user is authenticated: `{% if user.is_authenticated %}`)

This removes the per-page logout buttons scattered across `calendar.html` and `dashboard.html`. Those buttons can be left in place as secondary actions (per FR-009 — no functionality removed) or kept for redundancy; the navbar provides the canonical logout.

The navbar background is set via `--color-navbar-bg` (berry → plum gradient or solid berry fill — spec says solid fill).

- **Alternatives considered**: Adding navbar markup to each individual template. Rejected — `base.html` is the correct single point; individual templates should not duplicate structural chrome.

---

## 5. Glassmorphism Removal

### Context

Current `style.css` uses `backdrop-filter: blur(12px)` and `rgba(255, 250, 241, 0.88)` semi-transparent fills on cards, tables, and alerts. FR-007 explicitly excludes glassmorphism.

### Decision: Replace with flat opaque surface tokens

| Element | Old value | New value |
|---------|-----------|-----------|
| Card / table-responsive / alert background | `rgba(255,250,241,0.88)` + `backdrop-filter:blur` | `var(--color-surface)` = solid `#fffaf1` |
| Body background | radial + linear gradient | `var(--color-bg)` = solid `#fffaf1` (same as paper, or a slightly warmer tint `#fff7f0`) |
| `.selectable-day` background | `rgba(255,255,255,0.76)` | `var(--color-surface)` = solid `#ffffff` |
| Card / selectable-day shadow | `0 18px 45px rgba(106,44,112,0.18)` | `0 2px 8px rgba(106,44,112,0.12)` (softer, flatter) |

The grid overlay (`.app-shell::before` pseudo-element) is also removed — it is a decorative artifact of the glassmorphism era and is not compatible with flat minimal.

---

## 6. File Naming — `style.css` → `custom.css`

### Context

Constitution §III specifies `reservations/static/style.css`. Spec FR-012 specifies `custom.css`. See Complexity Tracking in `plan.md`.

### Decision

- Create `reservations/static/custom.css` as the new canonical stylesheet.
- Delete (or empty) `reservations/static/style.css`.
- Update the `<link>` in `base.html` from `{% static 'style.css' %}` to `{% static 'custom.css' %}`.
- **Alternatives considered**: Keeping filename as `style.css` and ignoring FR-012. Rejected — the spec explicitly names `custom.css` as the deliverable.

---

## Summary of Decisions

| Topic | Decision |
|-------|---------|
| Alert contrast fix | Solid tinted surface + `--ink` text + coloured left border |
| Bootstrap override strategy | `:root` BS variable remapping + targeted class overrides |
| Breakpoints | Aligned to Bootstrap 5 sm (576 px) and lg (992 px) |
| Navbar | Bootstrap `navbar-dark sticky-top` added to `base.html` |
| Glassmorphism removal | All `backdrop-filter` and `rgba` fills replaced with solid opaque tokens |
| File naming | `custom.css` (per FR-012); `style.css` retired; `base.html` link updated |
| Body background | Solid `--color-bg` (#fff7f0) replaces gradient |
| Card treatment | Solid surface + 1 px border + soft shadow (FR-007) |
