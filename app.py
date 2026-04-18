from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# simple in-memory storage (no database)
accounts = {}

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Create account
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]

        acc_no = random.randint(100000, 999999)

        accounts[acc_no] = {
            "name": name,
            "balance": 1000
        }

        return f"""
        <h2>Account Created Successfully 🎉</h2>
        <p>Your Account Number: <b>{acc_no}</b></p>
        <a href='/'>Go Home</a>
        """

    return render_template("create.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        acc_no = int(request.form["acc_no"])

        if acc_no in accounts:
            return redirect(url_for("dashboard", acc_no=acc_no))
        else:
            return "Invalid Account ❌"

    return render_template("login.html")

# Dashboard (Deposit / Withdraw)
@app.route("/dashboard/<int:acc_no>", methods=["GET", "POST"])
def dashboard(acc_no):
    user = accounts.get(acc_no)

    if not user:
        return "Account not found ❌"

    if request.method == "POST":
        amount = float(request.form["amount"])
        action = request.form["action"]

        if action == "deposit":
            user["balance"] += amount

        elif action == "withdraw":
            if user["balance"] >= amount:
                user["balance"] -= amount
            else:
                return "Insufficient Balance ❌"

    return render_template("dashboard.html", user=user, acc_no=acc_no)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
