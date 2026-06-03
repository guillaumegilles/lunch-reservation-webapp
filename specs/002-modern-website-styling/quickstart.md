# Quickstart: Modern Website Styling

**Feature**: `002-modern-website-styling`
**Branch**: `002-modern-website-styling`

---

## What this feature delivers

A single `custom.css` file that replaces the existing `style.css` and:

- Implements a flat minimal design (no glassmorphism, no gradient backgrounds)
- Applies a sticky coloured navbar (berry fill, near-white text) to every page
- Fixes the only WCAG AA contrast failure (alert-danger light text on light background)
- Moves the inline `<style>.locked-day</style>` from `calendar.html` into `custom.css`
- Exposes all visual values as CSS custom properties (design tokens)

No back-end changes. No build step. No new Python dependencies.

---

## Files changed

| File | Change |
|------|--------|
| `reservations/static/custom.css` | **NEW** — full design system |
| `reservations/static/style.css` | **DELETE** (or empty) |
| `reservations/templates/base.html` | Update `<link>` to `custom.css`; add sticky navbar |
| `reservations/templates/calendar.html` | Remove inline `<style>.locked-day{…}</style>` block |

---

## Step-by-step implementation guide

### Step 1 — Create `custom.css`

Create `reservations/static/custom.css`. The file is organised into 10 sections (see `data-model.md` Entity 4):

1. Design tokens (`:root` block)
2. Global reset (`body`, `a`, `h1–h6`, font-family)
3. Navbar (`.navbar`, `.navbar-brand`, `.navbar .btn-outline-light`)
4. Cards & containers (`.card`, `.card-body`, `.table-responsive`)
5. Buttons (`.btn`, `.btn-primary`, `.btn-success`, `.btn-outline-*`)
6. Form controls (`.form-control`, `.form-select`, `label`)
7. Alerts (`.alert`, `.alert-success`, `.alert-info`, `.alert-danger`, `.alert-warning`)
8. Table (`.table`, `.table thead th`, `.table-striped`, `.table-bordered`)
9. Calendar (`.selectable-day`, `.locked-day`, `.calendar-day`, `.calendar-selection-card`, `#statusMsg`)
10. Responsive (`@media (max-width: 575.98px)`)

Refer to `data-model.md` for every token value and component specification.

### Step 2 — Update `base.html`

Two changes:

**2a — Replace stylesheet link** (line 13 of current `base.html`):
```html
<!-- Old -->
<link rel="stylesheet" href="{% static 'style.css' %}">

<!-- New -->
<link rel="stylesheet" href="{% static 'custom.css' %}">
```

**2b — Add sticky navbar** before the `.container` div:
```html
<nav class="navbar navbar-dark sticky-top">
  <div class="container-fluid px-3">
    <a class="navbar-brand" href="/">🍽 Lunch Réservation</a>
    {% if user.is_authenticated %}
    <a class="btn btn-outline-light btn-sm" href="{% url 'logout' %}">Se déconnecter</a>
    {% endif %}
  </div>
</nav>
```

Remove `class="bg-light"` from `<body>` (it is no longer needed; `--color-bg` handles the background).

### Step 3 — Update `calendar.html`

Remove the inline `<style>` block (currently lines 6–8):
```html
<!-- DELETE THIS BLOCK -->
<style>
.locked-day { opacity: 0.4; cursor: default; }
</style>
```

The `.locked-day` rule must be present in `custom.css` section 9 instead.

### Step 4 — Delete (or empty) `style.css`

The old file is superseded. Either delete it or leave it empty so `collectstatic` does not serve stale CSS:
```bash
# Option A: delete
rm reservations/static/style.css

# Option B: empty (safer if unsure about CDN caches)
echo "/* superseded by custom.css */" > reservations/static/style.css
```

### Step 5 — Collect static files

```bash
python manage.py collectstatic --noinput
```

---

## Visual QA checklist

Run through each page and verify:

- [ ] **Home / index**: Warm off-white background (no gradient); card flat with 1px border and soft shadow
- [ ] **Login**: Form fields with plum-tinted border and apricot focus ring; primary button in berry
- [ ] **Register**: Same as login; no clipped fields on 375 px mobile
- [ ] **Dashboard**: Cards visually consistent with login page
- [ ] **Calendar**: Day cells flat, hover shows apricot border; selected day in solid berry; locked days at 45% opacity; calendar selection card flat
- [ ] **Admin summary**: Table with plum thead, striped rows; same card container as other pages
- [ ] **All pages**: Sticky navbar visible in berry, near-white brand text; logout button top-right

---

## Accessibility QA checklist

- [ ] Tab through login form: focus ring visible on each input and button
- [ ] Check alert-danger message (trigger an invalid login): text is dark ink on light pink surface ≥ 4.5:1
- [ ] Check alert-success message: dark ink on light yellow surface ≥ 4.5:1
- [ ] Inspect button contrast (DevTools → Accessibility): all ≥ 4.5:1 for label text

---

## Responsive QA checklist

- [ ] 375 px wide: no horizontal scrollbar on any page; buttons ≥ 44 px tall; calendar day cells all visible
- [ ] 768 px wide: tablet layout; cards and forms readable
- [ ] 1280 px wide: desktop layout; no excessive whitespace

---

## Design token extension guide

To add a new colour to the design system:

1. Add the token to `:root` in `custom.css`
2. Add an entry to `contracts/design-tokens.md` under "Stable Token API"
3. Use the token in component rules — never hardcode the hex value

To adjust an existing token value (e.g., darken `--color-primary`):

1. Change the hex in `:root`
2. Re-run the contrast audit for all pairs that reference this token (see `research.md`)
3. Confirm no new WCAG failures are introduced

---

## Running the dev server

```bash
# Ensure migrations are up-to-date (no changes needed for this feature)
python manage.py migrate

# Seed default admin if starting fresh
python manage.py init_db

# Start dev server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — the new design system is active immediately (no build step).
