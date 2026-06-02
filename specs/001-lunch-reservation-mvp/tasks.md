# Tasks: MVP Lunch Reservation Website

**Input**: Design documents from `specs/001-lunch-reservation-mvp/`

**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/ ✅

**Context**: The core Django application is largely implemented. These tasks fix the four
identified gaps (G1–G4), implement the 7-day advance booking rule (clarified post-spec),
add reservation cancellation support, and persist badge numbers and suggestions to the
database. US3 and US4 are already fully implemented and tested — those phases contain
only checkpoint verification tasks.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no inter-task dependency)
- **[Story]**: User story label (US1–US5) — Setup and Foundational phases carry no label

---

## Phase 1: Setup

**Purpose**: Dependency hygiene before any code changes.

- [X] T001 Pin exact dependency versions in `requirements.txt`: run `pip freeze` in the
  project virtualenv and replace the current `>=` constraints for `Django`, `dj-database-url`,
  and `psycopg2-binary` with `==<exact-version>`. Remove the bare `uv` entry (build tool,
  not a runtime dependency). Example result: `Django==5.2.1`, `dj-database-url==2.3.0`,
  `psycopg2-binary==2.9.10`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add the `UserProfile` model needed to persist badge numbers (G3 fix) and seed
the default `MealOption` records that the calendar requires on first deploy. Both must complete
before any user story work begins.

**⚠️ CRITICAL**: Phases 3–7 cannot begin until T002–T005 are complete.

- [X] T002 Add `UserProfile` model to `reservations/models.py`: `user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="profile")`, `badge_number = CharField(max_length=50)`. Place it after the `Suggestion` class. Import `settings` from `django.conf` if not already imported.

- [X] T003 Generate and verify migration: run `python manage.py makemigrations reservations`
  from the project root. Confirm it creates `reservations/migrations/0005_userprofile.py`
  with a `CreateModel` for `UserProfile` and the `OneToOneField` to `auth.User`. Run
  `python manage.py migrate` to apply it locally.

- [X] T004 Extend `reservations/management/commands/init_db.py` to seed the full default
  `MealOption` set so the calendar is usable on first deploy without staff intervention:
  add `update_or_create` calls for "🥗 Plat du jour" (order=10), "🐟 Poisson" (order=20),
  "🥩 Steak haché" (order=30), "🍳 Œufs brouillés" (order=40), and "🍝 Pâtes" (order=50).
  These mirror the five `WEEKDAY_MENUS` weekday defaults. The existing "🥩 Steak haché"
  entry can be merged into the new order=30 record; rename "🍳 Omelette" to
  "🍳 Œufs brouillés" (order=40) via `update_or_create` so old data is updated idempotently.
  Confirm `python manage.py init_db` is idempotent by running it twice — `MealOption` count
  must not grow on the second run.

- [X] T005 [P] Register `UserProfile` as a `StackedInline` on `UserAdmin` in
  `reservations/admin.py`: define `class UserProfileInline(admin.StackedInline)` with
  `model = UserProfile`, `can_delete = False`, then add it via
  `admin.site.unregister(User)` / `admin.site.register(User, UserAdminWithProfile)`.
  Import `User` from `django.contrib.auth.models` and `UserProfile` from `.models`.

**Checkpoint**: `python manage.py migrate` completes without error; `python manage.py init_db`
seeds ≥5 active `MealOption` records; `/django-admin/` shows the User change page with the
badge-number inline.

---

## Phase 3: User Story 1 — Registration & Authentication (Priority: P1)

**Goal**: Badge number collected at registration is persisted to `UserProfile`; all
existing auth flows (login, logout, redirect guards) remain unchanged.

**Independent Test**: Register a new account via `POST /register/`, then run
`python manage.py shell -c "from reservations.models import UserProfile; print(UserProfile.objects.get(user__username='K589479').badge_number)"` — must print the submitted badge number.

### Implementation for User Story 1

- [X] T006 [US1] Update `register_view` in `reservations/views.py` to create a
  `UserProfile` after `User.objects.create_user(...)`: add
  `UserProfile.objects.create(user=new_user, badge_number=badge_number)` immediately
  after the user creation line. Import `UserProfile` from `.models` at the top of the
  file. No changes to form, template, or URL.

- [X] T007 [US1] Update `test_register_creates_user_and_redirects` in
  `reservations/tests/test_views.py`: after the existing `User` assertions, add
  `from reservations.models import UserProfile` at the top of the file and assert
  `UserProfile.objects.filter(user__username="K589479", badge_number="123456").exists()`
  is True.

**Checkpoint**: `python manage.py test reservations.tests.test_views.AuthFlowTests` — all
6 existing auth tests pass plus the updated assertion in T007.

---

## Phase 4: User Story 2 — Meal Reservation via Monthly Calendar (Priority: P2)

**Goal**: Calendar shows `MealOption`-driven choices (G1 fix); days fewer than 7 calendar
days away are locked in both UI and server-side; employees can cancel a reservation for
any eligible day.

**Independent Test**: Create a `MealOption` fixture with `name="Végétarien"`. Log in,
open `/calendar/`, confirm the "Végétarien" option appears in the dropdown, confirm days
within 7 days show as locked, confirm selecting and cancelling a reservation for a day
≥ 7 days away works without page reload.

### Implementation for User Story 2

- [X] T008 [US2] Update `calendar_view` in `reservations/views.py`:
  1. Import `MealOption` from `.models` (add alongside existing `DailyMenu, Lunch` import).
  2. Replace `"alternative_options": CALENDAR_ALTERNATIVE_OPTIONS` in the render context
     with `"options": list(MealOption.objects.filter(is_active=True).values_list("name", flat=True))`.
  3. Add `is_locked` per day: in the day-building loop, add
     `"is_locked": current_date < date.today() + timedelta(days=7)` to each day dict.
  4. Remove the `CALENDAR_ALTERNATIVE_OPTIONS` constant from `views.py` entirely.

  > **⚠️ Sequential note (H2)**: T008 and T010 MUST NOT run in parallel — both modify
  > `reservations/views.py` and both reference the `CALENDAR_ALTERNATIVE_OPTIONS` constant.
  > T008 removes the constant and rewrites the calendar context; T010 then rewrites the
  > `save_lunch` MealOption validation to replace the now-removed constant's role. Running
  > them simultaneously would produce a merge conflict on the constant removal line. Complete
  > T008 (and verify it compiles) before starting T010.

- [X] T009 [US2] Update `save_lunch` in `reservations/views.py` — 7-day guard:
  Replace the line `if lunch_date < date.today():` with
  `if lunch_date < date.today() + timedelta(days=7):` and update the error message to
  `"Impossible de réserver moins de 7 jours à l'avance."`. The `timedelta` import is
  already present.

- [X] T010 [US2] Update `save_lunch` in `reservations/views.py` — MealOption validation
  (G1 fix): Replace the block that builds `allowed_choices` from `DailyMenu` +
  `CALENDAR_ALTERNATIVE_OPTIONS` with:
  ```python
  valid_options = set(MealOption.objects.filter(is_active=True).values_list("name", flat=True))
  if lunch not in valid_options:
      return JsonResponse({"status": "error", "message": "Option de repas invalide."}, status=400)
  ```
  Remove the now-unused `DEFAULT_DAILY_MENU` and `CALENDAR_ALTERNATIVE_OPTIONS` references
  from `save_lunch`. Remove those constants from `views.py` entirely if no other view
  uses them. [depends on T008 completing first — `CALENDAR_ALTERNATIVE_OPTIONS` must be
  removed from the file before this task can cleanly replace its usage in `save_lunch`]

- [X] T011 [US2] Add cancellation support to `save_lunch` in `reservations/views.py`:
  After the 7-day guard, add a branch before the MealOption validation:
  ```python
  if lunch == "":
      Lunch.objects.filter(user=request.user, lunch_date=lunch_date).delete()
      return JsonResponse({"status": "success", "message": "Réservation annulée."})
  ```
  This allows an empty `lunch` value to signal cancellation for an eligible date.

- [X] T012 [US2] Update `calendar.html` in `reservations/templates/calendar.html`:
  1. In the day loop, conditionally suppress `onclick` for locked days:
     `{% if not d.is_locked %}onclick="selectDay({{ d.day }})"{% endif %}`.
  2. Add a CSS class for locked days: `{% if d.is_locked %}locked-day{% endif %}` on the
     inner `selectable-day` div (style with `opacity: 0.4; cursor: default;`).
  3. Replace the JS `const alternatives = {{ alternative_options|safe }};` line with
     `const options = {{ options|safe }};` and update `syncLunchOption` to iterate
     `options` instead of `[defaultMenu, ...alternatives]` — the `options` list from the
     server already contains all active `MealOption` names; no client-side deduplication
     with a day menu needed.
  4. Add an "Annuler la réservation" button below the save button:
     ```html
     <button class="btn btn-outline-danger w-100 mb-2" onclick="cancelLunch()">Annuler la réservation</button>
     ```
     Add `cancelLunch()` JS function that POSTs `{ day: selectedDay, lunch: "", year, month }`
     to `/save-lunch/` and clears the `.lunch-label` on success.

- [X] T013 [P] [US2] Update `test_save_lunch_for_future_date_creates_or_updates_entry`
  in `reservations/tests/test_views.py`: change `timedelta(days=1)` to `timedelta(days=8)`
  so the test date is within the bookable window. Also create a `MealOption` fixture
  (`MealOption.objects.create(name="Plat du jour", is_active=True)`) in the test's `setUp`
  so the choice passes the new validation.

- [X] T014 [P] [US2] Update `test_save_lunch_for_past_date_returns_400` and
  `test_save_lunch_rejects_invalid_option` in `reservations/tests/test_views.py`:
  add `MealOption.objects.create(name="Plat du jour", is_active=True)` to `setUp` of
  `CalendarAndLunchTests`; ensure the invalid-option test still uses a name not in
  `MealOption` (e.g., `"Steak"` remains invalid). Add a new test
  `test_save_lunch_within_7_days_returns_400` that uses `date.today() + timedelta(days=3)`
  and expects HTTP 400.

- [X] T015 [P] [US2] Add `test_save_lunch_cancellation_deletes_reservation` to
  `CalendarAndLunchTests` in `reservations/tests/test_views.py`: create a `Lunch` record
  for `date.today() + timedelta(days=8)`, then POST `{"lunch": ""}` to `/save-lunch/` for
  that date, assert HTTP 200 and `Lunch.objects.filter(...).exists()` is False. Also add
  `test_calendar_options_come_from_meal_option_model` to assert `response.context["options"]`
  matches active `MealOption` names.

**Checkpoint**: `python manage.py test reservations.tests.test_views.CalendarAndLunchTests`
— all tests pass with the new 7-day rule and MealOption validation.

---

## Phase 5: User Story 3 — Monthly Admin Summary (Priority: P3)

**Goal**: Already fully implemented. Verify no regressions after Phase 4 changes.

**Independent Test**: `python manage.py test reservations.tests.test_views.AdminSummaryTests`

- [X] T016 [US3] Run `python manage.py test reservations.tests.test_views.AdminSummaryTests`
  and confirm all 4 existing tests pass unchanged. If any test fails due to Phase 4
  changes (e.g., MealOption fixture missing), add the necessary fixture to `setUp` in
  `AdminSummaryTests` without modifying the test assertions.

**Checkpoint**: All `AdminSummaryTests` pass — no new implementation required for US3.

---

## Phase 6: User Story 4 — Weekly Menu Management (Priority: P4)

**Goal**: Already fully implemented. Verify no regressions.

**Independent Test**: `python manage.py test reservations.tests.test_views.AdminSummaryTests`
(US4 tests are in the same class as US3.)

- [X] T017 [US4] Confirm `test_staff_can_create_weekly_menus` and
  `test_staff_weekly_menu_requires_monday` still pass after Phase 4 changes. No code
  changes expected — this is a regression guard checkpoint.

**Checkpoint**: US4 tests green — no new implementation required for US4.

---

## Phase 7: User Story 5 — Employee Suggestion Submission (Priority: P5)

**Goal**: Suggestions are persisted to the `Suggestion` table (currently only emailed, never
saved to DB). The `is_read` field becomes usable via Django admin.

**Independent Test**: Submit a suggestion via `POST /suggestion-submit/`, then open
`/django-admin/reservations/suggestion/` and confirm the record appears.

### Implementation for User Story 5

- [X] T018 [US5] Update `submit_suggestion` in `reservations/views.py`: add
  `from .models import ... Suggestion` to the existing models import line, then inside
  the `if form.is_valid():` block, before `send_mail(...)`, add
  `Suggestion.objects.create(user=request.user, text=text)`. The suggestion is saved
  regardless of email delivery outcome; the `is_read` field defaults to `False`.

- [X] T019 [P] [US5] Update `test_authenticated_user_can_submit_suggestion` in
  `reservations/tests/test_views.py`: after the existing email assertions, add
  `from reservations.models import Suggestion` at the top and assert
  `Suggestion.objects.filter(user=self.user, text="Ajouter un rappel sur le dashboard.").exists()`
  is True.

**Checkpoint**: `python manage.py test reservations.tests.test_views.SuggestionTests`
— both tests pass; suggestion record visible in Django admin.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finalise documentation, run the full test suite, and verify deployment config.

- [X] T020 Update `.github/copilot-instructions.md` (G4 fix): in the `## Database` section,
  remove the reference to the `LUNCH_OPTIONS` list constant; replace with a description
  of the `MealOption` model: "Meal options are managed via `MealOption` model records
  (`name`, `is_active`, `order`). Active options are fetched with
  `MealOption.objects.filter(is_active=True)`." Verify no other section still references
  `LUNCH_OPTIONS` or `CALENDAR_ALTERNATIVE_OPTIONS`.

- [X] T021 [P] Update `reservations/tests/test_management_commands.py`: add
  `test_init_db_seeds_default_meal_options` asserting that after `call_command("init_db")`
  there are ≥5 active `MealOption` records and all five WEEKDAY_MENUS defaults are present
  by name (e.g., `MealOption.objects.filter(name__startswith="🥗").exists()` is True).
  Verify idempotency: call `init_db` twice and confirm `MealOption.objects.count()` is
  unchanged on the second run.

- [X] T022 [P] Run `python manage.py test reservations` from the project root and confirm
  all tests pass. Fix any remaining failures before proceeding to T023.

- [X] T023 [P] Verify Vercel deployment readiness: confirm `vercel.json` `buildCommand`
  is `pip install -r requirements.txt && python manage.py migrate && python manage.py
  collectstatic --noinput`; confirm `vercel.json` pins `python3.12` runtime in the
  `@vercel/python` build config; confirm `quickstart.md` reflects the 7-day advance
  booking rule, the `UserProfile` model addition, and that `init_db` seeds default
  `MealOption` records (post-T004); confirm no SQLite database file is committed
  (check `.gitignore`).

**Checkpoint**: Full test suite green; `vercel.json` unchanged; `quickstart.md` accurate.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1. Blocks Phases 3–7.
- **Phase 3 (US1)**: Depends on Phase 2 completion (needs `UserProfile` model).
- **Phase 4 (US2)**: Can start after Phase 2; independent of Phase 3.
- **Phase 5 (US3)**: Depends on Phase 4 completion (regression guard).
- **Phase 6 (US4)**: Depends on Phase 4 completion (regression guard).
- **Phase 7 (US5)**: Independent of Phases 3–6; can run after Phase 2.
- **Phase 8 (Polish)**: Depends on all previous phases.

### User Story Dependencies

| Story | Depends On | Can Parallelise With |
|-------|-----------|---------------------|
| US1 (Phase 3) | Phase 2 | US5 (Phase 7) |
| US2 (Phase 4) | Phase 2 | US1, US5 |
| US3 (Phase 5) | Phase 4 | — |
| US4 (Phase 6) | Phase 4 | — |
| US5 (Phase 7) | Phase 2 | US1, US2 |

### Within Each Phase

- Tasks marked `[P]` have no intra-phase file conflicts and can run in parallel.
- T008 → T009 → T010 → T011 (all in `views.py`): apply sequentially to avoid conflicts.
  T008 and T010 in particular MUST NOT be parallelised (see ⚠️ note in T008 — both touch
  the `CALENDAR_ALTERNATIVE_OPTIONS` constant).
- T013, T014, T015 are test-file tasks marked `[P]` — parallelisable once T008–T012 are done.

---

## Parallel Examples

```bash
# After Phase 2 completes, these tasks touch different files and can run in parallel:
Task T006  # [US1] register_view badge_number persistence — views.py
Task T007  # [US1] AuthFlowTests test update — tests/test_views.py
Task T019  # [US5] SuggestionTests update — tests/test_views.py (SuggestionTests)
# Note: T006, T008, T018 all touch views.py — coordinate edits to avoid conflicts.
# T012 (calendar.html) requires T008–T011 to complete first — do NOT launch with Phase 2.
# After T008–T012 complete (Phase 4), these test tasks can run in parallel:
Task T013  # [US2] CalendarAndLunchTests — 7-day rule guard
Task T014  # [US2] CalendarAndLunchTests — MealOption validation
Task T015  # [US3] AdminSummaryTests — regression
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1 + Phase 2 (Setup + Foundational)
2. Complete Phase 3 (US1 — badge number persistence)
3. **STOP and VALIDATE**: Register user, confirm `UserProfile.badge_number` is saved
4. Deploy to verify no Vercel breakage

### Incremental Delivery

1. Phases 1–2 → Foundation ready
2. Phase 3 (US1) → Auth complete with badge number ✅
3. Phase 4 (US2) → Calendar with 7-day rule, MealOption, cancellation ✅
4. Phases 5–6 (US3/US4) → Verify existing features still work ✅
5. Phase 7 (US5) → Suggestions persisted to DB ✅
6. Phase 8 → Polish, full test run, Vercel check ✅

---

## Notes

- All views live in a single `reservations/views.py` — T006, T008–T011, T018 all modify
  it. Apply them sequentially within their phase.
- `CALENDAR_ALTERNATIVE_OPTIONS` and `DEFAULT_DAILY_MENU` constants in `views.py` become
  unused after T008/T010 — remove them to avoid confusion.
- T004 seeds `MealOption` records in `init_db`; T021 adds a test for this. Without T004,
  the calendar page renders with no selectable options on a fresh deploy.
- No new migrations are needed beyond T003 (`UserProfile`) — all other changes are
  view/template/test updates.
- `[P]` tasks within Phase 4 (T013, T014, T015) can only start once T008–T012 are done
  so the test updates target the correct new behaviour.
