# Research: MVP Lunch Reservation Website

**Phase 0 output** | **Date**: 2026-05-17 | **Plan**: [plan.md](plan.md)

## Summary

All technical questions are resolved by inspecting the existing codebase. No external
research was required. This document records the decisions already made, their rationale,
and any gaps identified.

---

## Decision 1: Django Single-App Architecture

**Decision**: One Django project package (`django_project/`) and one app (`reservations/`)
containing all models, views, forms, templates, static files, migrations, and tests.

**Rationale**: The application has a narrow, well-defined domain (lunch reservations for a
single office). A single-app structure keeps the codebase navigable, avoids unnecessary
cross-app imports, and aligns with the "simplicity over custom solutions" principle.

**Alternatives considered**:
- Multiple Django apps (e.g., `auth_app`, `calendar_app`, `admin_app`) — rejected because
  the features are tightly coupled and the scale does not justify the overhead.

---

## Decision 2: Database-Driven Meal Options (MealOption model)

**Decision**: Meal options are stored as `MealOption` records (`name`, `is_active`,
`order`) rather than a hardcoded list constant.

**Rationale**: Allows CSE staff to manage options via the Django admin without code
changes or redeployment. Active options are fetched with
`MealOption.objects.filter(is_active=True)` and passed to the calendar template.

**Gap identified**: The `save_lunch` view currently accepts any string for `lunch_choice`
without validating it against active `MealOption` records. This violates Principle II
(data integrity). A server-side validation step must be added.

**Note**: The copilot-instructions.md file refers to a `LUNCH_OPTIONS` list constant.
This is outdated — the implementation uses the `MealOption` model. The agent context
file should be updated to reflect this.

---

## Decision 3: Default Weekday Menus (WEEKDAY_MENUS constant)

**Decision**: `WEEKDAY_MENUS` is a dict constant in `views.py` mapping weekday integers
to default menu strings. Used as fallback when no `DailyMenu` record exists for a day.

**Rationale**: Provides a sensible default menu display without requiring staff to enter
menus every week. CSE staff override individual days using the `WeeklyMenuForm`.

**Alternatives considered**: Database-only (all menus must be set by staff) — rejected
as it would leave the calendar blank for weeks where no menu has been configured.

---

## Decision 4: Vercel Serverless Deployment

**Decision**: Vercel via `vercel.json` with `python3.12` runtime targeting
`django_project/wsgi.py`. Build command runs `migrate` and `collectstatic` automatically.

**Rationale**: Vercel provides zero-configuration HTTPS, global CDN for static files, and
a Python serverless runtime. The `vercel.json` is already committed and correct.

**Key configuration**:
```json
{
  "buildCommand": "pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput",
  "functions": { "django_project/wsgi.py": { "runtime": "python3.12" } }
}
```

**Constraint**: Vercel serverless functions are stateless — SQLite cannot be used in
production (file system is ephemeral). `DATABASE_URL` must be set to a persistent
PostgreSQL instance.

---

## Decision 5: Session-Based Authentication with Django Built-ins

**Decision**: Standard Django session authentication using `django.contrib.auth`. Login
via username (matricule) + password. `@login_required` decorator on all protected views.
Staff access via `is_staff=True` flag on the built-in `User` model.

**Rationale**: The built-in auth system is battle-tested, handles password hashing, CSRF,
and session management securely. No external auth dependency needed for this scale.

**Alternatives considered**: JWT tokens — rejected (overkill for a server-rendered app
with no separate API clients).

---

## Decision 6: Vanilla JS AJAX for Save-Lunch

**Decision**: `calendar.html` uses a small inline `<script>` block with `fetch()` to
POST to `/save-lunch/`. The CSRF token is read from the `csrftoken` cookie and sent
via `X-CSRFToken` header.

**Rationale**: Eliminates full-page reload on option selection while keeping zero build
tooling. Matches Principle III (minimal frontend).

---

## Gaps to Address

| ID | Gap | Principle | Severity |
|----|-----|-----------|----------|
| G1 | `save_lunch` does not validate `lunch_choice` against `MealOption` records | II | High |
| G2 | `requirements.txt` uses `>=` instead of pinned versions | Code Quality | Low |
| G3 | CSE badge number not captured in `RegisterForm` or `User` model | FR-001 | Medium |
| G4 | `copilot-instructions.md` references outdated `LUNCH_OPTIONS` constant | Docs | Low |
