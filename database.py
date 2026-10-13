import os
import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = os.environ.get("DATABASE_PATH", "leave_management.db")

def get_db_connection():
    parent = os.path.dirname(DATABASE)
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)

    if conn.execute(
        "SELECT 1 FROM employees WHERE username = ?", ("employee",)
    ).fetchone() is None:
        conn.execute(
            """
            INSERT INTO employees (username, password, name, email)
            VALUES (?, ?, ?, ?)
            """,
            (
                "employee",
                generate_password_hash("employee123"),
                "Demo Employee",
                "employee@example.com",
            ),
        )

    if conn.execute(
        "SELECT 1 FROM employees WHERE username = ?", ("admin",)
    ).fetchone() is None:
        conn.execute(
            """
            INSERT INTO employees (username, password, name, email)
            VALUES (?, ?, ?, ?)
            """,
            (
                "admin",
                generate_password_hash("admin123"),
                "System Administrator",
                "admin@example.com",
            ),
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
