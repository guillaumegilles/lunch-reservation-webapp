# Feature Specification: MVP Lunch Reservation Website

**Feature Branch**: `001-lunch-reservation-mvp`

**Created**: 2026-05-17

**Status**: Draft

**Input**: User description: "MVP lunch reservation website: a simple website to register
employee meal options for production-ready on vercel."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Employee Registration & Authentication (Priority: P1)

An employee creates an account using their company matricule (one letter + six digits),
first name, last name, CSE Nouvelle-Aquitaine badge number, and password. Once registered,
they can log in and out. Unauthenticated users are redirected to the login page for any
protected resource.

**Why this priority**: Authentication is the prerequisite for every other feature. No
reservation, summary, or suggestion is usable without identifying the user.

**Independent Test**: Can be fully tested by registering a new account with a valid
matricule, logging in, and logging out — delivers a working authentication system
independently of any reservation logic.

**Acceptance Scenarios**:

1. **Given** an unauthenticated visitor, **When** they navigate to any protected page,
   **Then** they are redirected to the login page.
2. **Given** the registration form, **When** a user submits a valid matricule, name,
   badge number, and password, **Then** a new account is created and they are redirected
   to the dashboard with a personalised welcome message.
3. **Given** a registered user, **When** they submit correct credentials on the login
   form, **Then** they are authenticated and redirected to the dashboard.
4. **Given** a logged-in user, **When** they click logout, **Then** their session is
   terminated and they are redirected to the login page.
5. **Given** the registration form, **When** a matricule that does not match the required
   format is submitted, **Then** the form is rejected with a clear error message.
6. **Given** the registration form, **When** a matricule already registered in the
   system is submitted, **Then** the form is rejected with a clear error message.

---

### User Story 2 - Meal Reservation via Monthly Calendar (Priority: P2)

A logged-in employee opens the monthly calendar and sees all working days (Monday–Friday)
for the current month. For each upcoming working day, they see the menu of the day and can
select or change their meal option. The selection is saved without a full page reload.
Past dates are locked.

**Why this priority**: This is the core value proposition of the app — replacing manual
lunch collection with a self-service digital process. It directly serves every employee,
every working day.

**Independent Test**: Can be fully tested by a logged-in employee selecting a meal option
for tomorrow, refreshing the page, and confirming the choice persists correctly.

**Acceptance Scenarios**:

1. **Given** a logged-in employee, **When** they open the calendar, **Then** they see all
   working days of the current month with the daily menu displayed for each day.
2. **Given** a future working day on the calendar, **When** the employee selects a meal
   option, **Then** the selection is saved immediately without reloading the page and a
   confirmation is shown.
3. **Given** a previously made reservation, **When** the employee selects a different
   option for the same future day, **Then** the reservation is updated to the new choice.
4. **Given** a past working day, **When** the employee attempts to select or change a meal
   option, **Then** the action is rejected and an error message is shown.
5. **Given** the calendar, **When** the employee clicks "previous month" or "next month",
   **Then** the calendar updates to display that month's working days.

---

### User Story 3 - Monthly Admin Summary (Priority: P3)

A CSE staff member accesses the admin summary page, which displays a monthly table listing
every employee's meal choice for each working day. Staff can navigate between months to
review past or future reservation data.

**Why this priority**: This directly replaces the manual counting and spreadsheet work
currently done by CSE staff. Without it, the app solves only the employee side of the
problem.

**Independent Test**: Can be tested independently by creating employee accounts with
reservations and verifying the admin summary correctly displays all choices in a monthly
table, restricted to staff-only access.

**Acceptance Scenarios**:

1. **Given** a CSE staff user, **When** they navigate to the admin summary page, **Then**
   they see a monthly table listing every employee's meal choice per working day.
2. **Given** a non-staff employee, **When** they attempt to access the admin summary page,
   **Then** they are redirected with an error message.
3. **Given** the admin summary, **When** the staff user navigates to a different month,
   **Then** the table updates to show that month's reservation data.

---

### User Story 4 - Weekly Menu Management (Priority: P4)

A CSE staff member sets the daily menu for each working day of a chosen week via a form
on the admin summary page. These custom menus override the system defaults and appear in
the employee calendar.

**Why this priority**: Without customised daily menus, the calendar displays only a static
default list, reducing the app's practical relevance to day-to-day catering needs.

**Independent Test**: Can be tested by a staff user entering a custom menu for next week,
then logging in as an employee and confirming the calendar shows the custom entries.

**Acceptance Scenarios**:

1. **Given** a CSE staff user, **When** they submit the weekly menu form for a chosen
   week, **Then** each specified day displays the custom menu in the employee calendar.
2. **Given** a day with a custom menu defined, **When** an employee views that day,
   **Then** the custom menu is shown instead of the system default.
3. **Given** a day without a custom menu, **When** an employee views that day,
   **Then** the system-default menu for that weekday is displayed.

---

### User Story 5 - Employee Suggestion Submission (Priority: P5)

A logged-in employee submits a free-text suggestion from the dashboard. An email
notification is sent to the configured CSE recipient address, and the employee sees
a success or error flash message.

**Why this priority**: Supports communication between employees and CSE management.
Lower priority as it does not affect the core reservation workflow.

**Independent Test**: Can be tested by submitting a suggestion and verifying the email
is sent (or logged in development) and the correct flash message is displayed.

**Acceptance Scenarios**:

1. **Given** a logged-in employee on the dashboard, **When** they submit the suggestion
   form with text, **Then** an email is sent to the configured CSE recipient and a
   success flash message is shown.
2. **Given** a suggestion submission, **When** email delivery fails, **Then** the user
   sees an error flash message and no data is silently lost.

---

### Edge Cases

- What happens when a matricule already in use is submitted during registration? The form
  is rejected with a clear error message; no duplicate account is created.
- What happens when no meal options are currently active? The calendar displays working
  days but employees cannot make a selection until staff activates options.
- What happens when an employee navigates to a month entirely in the past? Working days
  are shown but all are locked; no reservation can be made or changed.
- What happens when the email service is unavailable during a suggestion submission? The
  system displays an error flash message; no silent failure occurs.
- What happens when a non-staff user attempts to access the admin summary URL directly?
  They are redirected to the dashboard with an error message.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow employees to register with a unique matricule (format:
  one letter + six digits), first name, last name, CSE badge number, and a valid password.
- **FR-002**: System MUST authenticate users by session; unauthenticated users MUST be
  redirected to the login page when accessing any protected resource.
- **FR-003**: System MUST display a monthly calendar showing only working days
  (Monday–Friday) with the daily menu for each day.
- **FR-004**: Employees MUST be able to select or update their meal option for any
  upcoming working day; past dates MUST be locked from modification.
- **FR-005**: System MUST save meal selections without a full page reload and confirm the
  save to the user via an inline update.
- **FR-006**: System MUST reject any attempt to create or modify a reservation for a past
  date and return an explicit error response.
- **FR-007**: System MUST display a monthly admin summary table listing each employee's
  meal choice per working day, accessible only to CSE staff.
- **FR-008**: CSE staff MUST be able to define the daily menu for each day of a chosen
  week; these menus MUST override the system defaults in the employee calendar.
- **FR-009**: Employees MUST be able to submit free-text suggestions from the dashboard;
  each submission MUST trigger an email notification to the configured recipient.
- **FR-010**: System MUST display all UI text, labels, and flash messages in French.
- **FR-011**: System MUST be deployable to Vercel without code changes; all
  environment-specific settings MUST be supplied via environment variables.

### Key Entities

- **Employee (User)**: Represents a company employee identified by a unique matricule,
  with first name, last name, and CSE badge number. A staff flag distinguishes CSE
  administrators from regular employees.
- **Meal Reservation**: A single employee's meal choice for a specific working day.
  Uniquely constrained to one record per employee per day; supports both creation and
  update (upsert).
- **Meal Option**: An active, selectable menu choice managed by CSE staff. The set of
  active options determines what employees can choose on the calendar.
- **Daily Menu**: A custom menu entry created by CSE staff for a specific calendar day.
  Overrides the system default for that day in the employee-facing calendar.
- **Suggestion**: A free-text message submitted by an employee from the dashboard,
  triggering an email notification to the CSE recipient.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An employee can register, log in, and record their lunch preference for
  tomorrow in under 30 seconds.
- **SC-002**: CSE staff can view a complete monthly reservation summary for all employees
  with zero manual data entry or aggregation.
- **SC-003**: No reservation can be created or modified for a past date — this constraint
  must be enforced 100% of the time with no client-side bypass.
- **SC-004**: The application is accessible from a standard web browser on desktop and
  mobile without installing any native application.
- **SC-005**: All user-facing text, labels, and notifications are displayed in French.
- **SC-006**: The application deploys successfully to Vercel from source with no manual
  server administration required after initial environment variable configuration.

## Assumptions

- All users (employees and CSE staff) are internal to the organisation; no public
  self-registration beyond the standard registration form is required.
- Payment, billing, dietary restriction tracking, and allergen management are explicitly
  out of scope for this MVP.
- A native mobile application is out of scope; the web interface is expected to be
  usable on mobile browsers.
- The default meal options per weekday are pre-configured during initial database setup
  and can be managed via the Django admin interface.
- The CSE staff recipient email address for suggestions is configured once via an
  environment variable and does not change at runtime.
- A default admin user account is created via a management command during initial
  deployment to allow first-time CSE staff access.
- The production database is PostgreSQL hosted externally and connected via the
  `DATABASE_URL` environment variable; SQLite is used for local development only.
