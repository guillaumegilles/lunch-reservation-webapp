import json
from calendar import month_name, monthrange
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm
from .models import Lunch

LUNCH_OPTIONS = [
    "🥗 Plat du jour",
    "🐟 Poisson",
    "🥩 Steak haché",
    "🍳 Œufs brouillés",
]


def _month_navigation(year, month):
    prev_month = month - 1
    next_month = month + 1
    prev_year, next_year = year, year
    if prev_month == 0:
        prev_month, prev_year = 12, year - 1
    if next_month == 13:
        next_month, next_year = 1, year + 1
    return prev_year, prev_month, next_year, next_month


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

    num_days = monthrange(year, month)[1]
    days = [
        {
            "day": d,
            "weekday": date(year, month, d).strftime("%a"),
            "lunch": lunches_by_day.get(d, ""),
        }
        for d in range(1, num_days + 1)
    ]

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

    rows = Lunch.objects.filter(lunch_date__year=year, lunch_date__month=month).select_related("user")

    data = {}
    for row in rows:
        data.setdefault(row.user.username, {})[row.lunch_date.day] = row.lunch_choice

    users = sorted(data.keys())
    num_days = monthrange(year, month)[1]
    days = list(range(1, num_days + 1))
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
        },
    )
