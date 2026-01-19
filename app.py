from flask import Flask, render_template, request, redirect, session, abort
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps



app = Flask(__name__)
app.secret_key = "secret123"
DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")
            if role and session["role"] != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return wrapper


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = get_db()
        user = con.execute(
            "SELECT id, username, password, role FROM users WHERE username=?",
            (username,)
        ).fetchone()
        con.close()

        valid = False
        if user is not None:
            try:
                valid = check_password_hash(user["password"], password)
            except ValueError:
                valid = False

        if valid:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/dashboard")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)



@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        role = "employee"   # FORCED ROLE

        con = get_db()
        try:
            con.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            con.commit()
            con.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            error = "Username already exists"
            con.close()

    return render_template("register.html", error=error)

@app.route("/create_admin", methods=["GET", "POST"])
@login_required("admin")
def create_admin():
    message = None

    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        con = get_db()
        try:
            con.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')",
                (username, password)
            )
            con.commit()
            message = "Admin created successfully"
        except sqlite3.IntegrityError:
            message = "Username already exists"
        con.close()

    return render_template("create_admin.html", message=message)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if session["role"] == "admin":
        return redirect("/admin_dashboard")
    else:
        return redirect("/employee_dashboard")

    
@app.route("/employee_dashboard")
def employee_dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    # Get leave balance
    user = conn.execute(
        "SELECT leave_balance FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    # Get employee leaves
    leaves = conn.execute(
        "SELECT type, days, status FROM leaves WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template(
        "employee_dashboard.html",
        leave_balance=user["leave_balance"],
        leaves=leaves
    )
@app.route("/admin_dashboard")
def admin_dashboard():
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db()
    leaves = conn.execute("""
        SELECT leaves.id, leaves.type, leaves.days, leaves.status, users.username
        FROM leaves
        JOIN users ON leaves.user_id = users.id
        WHERE leaves.status = 'Pending'
    """).fetchall()
    conn.close()

    return render_template("admin_dashboard.html", leaves=leaves)



@app.route("/apply", methods=["GET", "POST"])
def apply():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO leaves (user_id, type, days, status) VALUES (?, ?, ?, ?)",
            (session["user_id"], request.form["type"], request.form["days"], "Pending")
        )
        conn.commit()
        conn.close()

        return redirect("/employee_dashboard")

    return render_template("apply.html")


@app.route("/manage")
@login_required("admin")
def manage():
    con = get_db()
    leaves = con.execute("""
        SELECT leaves.*, users.username
        FROM leaves
        JOIN users ON users.id = leaves.user_id
    """).fetchall()
    con.close()
    return render_template("manage.html", leaves=leaves)

@app.route("/approve/<int:leave_id>")
def approve_leave(leave_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "UPDATE leaves SET status = 'Approved' WHERE id = ?",
        (leave_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/admin_dashboard")

@app.route("/reject/<int:leave_id>")
def reject_leave(leave_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db()
    conn.execute(
        "UPDATE leaves SET status = 'Rejected' WHERE id = ?",
        (leave_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/admin_dashboard")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/create_first_admin")
def create_first_admin():
    con = get_db()

    admin = con.execute(
        "SELECT id FROM users WHERE role='admin'"
    ).fetchone()

    if admin:
        con.close()
        return "Admin already exists"

    from werkzeug.security import generate_password_hash

    con.execute(
        "INSERT INTO users (username, password, role, leave_balance) VALUES (?, ?, ?, ?)",
        ("admin", generate_password_hash("admin123"), "admin", 20)
    )
    con.commit()
    con.close()

    return "Admin created successfully. Username: admin | Password: admin123"



if __name__ == "__main__":
    app.run()
# username: admin
# password: admin123    

# username_admin:mohammadsadhik
# password_admin:sadhik9090

# username_employee:feroz
# password_employee:feroz9090
