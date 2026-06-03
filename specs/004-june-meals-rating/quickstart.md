# Quickstart: Options de repas de juin & notation des repas passés

**Feature**: `004-june-meals-rating`  
**Branch**: `004-june-meals-rating`

---

## What this feature delivers

- June 2026 menus populated automatically with varied meal labels
- Default meal selection prefilled from the menu quotidien when available
- 5-star ratings for past confirmed reservations
- Admin recap with per-day averages and per-user ratings

---

## Files changed

| File | Change |
|------|--------|
| `reservations/management/commands/seed_june_menus.py` | NEW — seed June 2026 menus idempotently |
| `reservations/models.py` | NEW — `MealRating` model |
| `reservations/views.py` | Default meal selection, rating save flow, admin recap aggregation |
| `reservations/templates/calendar.html` | Default option display and 5-star rating widget |
| `reservations/templates/admin.html` | Rating averages and per-user visibility |
| `reservations/static/custom.css` | Star-rating and selection styling |
| `reservations/migrations/` | NEW migration for `MealRating` |

---

## Run it locally

```bash
python3 manage.py migrate
python3 manage.py init_db
python3 manage.py seed_june_menus
python3 manage.py runserver
```

---

## Manual validation

1. Open the calendar for June 2026 and verify each day shows a varied menu label.
2. Open a June day and confirm the default meal is already selected.
3. Create or use a past confirmed reservation, submit a 5-star rating, and reload the calendar to confirm persistence.
4. Open the admin monthly recap and verify the average rating and user-level ratings appear for rated days.

---

## Sample shell check

If you need a past reservation for manual rating tests:

```bash
python3 manage.py shell
```

Create a `Lunch` record for a past date, then submit a rating from the calendar UI.
