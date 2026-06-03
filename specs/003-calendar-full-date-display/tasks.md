# Tasks: Affichage de la date complète dans le calendrier

**Input**: Design documents from `specs/003-calendar-full-date-display/`  
**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/ ✅ | quickstart.md ✅

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other tasks that touch different files
- **[Story]**: `US1`, `US2`, etc. Setup, Foundational, and Polish phases carry no story label

---

## Phase 1: Setup

**Purpose**: Capture the current baseline before changing the UI copy or date formatting.

- [X] T001 Run `python manage.py test` from the repo root and record the current passing baseline before editing `reservations/views.py` or any file under `reservations/templates/`.

**Checkpoint**: Baseline confirmed and ready for the feature work.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add the shared French date-label logic that both user stories depend on.

- [X] T002 Add French weekday and month label helpers in `reservations/views.py`: define explicit mappings for `lundi`→`dimanche` and `janvier`→`décembre`, then create a helper that formats full labels like `Lundi 14 juin` and expose `month_name_fr` in the calendar/admin view contexts for the visible headings.

**Checkpoint**: Shared French date formatting is available for both pages.

---

## Phase 3: User Story 1 - Lire la date complète sur chaque jour du calendrier (Priority: P1) 🎯 MVP

**Goal**: The calendar page shows the full French date on every workday, and the selected-day panel uses the same full label.

**Independent Test**: Open `/calendar/` for any month and verify each day cell shows `Jour + numéro + mois` in French, while the selection panel shows the same full label after clicking a day.

### Implementation for User Story 1

- [X] T003 [US1] Update `reservations/views.py` `calendar_view` to populate each `days` entry with the French weekday label and the full display label, while keeping `menu`, `lunch`, and `is_locked` unchanged, and pass `month_name_fr` for the visible calendar heading.

- [X] T004 [US1] Update `reservations/templates/calendar.html` to render `d.full_label` in each day cell, show the selected day as the full French date in the selection panel, use `month_name_fr` in the visible calendar title, and replace the remaining calendar-page English labels (`Lunch Reservation`, `Previous`, `Next`, `Dashboard`, `Logout`, `Admin Page`) with French equivalents.

- [X] T005 [US1] Adjust `reservations/static/custom.css` so the longer full-date labels fit cleanly in calendar cells on desktop and mobile without clipping, truncation, or breaking the grid at 375px and 768px widths.

**Checkpoint**: The calendar page is fully usable with full French date labels.

---

## Phase 4: User Story 2 - Cohérence de la langue française sur toute l'interface (Priority: P2)

**Goal**: Every remaining visible label across the app is fully French, including page titles, buttons, links, and accessibility labels.

**Independent Test**: Inspect the app pages (`/`, `/login/`, `/register/`, `/dashboard/`, `/calendar/`, `/admin-summary/`) and confirm no visible English text remains.

### Implementation for User Story 2

- [X] T006 [P] [US2] Update `reservations/templates/base.html` to use a French site title and French navbar copy, including the dismiss button `aria-label` set to `Fermer`.

- [X] T007 [P] [US2] Update `reservations/templates/index.html`, `reservations/templates/login.html`, `reservations/templates/register.html`, and `reservations/templates/dashboard.html` so every visible title, button, link, and accessibility label is French and no `Lunch Reservation`/`Close` strings remain.

- [X] T008 [P] [US2] Update `reservations/templates/admin.html` so the browser title and visible month heading both use `month_name_fr`, and the month navigation, return button, and table header are all in French (`Récapitulatif mensuel`, `Précédent`, `Suivant`, `Retour`, `Employé`).

**Checkpoint**: All pages now read consistently in French.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Validate the full feature and catch any remaining copy or layout issues.

- [X] T009 [P] Run `python manage.py test` from the repo root and fix any regressions introduced in `reservations/views.py`, `reservations/templates/`, or `reservations/static/custom.css`.

- [X] T010 [P] Sweep `reservations/templates/` and `reservations/views.py` for any remaining English UI text and replace any stragglers with French equivalents.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 (Phase 4)**: Depends on Foundational.
- **Polish (Phase 5)**: Depends on User Stories 1 and 2.

### User Story Dependencies

- **US1 (P1)**: Can start immediately after the shared French date helpers are added.
- **US2 (P2)**: Can start after the shared French date helpers are added and does not depend on US1.

### Within Each User Story

- Shared helpers first, then template rendering, then styling tweaks.
- Keep calendar-specific copy changes together so the selected-day behavior and full-date label stay aligned.
- Keep page-title/copy changes grouped by template file to reduce merge conflicts.

### Parallel Opportunities

- `T006`, `T007`, and `T008` can run in parallel because they touch different template files.
- `T009` and `T010` can run in parallel after the implementation tasks finish.

---

## Parallel Example: User Story 2

```bash
Task: "Update reservations/templates/base.html to use a French site title and French navbar copy"
Task: "Update reservations/templates/index.html, reservations/templates/login.html, reservations/templates/register.html, and reservations/templates/dashboard.html"
Task: "Update reservations/templates/admin.html so the title, month navigation, return button, and table header are all in French"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate the calendar page before touching the remaining templates

### Incremental Delivery

1. Add the shared French date helpers
2. Deliver the calendar page with full French date labels
3. Normalize the rest of the UI copy across all templates
4. Finish with a full test pass and a final copy sweep

### Parallel Team Strategy

1. One contributor handles the shared `reservations/views.py` date helpers
2. After that lands, one contributor can finish the calendar page while another normalizes the remaining templates
3. Run the final test and copy-sweep tasks in parallel
