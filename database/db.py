import os
import sqlite3

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    sample_expenses = [
        (user_id, 45.50, "Food", "2026-07-02", "Grocery shopping at Walmart"),
        (user_id, 12.00, "Transport", "2026-07-03", "Uber ride to office"),
        (user_id, 89.99, "Bills", "2026-07-05", "Electricity bill"),
        (user_id, 25.00, "Health", "2026-07-09", "Pharmacy - cold medicine"),
        (user_id, 15.00, "Entertainment", "2026-07-12", "Movie tickets"),
        (user_id, 60.00, "Shopping", "2026-07-15", "New running shoes"),
        (user_id, 10.00, "Other", "2026-07-20", "Miscellaneous purchase"),
        (user_id, 32.75, "Food", "2026-07-25", "Dinner at restaurant"),
    ]
    conn.executemany(
        """
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        sample_expenses,
    )
    conn.commit()
    conn.close()
