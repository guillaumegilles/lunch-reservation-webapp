from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .login import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash(
                "Veuillez renseigner le nom d'utilisateur et le mot de passe", "danger"
            )
            return render_template("login.html")

        db = get_db()
        row = db.execute(
            "SELECT id, username, password_hash, is_admin FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        if row and check_password_hash(row["password_hash"], password):
            user = User(row["id"], row["username"], row["is_admin"])
            login_user(user)
            flash(f"Connecté en tant que {username}", "success")
            return redirect(url_for("views.calendar_view"))
        flash("Identifiants invalides", "danger")
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not password:
            flash("Nom d'utilisateur et mot de passe requis", "danger")
            return render_template("register.html")
        if password != confirm:
            flash("Les mots de passe ne correspondent pas", "danger")
            return render_template("register.html")

        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash("Le nom d'utilisateur existe déjà", "danger")
            return render_template("register.html")

        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
        flash("Compte créé. Vous pouvez vous connecter.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("views.index"))
