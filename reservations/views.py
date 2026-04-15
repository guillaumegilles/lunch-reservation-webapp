import json
from calendar import month_name, monthrange
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, WeeklyMenuForm
from .models import DailyMenu, Lunch

LUNCH_OPTIONS = [
    "🥗 Plat du jour",
    "🐟 Poisson",
    "🥩 Steak haché",
    "🍳 Œufs brouillés",
]

WEEKDAY_MENUS = {
    0: "Lundi: 🥗 Plat du jour",
    1: "Mardi: 🐟 Poisson",
    2: "Mercredi: 🥩 Steak haché",
    3: "Jeudi: 🍳 Œufs brouillés",
    4: "Vendredi: 🍝 Pates",
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


def _menu_for_date(current_date, db_menus=None):
    if db_menus and current_date.day in db_menus:
        return db_menus[current_date.day]
    return WEEKDAY_MENUS[current_date.weekday()]


def index(request):
    if request.user.is_authenticated:
        return redirect("calendar")

    users = User.objects.values_list("username", flat=True).order_by("username")
    return render(request, "index.html", {"users": users})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Veuillez renseigner le nom d'utilisateur et le mot de passe")
            return render(request, "login.html", {"form": form})

        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            messages.success(request, f"Connecte en tant que {user.username}")
            return redirect("calendar")
        messages.error(request, "Identifiants invalides")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Nom d'utilisateur et mot de passe requis")
            return render(request, "register.html", {"form": form})

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        confirm = form.cleaned_data["confirm"]

        if password != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, "register.html", {"form": form})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilisateur existe deja")
            return render(request, "register.html", {"form": form})

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Compte cree. Vous pouvez vous connecter.")
        return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def calendar_view(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    lunches_qs = Lunch.objects.filter(
        user=request.user,
        lunch_date__year=year,
        lunch_date__month=month,
    )
    lunches_by_day = {l.lunch_date.day: l.lunch_choice for l in lunches_qs}

    db_menus_qs = DailyMenu.objects.filter(date__year=year, date__month=month)
    db_menus_by_day = {m.date.day: m.menu for m in db_menus_qs}

    num_days = monthrange(year, month)[1]
    days = []
    for d in range(1, num_days + 1):
        current_date = date(year, month, d)
        if current_date.weekday() >= 5:
            continue
        days.append(
            {
                "day": d,
                "weekday": current_date.strftime("%a"),
                "menu": _menu_for_date(current_date, db_menus_by_day),
                "lunch": lunches_by_day.get(d, ""),
            }
        )

    prev_year, prev_month, next_year, next_month = _month_navigation(year, month)

    return render(
        request,
        "calendar.html",
        {
            "username": request.user.username,
            "year": year,
            "month": month,
            "month_name": month_name[month],
            "days": days,
            "options": LUNCH_OPTIONS,
            "prev_month": prev_month,
            "next_month": next_month,
            "prev_year": prev_year,
            "next_year": next_year,
        },
    )


@require_POST
@login_required
def save_lunch(request):
    payload = json.loads(request.body.decode("utf-8"))

    day = int(payload.get("day"))
    month = int(payload.get("month"))
    year = int(payload.get("year"))
    lunch = payload.get("lunch", "")

    lunch_date = date(year, month, day)
    if lunch_date < date.today():
        return JsonResponse(
            {"status": "error", "message": "Impossible de modifier un dejeuner passe."},
            status=400,
        )

    Lunch.objects.update_or_create(
        user=request.user,
        lunch_date=lunch_date,
        defaults={"lunch_choice": lunch},
    )

    return JsonResponse({"status": "success", "message": "Dejeuner enregistre."})


@login_required
def admin_summary(request):
    if not request.user.is_staff:
        messages.error(request, "Acces reserve aux personnels du CSE")
        return redirect("calendar")

    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    week_start = today - timedelta(days=today.weekday())
    weekly_form = WeeklyMenuForm(
        initial={
            "week_start": week_start,
            "monday_menu": "🥗 Plat du jour",
            "tuesday_menu": "🐟 Poisson",
            "wednesday_menu": "🥩 Steak haché",
            "thursday_menu": "🍳 Oeufs brouillés",
            "friday_menu": "🍝 Pates",
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

                messages.success(request, "Menus hebdomadaires enregistres.")
                summary_year = request.POST.get("summary_year")
                summary_month = request.POST.get("summary_month")
                if summary_year and summary_month:
                    return redirect(f"{reverse('admin_summary')}?year={summary_year}&month={summary_month}")
                return redirect(f"{reverse('admin_summary')}?year={start.year}&month={start.month}")

    rows = Lunch.objects.filter(lunch_date__year=year, lunch_date__month=month).select_related("user")

    data = {}
    for row in rows:
        data.setdefault(row.user.username, {})[row.lunch_date.day] = row.lunch_choice

    users = sorted(data.keys())
    num_days = monthrange(year, month)[1]
    days = [d for d in range(1, num_days + 1) if date(year, month, d).weekday() < 5]
    table_rows = [
        {
            "username": username,
            "choices": [data.get(username, {}).get(day, "-") for day in days],
        }
        for username in users
    ]

    prev_year, prev_month, next_year, next_month = _month_navigation(year, month)

    return render(
        request,
        "admin.html",
        {
            "table_rows": table_rows,
            "days": days,
            "year": year,
            "month": month,
            "month_name": month_name[month],
            "prev_month": prev_month,
            "next_month": next_month,
            "prev_year": prev_year,
            "next_year": next_year,
            "weekly_menu_form": weekly_form,
        },
    )
