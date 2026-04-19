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
            "balance": 0
        }

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        # ADMIN LOGIN
        if u == ADMIN_USER and p == ADMIN_PASS:
            session["user"] = u
            session["role"] = "admin"
            return redirect("/admin")

        # USER LOGIN
        if u in users and users[u]["password"] == p:
            session["user"] = u
            session["role"] = "user"
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    u = session.get("user")

    if not u or session.get("role") != "user":
        return redirect("/login")

    return render_template("dashboard.html", user=u, data=users[u])

# ---------------- DEPOSIT ----------------
@app.route("/deposit", methods=["POST"])
def deposit():
    u = session.get("user")
    amt = int(request.form["amount"])

    users[u]["balance"] += amt

    transactions.append({
        "type": "deposit",
        "user": u,
        "amount": amt
    })

    return redirect("/dashboard")

# ---------------- WITHDRAW ----------------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    u = session.get("user")
    amt = int(request.form["amount"])

    if users[u]["balance"] >= amt:
        users[u]["balance"] -= amt

        transactions.append({
            "type": "withdraw",
            "user": u,
            "amount": amt
        })
    else:
        return "Insufficient balance"

    return redirect("/dashboard")

# ---------------- TRANSFER ----------------
@app.route("/transfer", methods=["POST"])
def transfer():
    sender = session.get("user")

    if not sender or session.get("role") != "user":
        return redirect("/login")

    receiver = request.form["receiver"]
    amount = int(request.form["amount"])

    if receiver not in users:
        return "Receiver not found"

    if users[sender]["balance"] < amount:
        return "Insufficient balance"

    users[sender]["balance"] -= amount
    users[receiver]["balance"] += amount

    transactions.append({
        "type": "transfer",
        "from": sender,
        "to": receiver,
        "amount": amount
    })

    return redirect("/dashboard")

# ---------------- USER TRANSACTIONS ----------------
@app.route("/transactions")
def user_transactions():
    u = session.get("user")

    if not u or session.get("role") != "user":
        return redirect("/login")

    user_txns = []

    for t in transactions:
        if t.get("user") == u or t.get("from") == u or t.get("to") == u:
            user_txns.append(t)

    return render_template("transactions.html", data=user_txns, user=u)

# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")

    return render_template("admin.html", users=users)

# ---------------- ADMIN TRANSACTIONS ----------------
@app.route("/admin/transactions")
def admin_transactions():
    if session.get("role") != "admin":
        return redirect("/login")

    return render_template("admin_transactions.html", data=transactions)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
