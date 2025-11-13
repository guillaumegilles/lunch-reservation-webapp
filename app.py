from flask import Flask, render_template, request, jsonify, redirect, url_for
from calendar import monthrange, month_name
from datetime import date
import sqlite3

app = Flask(__name__)

USERS = ["Alice", "Bob", "Charlie", "Diana"]
LUNCH_OPTIONS = [
    "🥗 Plat du jour",
    "🐟 Poisson",
    "🥩 Steak haché",
    "🍳 Œufs brouillés",
]

DB_FILE = "lunch.db"


# --- Initialize SQLite Database ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS lunches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            lunch_date TEXT NOT NULL,
            lunch_choice TEXT,
            UNIQUE(username, lunch_date)
        )
    """)
    conn.commit()
    conn.close()


init_db()


def get_user_lunches(username, year, month):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-{monthrange(year, month)[1]}"
    c.execute(
        """
        SELECT lunch_date, lunch_choice
        FROM lunches
        WHERE username = ? AND lunch_date BETWEEN ? AND ?
    """,
        (username, start, end),
    )
    data = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return data


@app.route("/")
def index():
    return render_template("index.html", users=USERS)


@app.route("/calendar", methods=["POST", "GET"])
def calendar_view():
    # Support both POST (from form) and GET (for month navigation)
    username = request.values.get("username")
    if not username:
        return redirect(url_for("index"))

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


@app.route("/save_lunch", methods=["POST"])
def save_lunch():
    data = request.json
    username = data.get("username")
    day = int(data.get("day"))
    lunch = data.get("lunch")
    year = int(data.get("year"))
    month = int(data.get("month"))

    lunch_date = date(year, month, day).isoformat()

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # INSERT OR REPLACE ensures the lunch_choice is saved/updated
    c.execute(
        """
        INSERT OR REPLACE INTO lunches (id, username, lunch_date, lunch_choice)
        VALUES (
            COALESCE((SELECT id FROM lunches WHERE username=? AND lunch_date=?), NULL),
            ?, ?, ?
        )
    """,
        (username, lunch_date, username, lunch_date, lunch),
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Saved {lunch} for {lunch_date}"})


@app.route("/admin")
def admin_summary():
    year = int(request.args.get("year", date.today().year))
    month = int(request.args.get("month", date.today().month))

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        SELECT username, lunch_date, lunch_choice
        FROM lunches
        WHERE strftime('%Y', lunch_date) = ? AND strftime('%m', lunch_date) = ?
        ORDER BY username, lunch_date
    """,
        (str(year), f"{month:02d}"),
    )
    rows = c.fetchall()
    conn.close()

    # Build a mapping: { username: { day: lunch_choice } }
    data = {user: {} for user in USERS}
    for username, lunch_date, lunch_choice in rows:
        day = int(lunch_date.split("-")[2])
        data.setdefault(username, {})[day] = lunch_choice

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
        users=USERS,
        data=data,
        days=days,
        year=year,
        month=month,
        month_name=month_name[month],
        prev_month=prev_month,
        next_month=next_month,
        prev_year=prev_year,
        next_year=next_year,
    )


if __name__ == "__main__":
    app.run(debug=True)
