from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"

# Temporary storage (in-memory)
users = {}

# Home (Login Page)
@app.route("/")
def home():
    return render_template("login.html")

# Create Account
@app.route("/create", methods=["POST"])
def create():
    user = request.form["username"]
    pwd = request.form["password"]

    if user in users:
        return "User already exists!"

    users[user] = {
        "password": pwd,
        "balance": 1000
    }

    return "Account Created Successfully!"

# Login
@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]

    if user in users and users[user]["password"] == pwd:
        session["user"] = user
        return redirect("/dashboard")

    return "Invalid Login"

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    balance = users[user]["balance"]

    return render_template("dashboard.html", user=user, balance=balance)

# Deposit
@app.route("/deposit", methods=["POST"])
def deposit():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    amt = int(request.form["amount"])

    users[user]["balance"] += amt

    return redirect("/dashboard")

# Withdraw
@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    amt = int(request.form["amount"])

    if users[user]["balance"] < amt:
        return "Insufficient Balance!"

    users[user]["balance"] -= amt

    return redirect("/dashboard")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
