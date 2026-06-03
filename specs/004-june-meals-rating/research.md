# Research: Options de repas de juin & notation des repas passés

**Feature**: `004-june-meals-rating`  
**Phase**: 0 — Research

---

## 1. June menu seeding strategy

### Context

The spec needs realistic daily menus for June 2026, with idempotent population and no manual data entry.

### Decision

Create a dedicated management command for June menus, separate from the existing bootstrap command that seeds the admin account and active meal options.

### Rationale

A feature-specific command keeps the bootstrap command focused, makes the June data easier to rerun safely, and avoids coupling one-off calendar content to generic initialization.

### Alternatives considered

- Extending `init_db`: rejected because it mixes feature data with general bootstrap responsibilities.
- Importing data through the admin UI: rejected because the spec wants a repeatable, non-manual population path.

---

## 2. Default selection for the meal picker

### Context

The calendar already renders the active `MealOption` list. The new requirement is that the daily menu should be preselected when it matches an active option, with a safe fallback when no match exists.

### Decision

Compute the default option from the daily menu by exact name match against active `MealOption` records; if no match exists, use the first active option ordered by `order`.

### Rationale

This reuses the current data model, preserves the admin-managed option list, and keeps the behavior predictable without adding a new foreign key to `DailyMenu`.

### Alternatives considered

- Adding a `default_meal_option` foreign key to `DailyMenu`: rejected as unnecessary schema expansion for this feature.
- Always hardcoding the first option as default: rejected because it would ignore the daily menu content.

---

## 3. Rating model shape

### Context

Users can rate only past meals that were actually reserved, and they can update the rating later.

### Decision

Store one `MealRating` record per confirmed `Lunch` using a one-to-one relationship, with a 1–5 integer rating and timestamps.

### Rationale

The reservation already uniquely identifies the user/date pair, so tying the rating to `Lunch` preserves integrity and makes updates straightforward.

### Alternatives considered

- Storing `(user, date)` directly on the rating model: rejected because it duplicates reservation identity.
- Allowing multiple rating rows per lunch: rejected because the spec requires one current rating with overwrite behavior.

---

## 4. Admin average calculation

### Context

The admin monthly recap needs averages per day and per-user visibility without creating a separate reporting subsystem.

### Decision

Compute averages on demand from `MealRating` and `Lunch` data when rendering the admin summary.

### Rationale

This keeps the implementation simple, avoids synchronization issues, and is sufficient for the monthly recap view.

### Alternatives considered

- Storing denormalized aggregates: rejected because it adds consistency overhead with no clear benefit at this scale.
- Deferring ratings to a separate analytics service: rejected as unnecessary complexity for the current scope.

