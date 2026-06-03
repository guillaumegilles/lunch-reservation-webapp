# Implementation Plan: Options de repas de juin & notation des repas passés

**Branch**: `004-june-meals-rating` | **Date**: 2026-06-03 | **Spec**: `specs/004-june-meals-rating/spec.md`

**Input**: Feature specification from `/specs/004-june-meals-rating/spec.md`

## Summary

Populate June 2026 with varied daily menu entries, keep the meal selector on the calendar preselected to the menu quotidien by default, and add 5-star ratings for past confirmed reservations with admin-visible averages and per-user details.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: Django 5.2.13, vanilla JavaScript, Bootstrap 5.3.2 via CDN, Python stdlib (`datetime`, `calendar`, `json`)  
**Storage**: SQLite for local development (`db.sqlite3`), PostgreSQL in production via `DATABASE_URL`; one new Django migration for `MealRating`  
**Testing**: `python3 manage.py test`  
**Target Platform**: Django web app on Linux/Vercel  
**Project Type**: Web app  
**Performance Goals**: Keep the calendar interaction single-page and immediate; seeding must stay idempotent and complete in one management-command run  
**Constraints**: Preserve the existing French UI, keep reservation validation server-side, only allow ratings for past confirmed reservations, and avoid introducing a frontend framework or build step  
**Scale/Scope**: One month of seeded menus (June 2026, 22 working days), one rating per confirmed reservation, and monthly admin aggregates over the same dataset

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Sécurité par défaut**: pass — AJAX already uses CSRF, and new rating writes will follow the same server-side validation pattern.
- **Intégrité des données**: pass — menu seeding will be idempotent, reservation uniqueness stays intact, and ratings will be tied to confirmed lunches.
- **Interface minimale et explicite**: pass — implementation remains Django templates + vanilla JS, with one JSON endpoint for rating.
- **Conventions Django**: pass — ORM, built-in User, management commands, and app URLs remain the core integration points.
- **Configuration pilotée par l'environnement**: pass — no new environment-driven behavior is required beyond existing settings.

## Project Structure

### Documentation (this feature)

```text
specs/004-june-meals-rating/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ui-and-api.md
└── tasks.md
```

### Source Code (repository root)

```text
django_project/
└── urls.py

reservations/
├── models.py
├── views.py
├── urls.py
├── forms.py
├── templates/
│   ├── calendar.html
│   └── admin.html
├── static/
│   └── custom.css
├── management/
│   └── commands/
│       └── seed_june_menus.py
└── migrations/
    └── 00xx_mealrating.py
```

**Structure Decision**: Keep all feature work inside the existing Django app. Use a dedicated management command for June menu seeding, add one new persistent model for ratings, and extend the existing calendar/admin views and templates instead of introducing a new app.

## Phase 0 — Research

- Choose the menu-seeding approach and make it idempotent.
- Confirm the default-option selection strategy for the calendar picker.
- Confirm the rating data model and how it links to confirmed reservations.
- Decide how the admin monthly recap will derive average ratings.

## Phase 1 — Design & Contracts

- Define the `MealRating` data model and its relation to `Lunch`.
- Document the management-command contract for June menu seeding.
- Document the calendar and rating JSON contract.
- Update `.github/copilot-instructions.md` to point to this plan file.

## Phase 2 — Implementation Outline

1. Add persistent rating support with a migration and server-side validation for 1–5 stars.
2. Add or extend the June menu seeding command so every working day of June 2026 gets a varied menu entry without duplicates.
3. Update calendar data preparation so the default selection matches the menu quotidien when possible, otherwise falls back to the first active option.
4. Extend the calendar UI to show the default meal and a 5-star rating widget only for past confirmed reservations.
5. Étendre le récapitulatif mensuel admin pour afficher les moyennes par jour et les notes par utilisateur lorsque pertinent.
6. Validate the end-to-end flow with tests and a manual quickstart path.
