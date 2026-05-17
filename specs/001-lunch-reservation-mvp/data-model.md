# Data Model: MVP Lunch Reservation Website

**Phase 1 output** | **Date**: 2026-05-17 | **Plan**: [plan.md](plan.md)

## Overview

The application uses Django's ORM with five logical entities. Four are custom models in
`reservations/models.py`; one is Django's built-in `User` model extended via the
`is_staff` flag.

---

## Entity: User (built-in `auth_user`)

**Table**: `auth_user`
**Managed by**: `django.contrib.auth`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | BigAutoField | PK | |
| `username` | CharField(150) | unique | Stores the matricule (e.g. `K589479`) in UPPERCASE |
| `first_name` | CharField(150) | | Employee first name |
| `last_name` | CharField(150) | | Employee last name |
| `password` | CharField | | Hashed by Django (PBKDF2) |
| `is_staff` | BooleanField | default=False | `True` = CSE staff; grants admin summary access |
| `is_active` | BooleanField | default=True | |

**Validation rules**:
- `username` MUST match regex `^[A-Za-z][0-9]{6}$` (enforced in `RegisterForm`)
- `username` is normalised to UPPERCASE before persistence

**Gap**: CSE badge number (`numéro de badge`) is specified in `app-features.md` (FR-001)
but is not currently stored. Options: (a) add a `Profile` model with a OneToOne to User,
(b) store in an unused `User` field, or (c) accept the gap for the MVP. **Recommended**:
store in `User.email` field (repurposed) or add a thin `UserProfile` model. Deferring
to task G3.

---

## Entity: MealOption

**Table**: `reservations_mealoptionption`
**File**: `reservations/models.py`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | BigAutoField | PK | |
| `name` | CharField(100) | unique | Display name (e.g. "Végétarien", "Viande") |
| `is_active` | BooleanField | default=True | Only active options shown on calendar |
| `order` | PositiveSmallIntegerField | default=0 | Controls display order |

**Ordering**: `["order", "name"]`

**Validation rules**:
- `name` must be unique across all records
- Only records with `is_active=True` are surfaced to employees

**Usage**: `MealOption.objects.filter(is_active=True).values_list("name", flat=True)`
in `calendar_view` — result passed as `options` to template.

---

## Entity: DailyMenu

**Table**: `reservations_dailymenu`
**File**: `reservations/models.py`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | BigAutoField | PK | |
| `date` | DateField | unique | Specific calendar date |
| `menu` | CharField(200) | | Menu description for that day |

**Ordering**: `["date"]`

**Validation rules**:
- One record per calendar date (unique constraint)
- Created/updated via `update_or_create(date=..., defaults={"menu": ...})`

**Fallback logic**: If no `DailyMenu` exists for a given date, `WEEKDAY_MENUS[weekday]`
is used (defined in `views.py`).

---

## Entity: Lunch (Reservation)

**Table**: `reservations_lunch`
**File**: `reservations/models.py`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | BigAutoField | PK | |
| `user` | ForeignKey(User) | CASCADE | Employee who made the reservation |
| `lunch_date` | DateField | | Date of the reservation |
| `lunch_choice` | CharField(100) | blank=True | Selected meal option name |

**Unique constraint**: `unique_together = ("user", "lunch_date")` — one reservation
per employee per day.

**Ordering**: `["user__username", "lunch_date"]`

**Upsert pattern**: `Lunch.objects.update_or_create(user=..., lunch_date=..., defaults={...})`

**Validation rules**:
- `lunch_date` MUST NOT be in the past (enforced in `save_lunch` view, returns HTTP 400)
- `lunch_choice` MUST be validated against active `MealOption.name` values before
  persistence (gap G1 — currently not enforced)

---

## Entity: Suggestion

**Table**: `reservations_suggestion`
**File**: `reservations/models.py`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | BigAutoField | PK | |
| `user` | ForeignKey(User) | CASCADE | Employee who submitted |
| `text` | TextField(500) | | Free-text suggestion content |
| `created_at` | DateTimeField | auto_now_add=True | |
| `is_read` | BooleanField | default=False | Staff read tracking |

**Ordering**: `["-created_at"]`

---

## Relationships Diagram

```
auth_user
  │
  ├──< reservations_lunch (user FK)
  │       └── lunch_date (unique with user)
  │       └── lunch_choice → validated against MealOption.name
  │
  └──< reservations_suggestion (user FK)

reservations_mealoptionption
  └── name (drives calendar option list)

reservations_dailymenu
  └── date (unique; overrides WEEKDAY_MENUS default)
```

---

## Migrations

| Migration | Content |
|-----------|---------|
| `0001_initial.py` | Creates `Lunch` model |
| `0002_dailymenu.py` | Adds `DailyMenu` model |
| `0003_meal_option.py` | Adds `MealOption` model |
| `0004_suggestion.py` | Adds `Suggestion` model |

**Next migration needed**: If CSE badge number field is added to a `UserProfile` model
(gap G3), a new migration `0005_userprofile.py` will be required.

---

## State Transitions

### Lunch Reservation

```
[no reservation] --select option--> [reserved: lunch_choice = X]
[reserved]       --change option--> [reserved: lunch_choice = Y]
[past date]      --any action    --> [rejected: HTTP 400]
```

### MealOption

```
[active: is_active=True]  <--> [inactive: is_active=False]
  (shown on calendar)           (hidden from calendar)
```
