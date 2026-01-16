import sqlite3
from calendar import monthrange

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    # Seed default admin user if no users exist
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    if count == 0:
        # Create a default admin user (password: "password")
        c.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("password"), 1),
        )
        db.commit()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def get_user_lunches(username, year, month):
    """Get all lunches for a user in a given month."""
    db = get_db()
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-{monthrange(year, month)[1]}"
    
    rows = db.execute(
        """
        SELECT lunch_date, lunch_choice
        FROM lunches
        WHERE username = ? AND lunch_date BETWEEN ? AND ?
        """,
        (username, start, end),
    ).fetchall()
    
    return {row["lunch_date"]: row["lunch_choice"] for row in rows}


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
