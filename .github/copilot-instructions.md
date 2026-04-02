# Copilot Instructions

## What This App Does

Django web app for office lunch reservations. Employees log in, pick a daily lunch option on a calendar, and staff members view a monthly summary of all reservations.

## Running the App

```bash
# Apply DB migrations (first time or after model changes)
python manage.py migrate

# Create default admin user (admin / password)
python manage.py init_db

# Run dev server (http://127.0.0.1:8000)
python manage.py runserver
```

Production: set `SECRET_KEY` and `DEBUG=False` via environment variables. Database path is `instance/lunch.db` (SQLite).

## Architecture

```
lunch_project/       # Django project package (settings, root URLs, wsgi)
reservations/        # Single Django app with all business logic
  models.py          # Lunch model (ForeignKey to built-in User)
  views.py           # All views: index, login, logout, register, calendar, save_lunch, admin_summary
  urls.py            # URL patterns for the reservations app
  admin.py           # Registers Lunch in Django admin (/django-admin/)
  templates/reservations/   # All HTML templates
  static/reservations/      # style.css
  management/commands/init_db.py  # Creates default admin user
  migrations/        # Django ORM migrations
```

## Database

Django ORM with SQLite. Two relevant tables:

- **`auth_user`** — Django's built-in User model. `is_staff=True` grants admin access (replaces the old `is_admin` flag).
- **`reservations_lunch`** — `user (FK)`, `lunch_date (DateField)`, `lunch_choice (CharField)`. Unique constraint on `(user, lunch_date)`. Use `Lunch.objects.update_or_create(user=..., lunch_date=..., defaults={...})` for upserts.

Promote a user to staff:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='alice').update(is_staff=True)"
```

## Key Conventions

- **Lunch options** are defined as `LUNCH_OPTIONS` list constant in `reservations/views.py`.
- **Admin check** is `request.user.is_staff` in views; `{% if request.user.is_staff %}` in templates.
- **Past date guard** — `save_lunch` rejects dates before today with a 400 JSON error (server-side only).
- **`/save_lunch/`** is a JSON POST endpoint. The JS in `calendar.html` sends `X-CSRFToken` in the request header — required for all non-GET AJAX calls.
- **Flash messages** use Django's `messages` framework (`messages.success/error(request, ...)`). Templates render them with `{% for message in messages %}`.
- **UI and flash messages are in French.**
- **Templates** live in `reservations/templates/reservations/` and must start with `{% load static %}` to use `{% static '...' %}`.
- **Days context** — the calendar view passes `days` as a list of dicts `{day, weekday, lunch}` so templates can access the lunch choice without dict key formatting tricks.

