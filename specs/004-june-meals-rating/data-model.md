# Data Model: Options de repas de juin & notation des repas passés

**Feature**: `004-june-meals-rating`  
**Phase**: 1 — Design

---

## Entity 1 — `DailyMenu` (existing)

Represents the daily menu shown in the calendar for a specific date.

| Field | Type | Description |
|------|------|-------------|
| `date` | Date | Unique day covered by the menu |
| `menu` | String | Menu label shown to employees |

### Rules

- One menu per date.
- June 2026 seeding must create one entry for each working day.
- The menu label should correspond to a selectable meal option when possible.

### Relationships

- Used by the calendar view to determine the default meal selection.

---

## Entity 2 — `MealOption` (existing)

Represents a selectable lunch choice shown in the meal picker.

| Field | Type | Description |
|------|------|-------------|
| `name` | String | Human-readable meal choice |
| `is_active` | Boolean | Whether the option is currently selectable |
| `order` | Integer | Display order / fallback priority |

### Rules

- Active options populate the selector.
- The first active option is the fallback default when no daily menu match exists.

---

## Entity 3 — `Lunch` (existing)

Represents a user reservation for a given date.

| Field | Type | Description |
|------|------|-------------|
| `user` | User | Reservation owner |
| `lunch_date` | Date | Reserved date |
| `lunch_choice` | String | Chosen meal option |

### Rules

- A user can have at most one lunch per date.
- Ratings can only exist for dates with a confirmed lunch.

---

## Entity 4 — `MealRating` (new)

Represents a 1–5 star rating submitted by a user for a past reserved meal.

| Field | Type | Description |
|------|------|-------------|
| `lunch` | One-to-one relation to `Lunch` | The reservation being rated |
| `rating` | Integer | Star rating from 1 to 5 |
| `created_at` | DateTime | When the rating was first submitted |
| `updated_at` | DateTime | When the rating was last modified |

### Rules

- Exactly one rating per confirmed lunch.
- Ratings are allowed only for past lunches.
- Valid values are integers from 1 to 5.
- Updating a rating overwrites the previous value for the same lunch.

### State transitions

- `unrated` → `rated`
- `rated` → `updated`

---

## Derived View Model — `DailyRatingSummary`

Used by the admin monthly recap to display averages without storing aggregated data.

| Field | Type | Description |
|------|------|-------------|
| `date` | Date | Calendar day being summarized |
| `average_rating` | Decimal or null | Mean rating for the day |
| `rating_count` | Integer | Number of submitted ratings |
| `user_ratings` | Collection | Individual user ratings for that day |

### Rules

- Show `Non noté` when `rating_count` is zero.
- Round averages to one decimal place for display.

