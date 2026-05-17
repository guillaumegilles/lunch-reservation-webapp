# HTTP Endpoint Contracts: MVP Lunch Reservation Website

**Phase 1 output** | **Date**: 2026-05-17 | **Plan**: [../plan.md](../plan.md)

All endpoints are defined in `reservations/urls.py` and implemented in
`reservations/views.py`.

---

## Public Endpoints (no authentication required)

### GET /

**View**: `index`
**Template**: `index.html`

**Behaviour**:
- If the user is authenticated → redirect to `GET /dashboard/`
- Otherwise → render the landing page (shows list of registered usernames for quick login)

**Response**: `200 OK` (HTML) or `302` redirect to `/dashboard/`

---

### GET /login/

**View**: `login_view`
**Template**: `login.html`

**Response**: `200 OK` (HTML) — renders `LoginForm`

---

### POST /login/

**View**: `login_view`

**Request body** (form-encoded):

| Field | Type | Constraints |
|-------|------|-------------|
| `identifier` | string | Required; regex `^[A-Za-z][0-9]{6}$`; normalised to UPPERCASE |
| `password` | string | Required |

**Responses**:
- `302` → `/dashboard/` on success (session cookie set)
- `200` → `login.html` with error flash message on invalid credentials or form errors

---

### GET /register/

**View**: `register_view`
**Template**: `register.html`

**Response**: `200 OK` (HTML) — renders `RegisterForm`

---

### POST /register/

**View**: `register_view`

**Request body** (form-encoded):

| Field | Type | Constraints |
|-------|------|-------------|
| `identifier` | string | Required; regex `^[A-Za-z][0-9]{6}$`; must be unique |
| `last_name` | string | Required |
| `first_name` | string | Required |
| `password` | string | Required; must pass Django password validators |
| `confirm_password` | string | Required; must match `password` |

**Responses**:
- `302` → `/login/` on success
- `200` → `register.html` with error flash message on validation failure or duplicate identifier

---

## Protected Endpoints (authentication required — redirects to /login/ if unauthenticated)

### GET /logout/

**View**: `logout_view`
**Method**: GET (requires `@login_required`)

**Behaviour**: Ends the user session.

**Response**: `302` → `/` (index)

---

### GET /dashboard/

**View**: `dashboard_view`
**Template**: `dashboard.html`

**Context**:
| Variable | Type | Notes |
|----------|------|-------|
| `username` | string | `request.user.username` |
| `first_name` | string | `request.user.first_name` |
| `is_staff` | bool | `request.user.is_staff` |
| `form` | SuggestionForm | Blank suggestion form |

**Response**: `200 OK` (HTML)

---

### POST /suggestion-submit/

**View**: `submit_suggestion`
**Requires**: `@login_required`, `@require_POST`

**Request body** (form-encoded):

| Field | Type | Constraints |
|-------|------|-------------|
| `text` | string | Required; max 500 characters |

**Behaviour**:
- Sends email to `settings.SUGGESTION_RECIPIENT_EMAIL`
- On success: `messages.success` flash
- On email failure: `messages.error` flash
- On form invalid: `messages.error` flash

**Response**: `302` → `/dashboard/` (always redirects)

---

### GET /calendar/

**View**: `calendar_view`
**Template**: `calendar.html`

**Query parameters**:

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `year` | int | current year | |
| `month` | int | current month | 1–12 |

**Context**:
| Variable | Type | Notes |
|----------|------|-------|
| `year` | int | |
| `month` | int | |
| `month_name` | string | Localised month name |
| `days` | list[dict] | `{day, weekday, menu, lunch}` — working days only |
| `options` | list[str] | Active `MealOption.name` values |
| `prev_year`, `prev_month` | int | For navigation |
| `next_year`, `next_month` | int | For navigation |

**Response**: `200 OK` (HTML)

---

### POST /save-lunch/

**View**: `save_lunch`
**Requires**: `@login_required`, `@require_POST`
**Content-Type**: `application/json`
**Headers**: `X-CSRFToken: <token>`

**Request body** (JSON):

```json
{
  "day": 15,
  "month": 6,
  "year": 2026,
  "lunch": "Végétarien"
}
```

| Field | Type | Constraints |
|-------|------|-------------|
| `day` | int | Day of month |
| `month` | int | 1–12 |
| `year` | int | |
| `lunch` | string | Meal option name; MUST match an active `MealOption` (gap G1) |

**Responses**:

`200 OK` — reservation saved or updated:
```json
{ "status": "success", "message": "Dejeuner enregistre." }
```

`400 Bad Request` — date is in the past:
```json
{ "status": "error", "message": "Impossible de modifier un dejeuner passe." }
```

`400 Bad Request` (after G1 fix) — invalid lunch option:
```json
{ "status": "error", "message": "Option de repas invalide." }
```

---

### GET /admin-summary/

**View**: `admin_summary`
**Template**: `admin.html`
**Requires**: `@login_required` + `request.user.is_staff`

**Query parameters**:

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `year` | int | current year | |
| `month` | int | current month | |

**Context**:
| Variable | Type | Notes |
|----------|------|-------|
| `table_rows` | list[dict] | `{username, choices[]}` per employee |
| `days` | list[int] | Working day numbers for the month |
| `year`, `month`, `month_name` | | |
| `prev_year/month`, `next_year/month` | int | Navigation |
| `weekly_menu_form` | WeeklyMenuForm | Prefilled with current week |

**Access control**:
- Non-staff user → `302` redirect to `/calendar/` with error flash message

**Response**: `200 OK` (HTML)

---

### POST /admin-summary/

**View**: `admin_summary` (handles `WeeklyMenuForm` submission)
**Requires**: `@login_required` + `request.user.is_staff`

**Request body** (form-encoded):

| Field | Type | Constraints |
|-------|------|-------------|
| `week_start` | date | Must be a Monday |
| `monday_menu` | string | Max 200 chars |
| `tuesday_menu` | string | Max 200 chars |
| `wednesday_menu` | string | Max 200 chars |
| `thursday_menu` | string | Max 200 chars |
| `friday_menu` | string | Max 200 chars |
| `summary_year` | int | Optional; used for redirect target |
| `summary_month` | int | Optional; used for redirect target |

**Behaviour**: Creates or updates `DailyMenu` records for Mon–Fri of the chosen week.

**Responses**:
- `302` → `/admin-summary/?year=...&month=...` on success with `messages.success` flash
- `200` → `admin.html` with form errors if `week_start` is not a Monday or form invalid

---

## Django Admin

### /django-admin/

Provides full CRUD for `MealOption`, `DailyMenu`, `Lunch`, and `Suggestion` models.
Access requires `is_staff=True` (or `is_superuser=True`). Not part of the user-facing app.
