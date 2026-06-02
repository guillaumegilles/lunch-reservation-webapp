# Implementation Plan: MVP Lunch Reservation Website

**Branch**: `main` | **Date**: 2026-05-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-lunch-reservation-mvp/spec.md`

## Summary

Django 5.2 / Python 3.12 server-rendered web application for office lunch reservations.
Employees register with a company matricule, browse a monthly working-day calendar, and
pick a daily meal option. CSE staff view a monthly summary and manage weekly menus. A
suggestion form sends email notifications. The app is production-ready on Vercel via a
single `vercel.json` build configuration. The core application is largely implemented;
this plan documents the architecture, identifies the remaining gaps, and charts the path
to a fully production-ready deployment.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django ~5.2, dj-database-url ≥2.1.0, psycopg2-binary ≥2.9.9

**Storage**: SQLite (development) / PostgreSQL via `DATABASE_URL` (production)

**Testing**: Django `TestCase` (built-in test runner via `python manage.py test`)

**Target Platform**: Vercel serverless (python3.12 runtime), office browser access

**Project Type**: web-service (server-rendered Django application)

**Performance Goals**: Reservation saved in under 30 seconds end-to-end (SC-001); small
internal office scale (tens of concurrent users at peak lunch-booking time)

**Constraints**: No build toolchain; single CSS file; vanilla JS only; all secrets via
env vars; no raw SQL; no custom User model

**Scale/Scope**: Single Django app (`reservations/`) + project package (`django_project/`);
~50 internal users; 5 working days × ~20 weekday-months per year reservation volume

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Sécurité par défaut | ✅ Pass | `@login_required` on all protected views; `is_staff` guard in `admin_summary`; CSRF enforced; secrets via env vars; `DEBUG` env-driven |
| II. Intégrité des données | ⚠️ Gap | `save_lunch` does not validate `lunch_choice` against active `MealOption` records — any string is accepted. Must add server-side validation. (addressed by T010) |
| III. Interface minimale | ✅ Pass | DTL templates; vanilla JS AJAX with `X-CSRFToken`; single `style.css`; all UI in French |
| IV. Conventions Django | ✅ Pass | Built-in `User`; `is_staff` only for access control; ORM-only; URLs in `reservations/urls.py`; `init_db` management command |
| V. Config pilotée | ✅ Pass | All secrets via `os.environ.get()`; SQLite/PostgreSQL switch via `DATABASE_URL`; Vercel `python3.12` runtime in `vercel.json` |
| Déploiement | ✅ Pass | `collectstatic` + `migrate` in Vercel build command; WSGI at `django_project/wsgi.py`; email backend env-driven |
| Qualité du code | ⚠️ Gap | `requirements.txt` uses `>=` (loose constraints); CSE badge number field absent from `RegisterForm` / `User` model despite being specified in `app-features.md` |

**Gate decision**: Proceed. Two gaps logged — both are implementation-level fixes, not
architectural blockers. Addressed in Phases 2–3 of tasks.

## Project Structure

### Documentation (this feature)

```text
specs/001-lunch-reservation-mvp/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── http-endpoints.md  # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks — not created by /speckit.plan)
```

### Source Code (repository root)

```text
django_project/          # Project package
├── settings.py          # Env-driven configuration
├── urls.py              # Delegates to reservations/urls.py
└── wsgi.py              # Vercel entrypoint

reservations/            # Single Django app
├── models.py            # MealOption, DailyMenu, Lunch, Suggestion
├── views.py             # All views + WEEKDAY_MENUS default constant
├── forms.py             # LoginForm, RegisterForm, WeeklyMenuForm, SuggestionForm
├── urls.py              # All URL patterns
├── admin.py             # Django admin registrations
├── templates/           # Server-rendered HTML (DTL)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── calendar.html
│   └── admin.html
├── static/
│   └── style.css        # Single stylesheet
├── management/commands/
│   └── init_db.py       # Seeds default admin user
├── migrations/          # ORM migrations (0001–0004)
└── tests/
    ├── test_views.py
    └── test_management_commands.py

manage.py
requirements.txt
vercel.json
```

**Structure Decision**: Single Django project with one app (`reservations/`). All business
logic, models, views, templates, and tests live inside `reservations/`. The project
package (`django_project/`) contains only settings, root URL config, and WSGI entry
point. This is the correct structure for the scale and simplicity constraints of this
project and aligns with Principle IV.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| `>=` version constraints in `requirements.txt` | Existing state; not a new addition | Must be pinned to satisfy Code Quality Gate — addressed in tasks |
