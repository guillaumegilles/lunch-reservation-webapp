# Quickstart: MVP Lunch Reservation Website

**Phase 1 output** | **Date**: 2026-05-17 | **Plan**: [plan.md](plan.md)

## Prerequisites

- Python 3.12
- Git

---

## Local Development Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd lunch-reservation
python3.12 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment (optional for local)

The app works out of the box with SQLite and a dev secret key. To customise:

```bash
cp .env.local.example .env.local   # if example exists, otherwise skip
# Set any overrides in .env.local or export them directly:
export SECRET_KEY="your-local-secret"
export DEBUG=True
```

### 3. Apply database migrations

```bash
python manage.py migrate
```

### 4. Seed the default admin user and meal options

```bash
python manage.py init_db
# Creates user Z999999 with password "password" and is_staff=True
# Seeds 5 default MealOption records: 🥗 Plat du jour, 🐟 Poisson, 🥩 Steak haché, 🍳 Œufs brouillés, 🍝 Pâtes
```

### 5. Run the development server

```bash
python manage.py runserver
# App available at http://127.0.0.1:8000
```

---

## Key URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Landing page / login redirect |
| `http://127.0.0.1:8000/register/` | New employee registration |
| `http://127.0.0.1:8000/login/` | Login |
| `http://127.0.0.1:8000/dashboard/` | Employee dashboard |
| `http://127.0.0.1:8000/calendar/` | Monthly reservation calendar |
| `http://127.0.0.1:8000/admin-summary/` | CSE staff summary (staff only) |
| `http://127.0.0.1:8000/django-admin/` | Django admin |

---

## Running Tests

```bash
python manage.py test reservations
```

---

## Creating a Staff (CSE) User

Option A — promote an existing user:
```bash
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.filter(username='K589479').update(is_staff=True)
"
```

Option B — use the default seeded admin:
```
Username: Z999999
Password: password
```

---

## Reservation Rules

- **7-day advance booking**: Employees can only make or cancel reservations for dates **at least 7 calendar days in the future**. Days within 7 days are displayed as locked (greyed out) on the calendar and cannot be selected.

---

## Adding Meal Options

Five default meal options are seeded automatically when you run `python manage.py init_db`:
🥗 Plat du jour, 🐟 Poisson, 🥩 Steak haché, 🍳 Œufs brouillés, 🍝 Pâtes.

To add further options, use Django admin at `/django-admin/reservations/mealoption/`:
- Click **Add meal option**
- Enter a name (e.g. "Végétarien"), set `is_active = True`, assign an order
- Save

Options appear immediately in the employee calendar.

---

## Production Deployment (Vercel)

### Required environment variables

| Variable | Example | Notes |
|----------|---------|-------|
| `SECRET_KEY` | `django-insecure-...` | Generate a strong random key |
| `DEBUG` | `False` | Must be `False` in production |
| `DATABASE_URL` | `postgresql://user:pass@host/db` | PostgreSQL connection string |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | |
| `EMAIL_HOST` | `smtp.example.com` | |
| `EMAIL_PORT` | `587` | |
| `EMAIL_USE_TLS` | `True` | |
| `EMAIL_HOST_USER` | `noreply@example.com` | |
| `EMAIL_HOST_PASSWORD` | `secret` | |
| `DEFAULT_FROM_EMAIL` | `noreply@cse-na.fr` | |
| `SUGGESTION_RECIPIENT_EMAIL` | `cse@cse-na.fr` | Suggestion notification target |

### Deploy steps

1. Push code to the connected Git repository
2. Vercel runs the build command automatically:
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```
3. On first deploy, run `init_db` manually via Vercel CLI or a one-time function:
   ```bash
   vercel run python manage.py init_db
   ```

### CSRF trusted origins

`settings.py` already includes:
```python
CSRF_TRUSTED_ORIGINS = [
    "https://*.app.github.dev",
    "https://*.vercel.app",
]
```

Add your custom domain if needed:
```python
CSRF_TRUSTED_ORIGINS = [..., "https://reservations.cse-na.fr"]
```

---

## Project Structure Reference

```
django_project/     # Project settings, root URLs, WSGI
reservations/       # All app logic
  models.py         # MealOption, DailyMenu, Lunch, Suggestion, UserProfile
  views.py          # All views + WEEKDAY_MENUS default constant
  forms.py          # LoginForm, RegisterForm, WeeklyMenuForm, SuggestionForm
  urls.py           # URL patterns
  templates/        # HTML templates
  static/style.css  # Single stylesheet
  management/commands/init_db.py
  migrations/
  tests/
manage.py
requirements.txt
vercel.json
```
