from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from database import get_db_connection, init_db
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key-in-production"

REQUEST_COUNT = Counter(
    "flask_request_count",
    "Total number of HTTP requests"
)
REQUEST_LATENCY = Histogram(
    "flask_request_latency_seconds",
    "HTTP request latency in seconds"
)

@app.before_request
def before_request():
    request.start_time = time.perf_counter()

@app.after_request
def after_request(response):
    REQUEST_COUNT.inc()
    start = getattr(request, "start_time", None)
    if start is not None:
        REQUEST_LATENCY.observe(time.perf_counter() - start)
    return response

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM employees WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["name"] = user["name"]
            session["role"] = "admin" if username == "admin" else "employee"

            return redirect(
                url_for("admin_dashboard")
                if session["role"] == "admin"
                else url_for("dashboard")
            )

        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    leaves = conn.execute(
        """
        SELECT * FROM leave_requests
        WHERE employee_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", leaves=leaves)

@app.route("/apply-leave", methods=["GET", "POST"])
def apply_leave():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        leave_type = request.form.get("leave_type", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        reason = request.form.get("reason", "").strip()

        if not all([leave_type, start_date, end_date, reason]):
            flash("Please fill in all fields.", "danger")
            return render_template("apply_leave.html")

        if end_date < start_date:
            flash("End date cannot be before start date.", "danger")
            return render_template("apply_leave.html")

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO leave_requests
            (employee_id, leave_type, start_date, end_date, reason, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"], leave_type, start_date,
                end_date, reason, "Pending"
            )
        )
        conn.commit()
        conn.close()

        flash("Leave request submitted successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("apply_leave.html")

@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    leaves = conn.execute(
        """
        SELECT
            leave_requests.id,
            employees.name,
            employees.email,
            leave_requests.leave_type,
            leave_requests.start_date,
            leave_requests.end_date,
            leave_requests.reason,
            leave_requests.status
        FROM leave_requests
        JOIN employees ON leave_requests.employee_id = employees.id
        ORDER BY leave_requests.id DESC
        """
    ).fetchall()
    conn.close()

    return render_template("admin.html", leaves=leaves)

@app.post("/update-leave/<int:leave_id>/<status>")
def update_leave(leave_id, status):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))
    if status not in {"Approved", "Rejected"}:
        flash("Invalid status.", "danger")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    conn.execute(
        "UPDATE leave_requests SET status = ? WHERE id = ?",
        (status, leave_id)
    )
    conn.commit()
    conn.close()

    flash(f"Leave request {status.lower()} successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
