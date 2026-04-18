from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "bank_secret"

# ---------------- DATA ----------------
users = {}
transactions = []

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users:
            return "User already exists"

        users[u] = {
            "password": p,
            "balance": 0,
            "transactions": []
        }

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        # ADMIN
        if u == ADMIN_USER and p == ADMIN_PASS:
            session["user"] = "admin"
            session["role"] = "admin"
            return redirect("/admin")

        # USER
        if u in users and users[u]["password"] == p:
            session["user"] = u
            session["role"] = "user"
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")


# ---------------- USER DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    u = session.get("user")

    if not u or session.get("role") != "user":
        return redirect("/login")

    return render_template("dashboard.html", user=u, data=users[u])


# ---------------- DEPOSIT ----------------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    u = session["user"]
    amt = int(request.form["amount"])

    if users[u]["balance"] >= amt:
        users[u]["balance"] -= amt
        users[u]["transactions"].append(f"Withdraw -{amt}")

    return redirect("/dashboard")
# ---------------- WITHDRAW ----------------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    u = session["user"]
    amt = int(request.form["amount"])

    if users[u]["balance"] >= amt:
        users[u]["balance"] -= amt
        users[u]["transactions"].append(f"Withdraw -{amt}")
        transactions.append(f"{u} withdrew {amt}")
    else:
        return "Insufficient balance"

    return redirect("/dashboard")


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")

    return render_template("admin.html", users=users, transactions=transactions)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
