# Tasks: Modern Website Styling

**Input**: Design documents from `specs/002-modern-website-styling/`

**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/design-tokens.md ✅

**Organization**: Tasks are grouped by user story. All CSS sections write to the same single
file (`reservations/static/custom.css`) and must be applied sequentially within each phase.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup

**Purpose**: Baseline verification before any changes

- [ ] T001 Confirm branch is `002-modern-website-styling` and run `python3 manage.py test
  reservations --no-input` from project root to record a passing baseline (26 tests expected).
  Note the test count so post-implementation regression check has a reference.

**Checkpoint**: Baseline test count confirmed — styling work can begin.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The two structural prerequisites that every page depends on — the new CSS file
and the updated base template. These MUST complete before any per-component styling.

- [ ] T002 Create `reservations/static/custom.css` as a new file (do NOT modify `style.css` yet).
  Write the complete `:root` design token block using the exact values from `data-model.md`:
  - **Colour tokens** (§1.1): `--color-primary` `#B83B5E`, `--color-primary-dark` `#6A2C70`,
    `--color-accent` `#F08A5D`, `--color-accent-hover` `#d96e3f`, `--color-sun` `#F9ED69`,
    `--color-bg` `#fff7f0`, `--color-surface` `#fffaf1`, `--color-surface-success` `#fffbdd`,
    `--color-surface-error` `#fce8ef`, `--color-navbar-bg` `#B83B5E`,
    `--color-navbar-text` `#ffe8ee`, `--color-text` `#2f1638`,
    `--color-text-muted` `rgba(47,22,56,0.58)`, `--color-border` `rgba(106,44,112,0.15)`,
    `--color-focus-ring` `rgba(184,59,94,0.35)`
  - **Bootstrap variable remapping** (research.md §2): remap `--bs-primary`,
    `--bs-body-color`, `--bs-body-bg`, `--bs-link-color`, `--bs-border-radius`,
    `--bs-card-bg`, `--bs-card-border-color` to the matching `--color-*` tokens
  - **Typography tokens** (§1.2): `--font-heading`, `--font-body`, `--font-size-base` through
    `--font-size-2xl`, `--line-height-base`, `--line-height-heading`, `--letter-spacing-heading`,
    `--font-weight-normal/medium/bold`
  - **Spacing tokens** (§1.3): `--space-xs` through `--space-2xl`
  - **Shape & shadow tokens** (§1.4): `--radius-sm/md/lg/pill`, `--shadow-card`,
    `--shadow-navbar`, `--shadow-focus`, `--transition-fast: 0.15s ease`,
    `--shadow-btn-hover: 0 6px 16px rgba(106,44,112,0.18)` (button hover elevation)
  - **Interaction colour tokens** (§1.5 — tokenise all rgba values so no raw rgba appears
    outside `:root`): `--color-navbar-hover-overlay: rgba(255,255,255,0.12)`,
    `--color-table-border-thead: rgba(255,255,255,0.12)`,
    `--color-table-stripe: rgba(249,237,105,0.12)`,
    `--color-link-underline: rgba(184,59,94,0.45)` (link text-decoration tint)
  - After the `:root` block, add a `/* === 2. GLOBAL RESET === */` section: set
    `body { background-color: var(--color-bg); color: var(--color-text); font-family: var(--font-body); }`
  - **Validation rule**: no hex colour literals or raw `rgba()` values outside `:root`,
    no `backdrop-filter`, no gradients.

- [ ] T003 Update `reservations/templates/base.html`:
  1. Change `<link rel="stylesheet" href="{% static 'style.css' %}">` →
     `<link rel="stylesheet" href="{% static 'custom.css' %}">`
  2. Remove `class="bg-light"` from `<body>` (body background is now token-driven)
  3. Insert a sticky navbar **above** `<div class="container py-4 app-shell">`:
     ```html
     <nav class="navbar navbar-dark sticky-top">
       <div class="container-fluid">
         <a class="navbar-brand" href="/">🍽 Lunch Réservation</a>
         {% if user.is_authenticated %}
         <a class="btn btn-outline-light btn-sm" href="{% url 'logout' %}">Se déconnecter</a>
         {% endif %}
       </div>
     </nav>
     ```
  4. Keep the `.app-shell` container and messages block intact (no other changes).
  The file must produce valid HTML — check that `{% load static %}` remains in `<head>`.

**Checkpoint**: Visit any page — the CSS tokens load (berry/plum colours appear) and the
sticky navbar is visible at top. No visual regressions from layout break.

---

## Phase 3: User Story 1 — Visually Refreshed Experience (Priority: P1) 🎯 MVP

**Goal**: Apply the flat minimal design system to all six pages via consistent component
styles — navbar, cards, buttons, and typography — using the tokens from T002.

**Independent Test**: Navigate to all 6 pages (index, login, register, dashboard, calendar,
admin summary); verify same font families, colour palette, card treatment (opaque surface,
1px border, soft shadow), and button styles throughout. No glassmorphism remnants visible.

- [ ] T004 [US1] Add heading and link styles to `reservations/static/custom.css` (append to
  section `/* === 2. GLOBAL RESET === */` or add `/* === 2b. TYPOGRAPHY === */`):
  - `h1`–`h6`, `.card-title`: `font-family: var(--font-heading)`, `letter-spacing: var(--letter-spacing-heading)`, `line-height: var(--line-height-heading)`, `color: var(--color-primary-dark)`
  - `a`: `color: var(--color-primary)`, `text-decoration-color: var(--color-link-underline)`
  - `a:hover, a:active`: `color: var(--color-primary-dark)`
  - `a:focus-visible`: `outline: 2px solid var(--color-primary); outline-offset: 2px; border-radius: 2px`
  - `.text-muted`: `color: var(--color-text-muted) !important`

- [ ] T005 [US1] Add navbar component styles to `reservations/static/custom.css`
  (append `/* === 3. NAVBAR === */` section):
  - `.navbar { background-color: var(--color-navbar-bg); box-shadow: var(--shadow-navbar); padding: var(--space-sm) var(--space-md); }`
  - `.navbar .navbar-brand { font-family: var(--font-heading); font-size: var(--font-size-lg); color: var(--color-navbar-text); }`
  - `.navbar .navbar-brand:hover { color: var(--color-navbar-text); opacity: 0.9; }`
  - `.navbar .btn-outline-light { border-color: var(--color-navbar-text); color: var(--color-navbar-text); }`
  - `.navbar .btn-outline-light:hover { background-color: var(--color-navbar-hover-overlay); }`

- [ ] T006 [US1] Add card and container flat minimal styles to `reservations/static/custom.css`
  (append `/* === 4. CARDS & CONTAINERS === */` section). This is the core glassmorphism
  removal (research.md §5):
  - `.card, .table-responsive, .alert { background: var(--color-surface); backdrop-filter: none; border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-card); }`
  - `.card-body { border: none; border-radius: 0; }`
  - Remove the `.app-shell::before` grid overlay: `.app-shell::before { display: none; }`
  - `.calendar-selection-card { max-width: 32rem; margin: 0 auto; }`
  - Ensure NO `background: rgba(...)` or `backdrop-filter:` remains in any card/container rule.

- [ ] T007 [US1] Add button styles to `reservations/static/custom.css`
  (append `/* === 5. BUTTONS === */` section). Per data-model.md §2.3:
  - Base `.btn`: `border-radius: var(--radius-pill); font-weight: var(--font-weight-bold); transition: var(--transition-fast); border-width: 2px; padding: 0.7rem 1.2rem;`
  - `.btn:hover, .btn:focus-visible`: `transform: translateY(-1px); box-shadow: var(--shadow-btn-hover);`
  - `.btn-primary`: bg `var(--color-primary)`, border `var(--color-primary)`, color `var(--color-navbar-text)`
  - `.btn-primary:hover/:active`: bg and border `var(--color-primary-dark) !important`
  - `.btn-success`: bg `var(--color-accent)`, border `var(--color-accent)`, color `var(--color-text)`
  - `.btn-success:hover/:active`: bg and border `var(--color-accent-hover) !important`, color `var(--color-text) !important`
  - `.btn-outline-primary`: border and color `var(--color-primary-dark)`; hover: bg fill `var(--color-primary-dark)`, color `var(--color-navbar-text)`
  - `.btn-outline-secondary`: border `var(--color-border)` solid 2px, color `var(--color-primary)`; hover: bg `var(--color-surface-success)`
  - `.btn-outline-danger`: border `var(--color-primary)`, color `var(--color-primary)`; hover: bg `var(--color-surface-error)`

**Checkpoint**: US1 complete. All 6 pages show: Archivo Black headings in plum, DM Sans body,
flat opaque cards (no blur), pill-shaped buttons in berry/apricot, sticky berry navbar.
Run `python3 manage.py test reservations` — 26 tests must still pass.

---

## Phase 4: User Story 2 — Accessible Colour Scheme (Priority: P2)

**Goal**: Fix the WCAG AA contrast failure on alert components and ensure all interactive
elements have clear focus/hover states. All text-background pairs must score ≥ 4.5:1.

**Independent Test**: Open browser DevTools → Accessibility panel or use a contrast checker
(e.g., WebAIM) on these pairs: body text (`#2f1638` on `#fffaf1`) ✓, btn-primary label
(`#ffe8ee` on `#B83B5E`) ✓, alert-danger text (`#2f1638` on `#fce8ef`) must now ✓ (was ✗).

- [ ] T008 [US2] Add form control styles to `reservations/static/custom.css`
  (append `/* === 6. FORM CONTROLS === */` section). Per data-model.md §2.4:
  - `.form-control, .form-select { border: 1.5px solid var(--color-border); border-radius: var(--radius-sm); background-color: #ffffff; padding: 0.6rem 0.9rem; transition: var(--transition-fast); }`
  - `.form-control:focus, .form-select:focus { border-color: var(--color-accent); box-shadow: var(--shadow-focus); outline: none; }`

- [ ] T009 [US2] Add alert styles with WCAG AA fix to `reservations/static/custom.css`
  (append `/* === 7. ALERTS === */` section). This resolves the 2.13:1 contrast failure
  identified in research.md §1:
  - `.alert { color: var(--color-text); border-radius: var(--radius-md); box-shadow: var(--shadow-card); border-left-width: 3px; border-left-style: solid; }`
  - `.alert-success, .alert-info { background: var(--color-surface-success); border-left-color: var(--color-primary-dark); }`
  - `.alert-danger, .alert-warning, .alert-error { background: var(--color-surface-error); color: var(--color-text); border-left-color: var(--color-primary); }`
  - **Critical**: NO `linear-gradient` or `rgba` semi-transparent background on alerts.
    The old gradient `linear-gradient(135deg, rgba(240,138,93,0.88), rgba(184,59,94,0.72))`
    with light text `#fffaf1` (2.13:1 contrast) is replaced by solid `#fce8ef` + ink text (13.6:1).

- [ ] T010 [US2] Add table styles to `reservations/static/custom.css`
  (append `/* === 8. TABLE === */` section). Per data-model.md §2.6:
  - `.table-responsive { border-radius: var(--radius-md); overflow: hidden; }`
  - `.table { margin-bottom: 0; }`
  - `.table thead th { background-color: var(--color-primary-dark) !important; color: var(--color-navbar-text); border-color: var(--color-table-border-thead); text-transform: uppercase; font-size: 0.82rem; letter-spacing: 0.05em; }`
  - `.table-striped > tbody > tr:nth-of-type(odd) > * { background-color: var(--color-table-stripe); }`
  - `.table-bordered > :not(caption) > * > * { border-color: var(--color-border); }`
  - `#statusMsg { color: var(--color-primary-dark); font-weight: var(--font-weight-bold); }`

**Checkpoint**: US2 complete. Verify with DevTools: alert-danger box has light berry-pink
solid background with dark text (contrast ≥ 4.5:1). Form fields show focus ring on Tab.

---

## Phase 5: User Story 3 — Responsive Layout (Priority: P3)

**Goal**: Calendar cells adapt to mobile, buttons meet 44 px tap target, no horizontal
overflow at 375 px. Move `.locked-day` from inline `<style>` in `calendar.html` to `custom.css`.

**Independent Test**: Open DevTools → Toggle device toolbar → iPhone SE (375×667).
Verify: no horizontal scrollbar, all day cells visible, all buttons ≥ 44 px tall,
"Annuler" / option buttons tappable without zoom. Check at 768 px (tablet) too.

- [ ] T011 [US3] Add calendar day cell styles to `reservations/static/custom.css`
  (append `/* === 9. CALENDAR === */` section). Per data-model.md §2.7:
  - `.calendar-day { cursor: pointer; }`
  - `.selectable-day { border: 1.5px solid var(--color-border); border-radius: var(--radius-lg); background: var(--color-surface); box-shadow: var(--shadow-card); transition: var(--transition-fast); }`
  - `.selectable-day:hover { border-color: var(--color-accent); transform: translateY(-1px); }`
  - `.calendar-day .bg-primary { border-radius: var(--radius-lg); background: var(--color-primary) !important; color: var(--color-navbar-text); box-shadow: var(--shadow-card); }`
  - `.calendar-day .bg-primary .small, .calendar-day .bg-primary .lunch-label { color: var(--color-navbar-text) !important; }`
  - `.locked-day { opacity: 0.45; cursor: default; pointer-events: none; }`

- [ ] T012 [US3] Remove the inline `<style>` block from `reservations/templates/calendar.html`.
  Delete lines 6–8 (the `<style>.locked-day { opacity: 0.4; cursor: default; }</style>` block).
  The `.locked-day` rule is now in `custom.css` (T011) with `opacity: 0.45` and
  `pointer-events: none` added for full accessibility.

- [ ] T013 [US3] Add responsive breakpoint media queries to `reservations/static/custom.css`
  (append `/* === 10. RESPONSIVE === */` section). Per data-model.md §3 and SC-003:
  ```css
  @media (max-width: 575.98px) {
    /* SC-003: 44px minimum tap target */
    .btn { min-height: 44px; padding: 0.68rem 1rem; }
    /* Reduce radius for tighter mobile feel */
    .card, .alert, .table-responsive,
    .selectable-day, .calendar-day .bg-primary { border-radius: var(--radius-sm) !important; }
    /* Scale down headings one step */
    h1 { font-size: var(--font-size-xl); }
    h2 { font-size: var(--font-size-lg); }
    /* App shell padding */
    .app-shell { padding-top: var(--space-md) !important; padding-bottom: var(--space-lg) !important; }
  }

  /* FR-008 tablet tier — Bootstrap grid (col-sm-*, col-md-*) handles column layout automatically */
  @media (min-width: 576px) and (max-width: 991.98px) {
    /* Buttons: default padding retained (44px min-height required on mobile only per SC-003) */
    /* Cards and alerts: --radius-md (default) retained — no intermediate adjustment needed */
    .app-shell { padding-top: var(--space-lg) !important; }
  }
  ```

**Checkpoint**: US3 complete. At 375 px: no overflow, buttons ≥ 44 px, calendar cells
display correctly, locked days greyed out with no click interaction.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Retire the old stylesheet, final regression check, and documentation sync.

- [ ] T014 Delete `reservations/static/style.css`. This file is fully superseded by
  `custom.css`. Confirm `base.html` still references `custom.css` (T003 change) and
  that no other template has a hard-coded link to `style.css`.

- [ ] T015 [P] Run `python3 manage.py test reservations --no-input` from project root.
  All 26 tests must pass. If any test fails, identify whether it is a pre-existing failure
  or a regression introduced by template changes (T003, T012) and fix accordingly.

- [ ] T016 [P] Visual QA — start the dev server (`python3 manage.py runserver`) and open
  each of the 6 pages in a browser. For each page verify:
  - Berry/plum sticky navbar visible at top with logout button when authenticated
  - Flat opaque cards (no blur, no gradient background visible through cards)
  - Archivo Black headings in plum, DM Sans body text
  - No unstyled elements (plain black/white Bootstrap defaults)
  - Alert messages (flash a success login and a failed login) use correct solid-surface colours
  - At 375 px viewport (DevTools): no horizontal scroll, buttons tappable
  - Admin summary table: plum header, sun-tinted striped rows
  - **SC-001 token audit**: open `custom.css` in browser DevTools → Sources; confirm
    no hex colour literal (`#xxxxxx`) or raw `rgba()` value appears outside the `:root { }`
    block. Every colour reference outside `:root` must be `var(--color-*)` or `var(--shadow-*)`.
  - **SC-005 primary action visibility**: on each page, the primary CTA button is visible
    without scrolling at desktop (1280×720), tablet (768×1024), and mobile (375×667).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1. T002 must complete before T003. Blocks all styling phases.
- **Phase 3 (US1)**: Depends on Phase 2 (T002 tokens must exist). T004 → T005 → T006 → T007 (sequential — same file).
- **Phase 4 (US2)**: Depends on Phase 2. T008 → T009 → T010 (sequential — same file). Can start after Phase 2 in parallel with Phase 3.
- **Phase 5 (US3)**: Depends on Phase 3 (`.selectable-day` base rules from T006). T011 → T012 → T013 (sequential).
- **Phase 6 (Polish)**: Depends on all previous phases. T014 → then T015 and T016 in parallel.

### User Story Dependencies

| Story | Depends On | Can Parallelise With |
|-------|-----------|---------------------|
| US1 — Visual refresh (Phase 3) | Phase 2 | US2 (Phase 4) after Phase 2 |
| US2 — Accessible colours (Phase 4) | Phase 2 | US1 (Phase 3) |
| US3 — Responsive layout (Phase 5) | Phase 3 (T006 card base) | — |

### Within Each Phase

- All tasks in Phase 3 write to `custom.css` → apply **sequentially** (T004 → T005 → T006 → T007).
- All tasks in Phase 4 write to `custom.css` → apply **sequentially** (T008 → T009 → T010).
- T011 (write), T012 (template delete), T013 (write) → apply **sequentially** to avoid section conflicts.
- T015 and T016 are `[P]` — run the server in parallel with the test suite.

---

## Parallel Examples

```bash
# After Phase 2 completes, US1 and US2 can begin in parallel on different sections:
# (US1 works on sections 2-5 of custom.css; US2 works on sections 6-8)

# US1 sequence:
Task T004  # [US1] Typography + heading styles → custom.css
Task T005  # [US1] Navbar styles → custom.css
Task T006  # [US1] Card/container flat minimal → custom.css
Task T007  # [US1] Button variants → custom.css

# US2 sequence (can start in parallel with US1 if editing different section blocks):
Task T008  # [US2] Form controls → custom.css
Task T009  # [US2] Alert WCAG AA fix → custom.css
Task T010  # [US2] Table styles → custom.css

# After Phase 3 (US1) completes:
Task T011  # [US3] Calendar day cells + locked-day → custom.css
Task T012  # [US3] Remove inline <style> from calendar.html
Task T013  # [US3] Responsive breakpoints → custom.css
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 (baseline test)
2. Complete Phase 2 (T002 tokens + T003 base.html)
3. Complete Phase 3 (T004–T007 — visual refresh)
4. **STOP and VALIDATE**: Visit all 6 pages — coherent warm palette, flat minimal cards, sticky navbar ✓
5. Delete `style.css` (T014) and run tests (T015)

### Incremental Delivery

1. Phases 1–2 → Design token infrastructure ready
2. Phase 3 (US1) → Visual consistency across all pages ✅
3. Phase 4 (US2) → WCAG AA alert fix + form focus states ✅
4. Phase 5 (US3) → Mobile responsive layout ✅
5. Phase 6 → Style.css retired, full test green, visual QA ✅

---

## Notes

- All custom styles live in a single `reservations/static/custom.css` — no other CSS files created.
- Tasks T004–T013 all append sections to `custom.css`; apply them in order within each phase to avoid conflicts.
- The `style.css` file is NOT deleted until T014 (Phase 6) — keep it intact during development as a reference.
- `base.html` is the only template that requires structural markup changes (navbar + link update).
- `calendar.html` only requires the inline `<style>` block removal (T012) — no other template needs markup changes.
- After T003, the navbar provides a global logout button; the per-page logout buttons in `dashboard.html` and `calendar.html` are retained as secondary actions (FR-009 — no functionality removed).
- Validation rule throughout: no hex colour literals or raw `rgba()` values outside `:root`, no `backdrop-filter`, no `linear-gradient` on cards/alerts.
