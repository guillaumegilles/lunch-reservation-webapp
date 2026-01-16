from flask_login import LoginManager, UserMixin

from .db import get_db

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = "auth.login"


class User(UserMixin):
    def __init__(self, id, username, is_admin=0):
        self.id = id
        self.username = username
        self.is_admin = is_admin

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    row = db.execute(
        "SELECT id, username, is_admin FROM users WHERE id = ?", (int(user_id),)
    ).fetchone()
    if row:
        return User(row["id"], row["username"], row["is_admin"])
    return None


def init_app(app):
    login_manager.init_app(app)
