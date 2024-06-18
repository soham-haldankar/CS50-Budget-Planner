import os
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///budget.db")

category_exp = ["Food", "Entertainment", "Clothing", "Electronics", "Gifts", "Groceries", "Health Care", "Transportation"]
category_inco = ["Wage", "Gift", "Investments", "Savings"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if request.method == "POST":
            if not name:
                return render_template("register.html", string="You need to enter a username")
            taken_name = db.execute("SELECT * FROM users")
            for k in taken_name:
                if k["username"] == name:
                    return render_template("register.html", string="The entered username is already in use")
            if not password or not confirmation:
                return render_template("register.html", string="Both password and confirmation are necessary fields")
            if password != confirmation:
                return render_template("register.html", string="Both password and reentered password must be same")
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                name,
                generate_password_hash(password),
            )
            id = db.execute("SELECT * FROM users WHERE username = ?", name)
            session["user_id"] = id[0]["id"]
            for i in category_exp:
                db.execute("INSERT INTO categories (id, category, type) VALUES (?, ?, 'expense')", session["user_id"], i,)
            for j in category_inco:
                db.execute("INSERT INTO categories (id, category, type) VALUES (?, ?, 'income')", session["user_id"], j,)
            return redirect("/")
    if request.method == "GET":
        return render_template("register.html")


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/expense", methods=["GET", "POST"])
@login_required
def income():
    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        note = request.form.get("note")
        db.execute(
            "INSERT INTO info (id, amount, category, date, notes, type) VALUES (?, ?, ?, ?, ?, 'expense')",
            session["user_id"],
            amount,
            category,
            date,
            note,
        )
        return redirect("/history")
    else:
        categories=db.execute("SELECT * FROM categories WHERE id = ? AND type = 'expense'", session["user_id"])
        return render_template("expense.html", categories=categories)

@app.route("/income", methods=["GET", "POST"])
@login_required
def expense():
    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        note = request.form.get("note")
        db.execute(
            "INSERT INTO info (id, amount, category, date, notes, type) VALUES (?, ?, ?, ?, ?, 'income')",
            session["user_id"],
            amount,
            category,
            date,
            note,
        )
        return redirect("/history")
    else:
        categories=db.execute("SELECT * FROM categories WHERE id = ? AND type = 'income'", session["user_id"])
        return render_template("income.html", categories=categories)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    if request.method == "POST":
        info = db.execute("SELECT * FROM info WHERE id = ? ORDER BY date DESC", session["user_id"])
        total = db.execute("SELECT SUM(amount) FROM info WHERE id = ? AND type = 'expense'", session["user_id"])
        total_exp = total[0]["SUM(amount)"]
        total = db.execute("SELECT SUM(amount) FROM info WHERE id = ? AND type = 'income'", session["user_id"])
        total_inco = total[0]["SUM(amount)"]
        month = request.form.get("month")
        month_s = str(month)
        expense = db.execute("SELECT category, amount FROM info WHERE strftime('%m', date) = ? AND type = 'expense' AND id = ?", month_s, session["user_id"],)
        income = db.execute("SELECT category, amount FROM info WHERE strftime('%m', date) = ? AND type = 'income' AND id = ?", month_s, session["user_id"],)

        return render_template("history.html", info=info, total_exp=total_exp, total_inco=total_inco, expense=expense, income=income)
    else:
        info = db.execute("SELECT * FROM info WHERE id = ? ORDER BY date DESC", session["user_id"])
        total = db.execute("SELECT SUM(amount) FROM info WHERE id = ? AND type = 'expense'", session["user_id"])
        total_exp = total[0]["SUM(amount)"]
        total = db.execute("SELECT SUM(amount) FROM info WHERE id = ? AND type = 'income'", session["user_id"])
        total_inco = total[0]["SUM(amount)"]
        expense = []
        income = []
        return render_template("history.html", info=info, total_exp=total_exp, total_inco=total_inco, expense=expense, income=income)

@app.route("/category", methods=["GET", "POST"])
@login_required
def add_cat():
    if request.method == "POST":
        category = request.form.get("category")
        key = request.form.get("key")
        if key == 'expense':
            db.execute("INSERT INTO categories (id, category, type) VALUES (?, ?, 'expense')", session["user_id"], category,)
        else:
            db.execute("INSERT INTO categories (id, category, type) VALUES (?, ?, 'income')", session["user_id"], category,)
        return redirect("/")
    else:
        return render_template("category.html")

