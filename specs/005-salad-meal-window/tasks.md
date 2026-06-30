# Tasks: Option salade avec fenêtre de 48 heures

**Input**: Design documents from `specs/005-salad-meal-window/`  
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/ui-and-api.md ✅ | quickstart.md ✅

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other tasks that touch different files
- **[Story]**: `US1`, `US2`, etc. Setup, Foundational, and Polish phases carry no story label

---

## Phase 1: Setup

**Purpose**: Capture the current reservation baseline before touching the salad availability flow.

- [X] T001 Run `python3 manage.py test` from the repo root and record the baseline before editing `reservations/views.py`, `reservations/admin.py`, `reservations/management/commands/init_db.py`, `reservations/templates/calendar.html`, and `reservations/tests/test_views.py`.

**Checkpoint**: The current Django lunch reservation flow is known-good before feature work starts.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Put the shared catalogue and availability primitives in place before any user-story behavior is implemented.

- [X] T002 [P] Update `reservations/management/commands/init_db.py` so the seeded salad catalogue entries (`🥗 Salade César`, `🥙 Salade Niçoise`, `🥬 Salade composée`) stay active with `advance_days = 2` while the existing standard meals keep their configured delays.

- [X] T003 [P] Update `reservations/admin.py` `MealOptionAdmin` to expose `advance_days` in the existing meal catalogue list so staff can manage salad lead times without a separate admin workflow.

- [X] T004 Create shared availability helpers in `reservations/views.py` that evaluate each `MealOption.advance_days` from `localdate()`, produce the French 48-hour guidance/error copy, and can be reused by both `calendar_view` and the JSON `save_lunch` POST on `/save-lunch/`.

**Checkpoint**: The catalogue and shared availability rule are ready for story-specific calendar behavior.

---

## Phase 3: User Story 1 - Réserver une salade pour une date éligible (Priority: P1) 🎯 MVP

**Goal**: Let an employee pick and save a salad for a date that meets the inclusive 2-day threshold.

**Independent Test**: Open a workday at `J+2` or later, choose a salad from the calendar card, submit the JSON POST to `/save-lunch/`, then reload the same day and confirm the saved salad remains visible.

### Tests for User Story 1

- [X] T005 [US1] Add regression coverage in `reservations/tests/test_views.py` for an eligible salad saved exactly at the inclusive `J+2` threshold, the Friday→Monday case, and the calendar redisplay of the saved salad on a later page load.

### Implementation for User Story 1

- [X] T006 [US1] Update `reservations/views.py` so `calendar_view` and `save_lunch` use the shared per-option availability helper to allow eligible salad selections, preserve the existing JSON contract on `/save-lunch/`, and keep the saved `Lunch.lunch_choice` visible after persistence.

- [X] T007 [US1] Update `reservations/templates/calendar.html` so the day selector populates from the eligible per-day options, keeps French labels/messages, and shows the saved salad in both the calendar grid and selected-day panel after a successful reservation.

**Checkpoint**: A salad can be reserved and reloaded successfully for any date that meets the 48-hour rule.

---

## Phase 4: User Story 2 - Comprendre quand la salade n'est plus disponible (Priority: P1)

**Goal**: Make it obvious in French when salad is no longer available while still allowing any other meal whose own delay is satisfied.

**Independent Test**: Open a date that is too close for salad, verify that no new salad choice is shown, confirm that a French explanation is displayed, and verify that `/save-lunch/` still accepts another allowed meal for that same day.

### Tests for User Story 2

- [X] T008 [US2] Add regression coverage in `reservations/tests/test_views.py` for a near-date selection where salad is filtered out, a French 48-hour notice is exposed in the calendar state, `/save-lunch/` rejects an ineligible salad POST, and another allowed meal can still be saved.

### Implementation for User Story 2

- [X] T009 [US2] Update `reservations/views.py` so each calendar day exposes `available_options` and `unavailable_notice`, rejects too-soon salad submissions with the French contract error, and keeps non-salad meals available whenever their own `advance_days` still allow them.

- [X] T010 [US2] Update `reservations/templates/calendar.html` so the selection card hides too-soon salad choices for new reservations, renders the French 48-hour explanation, and keeps JSON submission pointed to `/save-lunch/` for the remaining allowed meals.

**Checkpoint**: Too-soon salad bookings are clearly explained and cannot be submitted, without blocking other eligible meals.

---

## Phase 5: User Story 3 - Conserver la lisibilité d'une réservation salade déjà prise (Priority: P2)

**Goal**: Keep an already booked salad visible below the cutoff, while still allowing cancellation or replacement and preventing re-selection after removal.

**Independent Test**: Save a salad for an eligible date, move the test clock below the threshold, confirm the reservation still shows as salad, cancel or replace it successfully, and verify that salad cannot be chosen again for that same date.

### Tests for User Story 3

- [X] T011 [US3] Add regression coverage in `reservations/tests/test_views.py` for a previously saved salad remaining visible below the cutoff, successful cancellation or replacement with another allowed meal, and refusal to reselect salad after it was removed under the threshold.

### Implementation for User Story 3

- [X] T012 [US3] Update `reservations/views.py` so the calendar state separates the stored `existing_lunch` display from new `available_options`, keeps a below-threshold salad visible after it was booked in time, and prevents that salad from reappearing as a selectable option once it has been cancelled.

- [X] T013 [US3] Update `reservations/templates/calendar.html` so an existing salad reservation stays visible even when it is absent from the selector, while the French cancel/replacement flow remains usable for below-threshold dates.

**Checkpoint**: Existing salad reservations stay trustworthy below the cutoff, and the post-cancellation guard is enforced.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the full salad workflow and catch any remaining inconsistencies across the shared files.

- [X] T014 [P] Run `python3 manage.py check` and `python3 manage.py test reservations.tests.test_views` from the repo root to validate the final changes in `reservations/views.py`, `reservations/admin.py`, `reservations/management/commands/init_db.py`, `reservations/templates/calendar.html`, and `reservations/tests/test_views.py`.

- [X] T015 [P] Validate the manual scenarios in `specs/005-salad-meal-window/quickstart.md` against `reservations/views.py` and `reservations/templates/calendar.html`, then tighten any remaining French UI/error copy mismatches in those same files.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 (Phase 4)**: Depends on Foundational.
- **User Story 3 (Phase 5)**: Depends on Foundational and builds on the persisted salad flow from User Story 1.
- **Polish (Phase 6)**: Depends on the user stories you plan to ship.

### User Story Dependencies

| Story | Depends On | Can Parallelise With |
|-------|-----------|---------------------|
| US1 (P1) | Phase 2 | US2 (with coordination, because both touch `reservations/views.py` and `reservations/templates/calendar.html`) |
| US2 (P1) | Phase 2 | US1 (with coordination, because both touch `reservations/views.py` and `reservations/templates/calendar.html`) |
| US3 (P2) | Phase 2, US1 | — |

### Within Each User Story

- Add or update the `reservations/tests/test_views.py` coverage before changing the corresponding implementation files.
- Keep shared availability logic in `reservations/views.py` ahead of the template wiring in `reservations/templates/calendar.html`.
- Preserve the existing JSON POST contract on `/save-lunch/` while changing UI state and validation behavior.

### Parallel Opportunities

- `T002` and `T003` can run in parallel because they touch `reservations/management/commands/init_db.py` and `reservations/admin.py` separately.
- After `T004`, one contributor can take `US1` while another takes `US2`, but they must coordinate changes in `reservations/views.py` and `reservations/templates/calendar.html`.
- `T014` and `T015` can run in parallel once the implementation phases are complete.

---

## Parallel Example: User Story 1

```bash
Task: "Update reservations/views.py so calendar_view and save_lunch allow eligible salad selections"
Task: "Update reservations/templates/calendar.html so the selector and saved-lunch display follow the per-day eligible options contract"
```

## Parallel Example: User Story 2

```bash
Task: "Update reservations/views.py so near-date days expose unavailable_notice and reject too-soon salad POSTs"
Task: "Update reservations/templates/calendar.html so too-soon salad choices are hidden and the French 48-hour explanation is rendered"
```

## Parallel Example: User Story 3

```bash
Task: "Update reservations/views.py so existing_lunch remains visible below the cutoff and salad cannot be reselected after cancellation"
Task: "Update reservations/templates/calendar.html so below-threshold salad reservations stay visible while cancel/replacement remains usable"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate an eligible salad booking end-to-end before adding the guardrail stories

### Incremental Delivery

1. Seed/admin-enable the salad catalogue and shared availability logic
2. Deliver eligible salad booking and persistence (US1)
3. Add the French near-date explanation and blocked-submit guardrails (US2)
4. Finish the below-threshold visibility/cancel/reselection behavior (US3)
5. Run automated and quickstart validation before shipping

### Parallel Team Strategy

1. One contributor handles the shared catalogue/bootstrap work in `reservations/management/commands/init_db.py` and `reservations/admin.py`
2. After the shared availability helper lands in `reservations/views.py`, one contributor can focus on the eligible booking flow while another handles the near-date guidance flow
3. Finish with a dedicated pass on the below-threshold persistence rules and the final regression/manual validation tasks
