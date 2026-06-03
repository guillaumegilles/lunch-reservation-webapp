# Tasks: Options de repas de juin & notation des repas passés

**Input**: Design documents from `specs/004-june-meals-rating/`  
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/ ✅ | quickstart.md ✅

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other tasks that touch different files
- **[Story]**: `US1`, `US2`, etc. Setup, Foundational, and Polish phases carry no story label

---

## Phase 1: Setup

**Purpose**: Capture a baseline before changing the calendar, menus, or rating flow.

- [X] T001 Run `python3 manage.py test` from the repo root and record the current passing baseline before editing `reservations/models.py`, `reservations/views.py`, or any template/command file.

**Checkpoint**: Baseline confirmed and ready for feature work.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add the persistent model that the rating feature depends on.

- [X] T002 Add the `MealRating` model to `reservations/models.py` with a one-to-one link to `Lunch`, a 1–5 integer rating, and created/updated timestamps.

- [X] T003 Create and verify the migration for `MealRating` in `reservations/migrations/00xx_mealrating.py`, then apply it locally with `python3 manage.py migrate`.

**Checkpoint**: Rating persistence exists at the data layer.

---

## Phase 3: User Story 1 — Consulter et réserver un repas avec une option pré-sélectionnée (Priority: P1) 🎯 MVP

**Goal**: The calendar preselects the menu quotidien when it matches an active option de repas, and falls back safely when no match exists.

**Independent Test**: Open a day in the calendar with a matching menu quotidien and confirm the matching option de repas is already selected; open a day without a match and confirm the first active option de repas is selected.

### Implementation for User Story 1

- [X] T004 [P] [US1] Add tests in `reservations/tests/test_views.py` covering matching menu quotidien preselection and the first-active-option fallback when no menu match exists.

- [X] T005 [US1] Update `reservations/views.py` so `calendar_view` computes the default option de repas from the menu quotidien by exact name match against active `MealOption` records, and falls back to the first active option when needed.

- [X] T006 [US1] Update `reservations/templates/calendar.html` and `reservations/static/custom.css` so the menu quotidien opens with the computed default option selected and the longer June menu labels remain readable in the grid.

**Checkpoint**: Calendar reservation flow now defaults to the correct meal choice.

---

## Phase 4: User Story 2 — Charger les données de menus de juin (Priority: P1)

**Goal**: June 2026 is populated with varied menu quotidien entries without duplicate rows.

**Independent Test**: Run the seeding command twice and confirm the first run creates 22 working-day menus and the second run does not duplicate them; with `--force`, existing rows are replaced and Fridays keep a festive menu.

### Implementation for User Story 2

- [X] T007 [P] [US2] Add tests in `reservations/tests/test_management_commands.py` for the June seeding command covering 22 working-day rows, at least 6 distinct menu labels, idempotent reruns, Friday festive menus, and `--force` replacement behavior.

- [X] T008 [US2] Implement `reservations/management/commands/seed_june_menus.py` to populate June 2026 working days with varied French menu labels, ensure Fridays receive a festive or more elaborate menu, and support `--force` for overwriting existing rows when requested.

**Checkpoint**: June menu population is repeatable and safe.

---

## Phase 5: User Story 3 — Noter un repas passé (Priority: P2)

**Goal**: Users can rate only past confirmed reservations with a 5-star widget, and ratings persist and can be updated.

**Independent Test**: Create a past confirmed reservation, rate it from the calendar, reload, and confirm the rating persists; verify the widget is hidden for future dates and dates without a reservation.

### Implementation for User Story 3

- [X] T009 [P] [US3] Add tests in `reservations/tests/test_views.py` covering rating visibility for past confirmed lunches only, rejection without a reservation, rejection for today/future dates, and rating overwrite behavior.

- [X] T010 [US3] Add the `/save-meal-rating/` JSON flow in `reservations/views.py` and `reservations/urls.py`, backed by `MealRating`, with 1–5 validation and overwrite behavior for the same lunch.

- [X] T011 [US3] Update `reservations/templates/calendar.html` and `reservations/static/custom.css` to render a 5-star rating widget only for eligible past reservations and preserve the selected star state on reload.

**Checkpoint**: Past-meal ratings are writable, persistent, and correctly gated.

---

## Phase 6: User Story 4 — Consulter les statistiques de notation (admin) (Priority: P3)

**Goal**: Administrators can see per-day average ratings and individual user ratings in the monthly recap.

**Independent Test**: Seed a few ratings, open the admin monthly recap, and verify each rated day shows an average while unrated days show `Non noté`.

### Implementation for User Story 4

- [X] T012 [P] [US4] Add tests in `reservations/tests/test_views.py` for daily average ratings, per-user rating visibility, and the `Non noté` state when no ratings exist.

- [X] T013 [US4] Extend `reservations/views.py` to compute per-day averages and per-user rating summaries for the admin monthly recap using `Lunch` and `MealRating`.

- [X] T014 [US4] Update `reservations/templates/admin.html` to show the average rating per day and each user's rating in the monthly summary.

**Checkpoint**: Admin recap includes usable rating analytics.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final regression check and cleanup across all feature surfaces.

- [X] T015 [P] Run `python3 manage.py test` from the repo root and fix any regressions across `reservations/models.py`, `reservations/views.py`, `reservations/templates/`, `reservations/management/commands/`, or `reservations/static/custom.css`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup and blocks rating-related work.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 (Phase 4)**: Depends on Foundational and can run in parallel with US1.
- **User Story 3 (Phase 5)**: Depends on Foundational and can start after US1’s calendar wiring is in place.
- **User Story 4 (Phase 6)**: Depends on User Story 3.
- **Polish (Final Phase)**: Depends on all desired user stories.

### User Story Dependencies

| Story | Depends On | Can Parallelise With |
|-------|-----------|---------------------|
| US1 (P1) | Phase 2 | US2 |
| US2 (P1) | Phase 2 | US1 |
| US3 (P2) | Phase 2, US1 | — |
| US4 (P3) | US3 | — |

### Within Each User Story

- Tests (if included) should be written before implementation tasks in that story.
- Model changes before endpoint/view wiring.
- View wiring before template and styling updates.
- Keep tasks that touch the same file sequential.

### Parallel Opportunities

- `T004` and `T007` can run in parallel because they touch different test files.
- `T005` and `T008` can run in parallel because they touch different implementation surfaces.
- `T009` can run while `T010` is being planned, but both should complete before `T011`.

---

## Parallel Example: User Story 1

```bash
Task T004  # [US1] tests in reservations/tests/test_views.py
Task T005  # [US1] calendar_view logic in reservations/views.py
Task T006  # [US1] calendar template + CSS
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate the default-selection calendar flow

### Incremental Delivery

1. Add persistent rating storage
2. Deliver the default meal selection behavior
3. Deliver June menu seeding
4. Add past-meal ratings
5. Add admin rating analytics
6. Finish with a full regression pass

### Parallel Team Strategy

1. One contributor handles menu default-selection work (US1)
2. Another contributor handles June seeding (US2)
3. After the rating model exists, one contributor handles rating UI/API while another prepares admin analytics
