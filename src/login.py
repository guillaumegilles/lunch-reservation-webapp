from flask_login import LoginManager, UserMixin

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, is_admin=0):
        self.id = id
        self.username = username
        self.is_admin = is_admin

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, username, is_admin FROM users WHERE id = ?", (int(user_id)))
    row = c.fetchone()
    if row:
        return User(row[0], row[1], row[2])
    return None
