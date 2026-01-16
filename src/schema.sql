DROP TABLE IF EXISTS lunches;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_admin INTEGER DEFAULT 0
);

CREATE TABLE lunches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  lunch_date TEXT NOT NULL,
  lunch_choice TEXT,
  UNIQUE(username, lunch_date)
);

