import json
import logging
from calendar import monthrange
from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import OperationalError, ProgrammingError, connection
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.utils.timezone import localdate
from django.views.decorators.http import require_POST

from .db_compat import is_missing_column_error
from .forms import LoginForm, RegisterForm, WeeklyMenuForm, SuggestionForm
from .models import DailyMenu, Lunch, MealOption, MealRating, Suggestion, UserProfile

DEFAULT_DAILY_MENU = "Plat du jour"
DEFAULT_ADVANCE_DAYS = 7

logger = logging.getLogger(__name__)

FRENCH_WEEKDAY_NAMES = {
    0: "Lundi",
    1: "Mardi",
    2: "Mercredi",
    3: "Jeudi",
    4: "Vendredi",
    5: "Samedi",
    6: "Dimanche",
}

FRENCH_MONTH_NAMES = {
    1: "janvier",
    2: "février",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "août",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "décembre",
}

WEEKDAY_MENUS = {
    0: "Lundi: 🥗 Plat du jour",
    1: "Mardi: 🐟 Poisson",
    2: "Mercredi: 🥩 Steak haché",
    3: "Jeudi: 🍳 Œufs brouillés",
    4: "Vendredi: 🍝 Pâtes",
}


def _month_navigation(year, month):
    prev_month = month - 1
    next_month = month + 1
    prev_year, next_year = year, year
    if prev_month == 0:
        prev_month, prev_year = 12, year - 1
    if next_month == 13:
        next_month, next_year = 1, year + 1
    return prev_year, prev_month, next_year, next_month


def _weekday_name_fr(current_date):
    return FRENCH_WEEKDAY_NAMES[current_date.weekday()]


def _month_name_fr(month):
    return FRENCH_MONTH_NAMES[month]


def _full_date_label(current_date):
    return f"{_weekday_name_fr(current_date)} {current_date.day} {_month_name_fr(current_date.month)}"


def _menu_for_date(current_date, db_menus=None):
    if db_menus and current_date.day in db_menus:
        return db_menus[current_date.day]
    return DEFAULT_DAILY_MENU


def _default_meal_option(menu_label, active_options):
    if menu_label and menu_label in active_options:
        return menu_label
    return active_options[0] if active_options else ""


def _calendar_date(year, month, day):
    return date(year, month, day)


def _meal_rating_table_exists():
    return MealRating._meta.db_table in connection.introspection.table_names()


def _active_meal_options():
    try:
        return list(MealOption.objects.filter(is_active=True).values("name", "advance_days"))
    except (OperationalError, ProgrammingError) as error:
        if not is_missing_column_error(error, "advance_days"):
            raise
        logger.warning(
            "MealOption.advance_days column is unavailable; falling back to the default advance delay: %s",
            error,
        )
        return [
            {"name": name, "advance_days": DEFAULT_ADVANCE_DAYS}
            for name in MealOption.objects.filter(is_active=True).values_list("name", flat=True)
        ]


def _active_meal_option_map():
    return {option["name"]: option["advance_days"] for option in _active_meal_options()}


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    users = User.objects.values_list("username", flat=True).order_by("username")
    return render(request, "index.html", {"users": users})


def _normalize_identifier(value):
    return (value or "").strip().upper()


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Veuillez renseigner un identifiant valide et un mot de passe")
            return render(request, "login.html", {"form": form})

        identifier = _normalize_identifier(form.cleaned_data["identifier"])
        password = form.cleaned_data["password"]

        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Connecté en tant que {user.username}")
            return redirect("calendar")

        messages.error(request, "Identifiants invalides")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Identifiant, numéro de badge, nom, prénom et mot de passe requis")
            return render(request, "register.html", {"form": form})

        identifier = _normalize_identifier(form.cleaned_data["identifier"])
        badge_number = form.cleaned_data["badge_number"].strip()
        last_name = form.cleaned_data["last_name"].strip()
        first_name = form.cleaned_data["first_name"].strip()
        password = form.cleaned_data["password"]
        confirm_password = form.cleaned_data["confirm_password"]

        if not badge_number:
            messages.error(request, "Le numéro de badge est requis")
            return render(request, "register.html", {"form": form})

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, "register.html", {"form": form})

        if User.objects.filter(username=identifier).exists():
            messages.error(request, "Cet identifiant existe déjà")
            return render(request, "register.html", {"form": form})

        draft_user = User(username=identifier, first_name=first_name, last_name=last_name)
        try:
            validate_password(password, user=draft_user)
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
            return render(request, "register.html", {"form": form})

        new_user = User.objects.create_user(
            username=identifier,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        UserProfile.objects.create(user=new_user, badge_number=badge_number)
        messages.success(request, "Compte créé. Vous pouvez vous connecter.")
        return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def dashboard_view(request):
    """Landing page after login with general information and navigation."""
    form = SuggestionForm()
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'is_staff': request.user.is_staff,
        'form': form,
    }
    return render(request, "dashboard.html", context)



@login_required
def calendar_view(request):
    today = localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    lunches_qs = Lunch.objects.filter(
        user=request.user,
        lunch_date__year=year,
        lunch_date__month=month,
    ).select_related("user")
    lunches_by_day = {l.lunch_date.day: l for l in lunches_qs}

    db_menus_qs = DailyMenu.objects.filter(date__year=year, date__month=month)
    db_menus_by_day = {m.date.day: m.menu for m in db_menus_qs}
    active_options = _active_meal_options()
    active_option_names = [opt["name"] for opt in active_options]
    min_advance_days = min((opt["advance_days"] for opt in active_options), default=2)
    ratings_enabled = _meal_rating_table_exists()

    ratings_by_lunch_id = (
        {
            rating.lunch_id: rating.rating
            for rating in MealRating.objects.filter(lunch__in=lunches_qs)
        }
        if ratings_enabled
        else {}
    )

    num_days = monthrange(year, month)[1]
    month_name_fr = _month_name_fr(month)
    days = []
    for d in range(1, num_days + 1):
       current_date = date(year, month, d)
       if current_date.weekday() >= 5:
           continue
       lunch = lunches_by_day.get(d)
       menu_label = _menu_for_date(current_date, db_menus_by_day)
       days_until = (current_date - today).days
       days.append(
           {
               "day": d,
               "weekday_label": _weekday_name_fr(current_date),
               "month_name_fr": month_name_fr,
               "full_label": _full_date_label(current_date),
               "menu": menu_label,
               "lunch": lunch.lunch_choice if lunch else "",
               "default_option": _default_meal_option(menu_label, active_option_names),
               "rating": ratings_by_lunch_id.get(lunch.id) if lunch and ratings_enabled else None,
               "days_until": days_until,
               "can_reserve": days_until >= min_advance_days,
               "can_rate": current_date < today and lunch is not None,
           }
       )

    prev_year, prev_month, next_year, next_month = _month_navigation(year, month)
    month_name_fr = _month_name_fr(month)

    return render(
        request,
        "calendar.html",
        {
            "username": request.user.username,
            "year": year,
            "month": month,
            "month_name": month_name_fr,
            "month_name_fr": month_name_fr,
            "days": days,
            "options": active_options,
            "ratings_enabled": ratings_enabled,
            "prev_month": prev_month,
            "next_month": next_month,
            "prev_year": prev_year,
            "next_year": next_year,
        },
    )


@require_POST
@login_required
def save_lunch(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Requête JSON invalide."}, status=400)

    day = int(payload.get("day"))
    month = int(payload.get("month"))
    year = int(payload.get("year"))
    lunch = payload.get("lunch", "")

    lunch_date = _calendar_date(year, month, day)
    if lunch == "":
        Lunch.objects.filter(user=request.user, lunch_date=lunch_date).delete()
        return JsonResponse({"status": "success", "message": "Réservation annulée."})

    options_map = _active_meal_option_map()

    if lunch not in options_map:
        return JsonResponse(
            {
                "status": "error",
                "message": "Option de repas invalide.",
            },
            status=400,
        )

    advance_days = options_map[lunch]
    if lunch_date < localdate() + timedelta(days=advance_days):
        return JsonResponse(
            {
                "status": "error",
                "message": f"Cette option doit être réservée au moins {advance_days} jours à l'avance.",
            },
            status=400,
        )

    Lunch.objects.update_or_create(
        user=request.user,
        lunch_date=lunch_date,
        defaults={"lunch_choice": lunch},
    )

    return JsonResponse({"status": "success", "message": "Déjeuner enregistré."})


@require_POST
@login_required
def save_meal_rating(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Requête JSON invalide."}, status=400)

    try:
        day = int(payload.get("day"))
        month = int(payload.get("month"))
        year = int(payload.get("year"))
        rating = int(payload.get("rating"))
    except (TypeError, ValueError):
        return JsonResponse({"status": "error", "message": "Note invalide."}, status=400)

    if rating < 1 or rating > 5:
        return JsonResponse({"status": "error", "message": "Note invalide."}, status=400)

    if not _meal_rating_table_exists():
        return JsonResponse(
            {"status": "error", "message": "La notation n'est pas encore disponible."},
            status=503,
        )

    rating_date = _calendar_date(year, month, day)
    if rating_date >= localdate():
        return JsonResponse(
            {"status": "error", "message": "La notation est réservée aux repas passés."},
            status=400,
        )

    lunch = Lunch.objects.filter(user=request.user, lunch_date=rating_date).first()
    if lunch is None:
        return JsonResponse(
            {"status": "error", "message": "Aucune réservation trouvée pour cette date."},
            status=400,
        )

    MealRating.objects.update_or_create(
        lunch=lunch,
        defaults={"rating": rating},
    )

    return JsonResponse({"status": "success", "message": "Note enregistrée."})


@login_required
def admin_summary(request):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux personnels du CSE")
        return redirect("calendar")

    today = localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    week_start = today - timedelta(days=today.weekday())
    weekly_form = WeeklyMenuForm(
        initial={
            "week_start": week_start,
            "monday_menu": "🥗 Plat du jour",
            "tuesday_menu": "🐟 Poisson",
            "wednesday_menu": "🥩 Steak haché",
            "thursday_menu": "🍳 Œufs brouillés",
            "friday_menu": "🍝 Pâtes",
        }
    )

    if request.method == "POST":
        weekly_form = WeeklyMenuForm(request.POST)
        if weekly_form.is_valid():
            start = weekly_form.cleaned_data["week_start"]
            if start.weekday() != 0:
                weekly_form.add_error("week_start", "Veuillez choisir un lundi.")
            else:
                day_keys = [
                    "monday_menu",
                    "tuesday_menu",
                    "wednesday_menu",
                    "thursday_menu",
                    "friday_menu",
                ]
                for index, key in enumerate(day_keys):
                    DailyMenu.objects.update_or_create(
                        date=start + timedelta(days=index),
                        defaults={"menu": weekly_form.cleaned_data[key]},
                    )

                messages.success(request, "Menus hebdomadaires enregistrés.")
                summary_year = request.POST.get("summary_year")
                summary_month = request.POST.get("summary_month")
                if summary_year and summary_month:
                    return redirect(f"{reverse('admin_summary')}?year={summary_year}&month={summary_month}")
                return redirect(f"{reverse('admin_summary')}?year={start.year}&month={start.month}")

    rows = list(Lunch.objects.filter(lunch_date__year=year, lunch_date__month=month).select_related("user"))
    ratings_enabled = _meal_rating_table_exists()
    ratings_by_lunch_id = (
        {rating.lunch_id: rating.rating for rating in MealRating.objects.filter(lunch__in=rows)}
        if ratings_enabled
        else {}
    )

    data = {}
    for row in rows:
        data.setdefault(row.user.username, {})[row.lunch_date.day] = row

    users = sorted(data.keys())
    num_days = monthrange(year, month)[1]
    days = [d for d in range(1, num_days + 1) if date(year, month, d).weekday() < 5]

    daily_rating_summary = []
    for day in days:
        day_ratings = [ratings_by_lunch_id[row.id] for row in rows if row.lunch_date.day == day and row.id in ratings_by_lunch_id]
        if day_ratings:
            average_rating = round(sum(day_ratings) / len(day_ratings), 1)
            average_display = f"★ {average_rating} / 5"
        else:
            average_rating = None
            average_display = "Non noté"
        daily_rating_summary.append(
            {
                "day": day,
                "average_rating": average_rating,
                "average_display": average_display,
            }
        )

    table_rows = [
        {
            "username": username,
            "cells": [
                {
                    "choice": user_day.lunch_choice,
                    "rating": ratings_by_lunch_id.get(user_day.id),
                }
                if (user_day := data.get(username, {}).get(day)) is not None
                else {"choice": "-", "rating": None}
                for day in days
            ],
        }
        for username in users
    ]

    prev_year, prev_month, next_year, next_month = _month_navigation(year, month)
    month_name_fr = _month_name_fr(month)

    return render(
        request,
        "admin.html",
        {
            "table_rows": table_rows,
            "days": days,
            "daily_rating_summary": daily_rating_summary,
            "year": year,
            "month": month,
            "month_name": month_name_fr,
            "month_name_fr": month_name_fr,
            "prev_month": prev_month,
            "next_month": next_month,
            "prev_year": prev_year,
            "next_year": next_year,
            "weekly_menu_form": weekly_form,
        },
    )


@require_POST
@login_required
def submit_suggestion(request):
    form = SuggestionForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        Suggestion.objects.create(user=request.user, text=text)
        subject = f"Suggestion de {request.user.username}"
        body = f"Utilisateur : {request.user.get_full_name()} ({request.user.username})\n\n{text}"
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.SUGGESTION_RECIPIENT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Merci pour votre suggestion !")
        except Exception:
            messages.error(request, "Erreur lors de l'envoi de votre suggestion. Veuillez reessayer.")
    else:
        messages.error(request, "Erreur lors de l'envoi de votre suggestion.")
    return redirect('dashboard')
