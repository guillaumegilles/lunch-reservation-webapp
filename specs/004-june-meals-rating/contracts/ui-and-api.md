# Contracts: June menus & meal ratings

**Feature**: `004-june-meals-rating`

---

## 1. Management command contract

### Command

`python3 manage.py seed_june_menus`

### Expected behavior

- Populates June 2026 working-day menus
- Is safe to run repeatedly
- Does not duplicate existing menu rows
- Uses realistic French menu labels

### Success output

- Reports how many menu rows were created or left unchanged

---

## 2. Calendar selection contract

### Default selection rules

- If the daily menu matches an active meal option by name, that option is preselected.
- If no match exists, the first active meal option by order is preselected.
- If the user already has a reservation, their existing choice remains selected.

### Rating visibility rules

- Show a 5-star widget only for past dates with a confirmed lunch.
- Do not show the widget for today, future dates, or dates without a lunch.

---

## 3. Rating save endpoint contract

### Request

`POST /save-meal-rating/`

```json
{
  "day": 14,
  "month": 6,
  "year": 2026,
  "rating": 5
}
```

### Success response

```json
{
  "status": "success",
  "message": "Note enregistrée."
}
```

### Error cases

- Missing reservation for the requested date
- Date is today or in the future
- Rating outside 1–5
- User is not authenticated

### Error response example

```json
{
  "status": "error",
  "message": "Note invalide."
}
```

---

## 4. Admin recap contract

### Display rules

- Show the average rating per day when at least one rating exists
- Show `Non noté` when no rating exists for a day
- Show user-level ratings for the selected month

