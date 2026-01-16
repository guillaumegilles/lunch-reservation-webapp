from calendar import month_name, monthrange
from datetime import date

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .db import get_db, get_user_lunches

bp = Blueprint("views", __name__)

LUNCH_OPTIONS = [
    "🥗 Plat du jour",
    "🐟 Poisson",
    "🥩 Steak haché",
    "🍳 Œufs brouillés",
]


@bp.route("/")
def index():
    # If already logged in, redirect to calendar
    if current_user.is_authenticated:
        return redirect(url_for("views.calendar_view"))
    
    # Get list of all users for display
    db = get_db()
    users = [row["username"] for row in db.execute("SELECT username FROM users").fetchall()]
    return render_template("index.html", users=users)


@bp.route("/calendar", methods=["POST", "GET"])
@login_required
def calendar_view():
    # Show calendar for the logged-in user (ignore arbitrary username posts)
    username = current_user.username

    # Determine which month to show
    today = date.today()
    year = int(request.args.get("year", today.year))
    month = int(request.args.get("month", today.month))

    num_days = monthrange(year, month)[1]
    days = [
        {"day": d, "weekday": date(year, month, d).strftime("%a")}
        for d in range(1, num_days + 1)
    ]

    lunches = get_user_lunches(username, year, month)

    # Compute previous and next month for navigation
    prev_month = month - 1
    next_month = month + 1
    prev_year, next_year = year, year
    if prev_month == 0:
        prev_month, prev_year = 12, year - 1
    if next_month == 13:
        next_month, next_year = 1, year + 1

    return render_template(
        "calendar.html",
        username=username,
        year=year,
        month=month,
        month_name=month_name[month],
        days=days,
        options=LUNCH_OPTIONS,
        lunches=lunches,
        prev_month=prev_month,
        next_month=next_month,
        prev_year=prev_year,
        next_year=next_year,
    )


@bp.route("/save_lunch", methods=["POST"])
@login_required
def save_lunch():
    data = request.json
    username = current_user.username

    day = int(data.get("day"))
    month = int(data.get("month"))
    year = int(data.get("year"))
    lunch = data.get("lunch")

    lunch_date = date(year, month, day)
    today = date.today()

    # Block past dates
    if lunch_date < today:
        return jsonify(
            {"status": "error", "message": "Impossible de modifier un déjeuner passé."}
        ), 400

    db = get_db()
    db.execute(
        """
        INSERT OR REPLACE INTO lunches (id, username, lunch_date, lunch_choice)
        VALUES (
            COALESCE((SELECT id FROM lunches WHERE username=? AND lunch_date=?), NULL),
            ?, ?, ?
        )
        """,
        (username, lunch_date.isoformat(), username, lunch_date.isoformat(), lunch),
    )
    db.commit()

    return jsonify({"status": "success"})


@bp.route("/admin")
@login_required
def admin_summary():
    if not current_user.is_admin:
        flash("Accés réservé aux personnels du CSE")
        return redirect(url_for("views.calendar_view"))
    
    year = int(request.args.get("year", date.today().year))
    month = int(request.args.get("month", date.today().month))

    db = get_db()
    rows = db.execute(
        """
        SELECT username, lunch_date, lunch_choice
        FROM lunches
        WHERE strftime('%Y', lunch_date) = ? AND strftime('%m', lunch_date) = ?
        ORDER BY username, lunch_date
        """,
        (str(year), f"{month:02d}"),
    ).fetchall()

    # Build a mapping: { username: { day: lunch_choice } }
    data = {}
    for row in rows:
        username = row["username"]
        lunch_date = row["lunch_date"]
        lunch_choice = row["lunch_choice"]
        day = int(lunch_date.split("-")[2])
        data.setdefault(username, {})[day] = lunch_choice

    # Get list of all users
    users = list(data.keys())

    num_days = monthrange(year, month)[1]
    days = list(range(1, num_days + 1))

    # Compute navigation
    prev_month, next_month = month - 1, month + 1
    prev_year, next_year = year, year
    if prev_month == 0:
        prev_month, prev_year = 12, year - 1
    if next_month == 13:
        next_month, next_year = 1, year + 1

    return render_template(
        "admin.html",
        data=data,
        users=users,
        days=days,
        year=year,
        month=month,
        month_name=month_name[month],
        prev_month=prev_month,
        next_month=next_month,
        prev_year=prev_year,
        next_year=next_year,
    )
