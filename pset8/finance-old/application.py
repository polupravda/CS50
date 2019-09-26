import os
import sqlite3
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # get data from database
    rows = db.execute("SELECT symbol, name, SUM(share_quantity) as sum_share_quantity, share_price, SUM(total_price)\
            FROM record WHERE user_id=:user_id GROUP BY symbol",\
            user_id=session["user_id"])

    if not rows:
        return apology("You have no shares yet")
    else:
        # get total price of all shares bought
        allSharesPrice = db.execute("SELECT SUM(total_price) FROM record WHERE user_id=:user_id", user_id=session["user_id"])
        cashRaw = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        budget = usd(float(allSharesPrice[0]["SUM(total_price)"]) + float(cashRaw[0]["cash"]))
        cash = usd(float(cashRaw[0]["cash"]))

        # add formatted values to the dictionary
        for row in rows:
            row.update({"sum_total_price" : usd(float(row["SUM(total_price)"]))})
            row["share_price"] = usd(row["share_price"])

        return render_template("index.html", rows=rows, budget=budget, cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)

        if not quote:
            return apology("Stock is invalid", 400)
        elif not shares or not int(shares) > 0:
            return apology("Enter number of shares", 400)

        # check how much cash is available
        currTotalRecord = db.execute("SELECT cash FROM users WHERE id = :id",
                        id=session["user_id"])

        currTotal = currTotalRecord[0]["cash"]

        # calculate the total price of shares
        shareTotal = quote["price"] * int(shares)

        # gather data
        transData = {
            "user_id": session["user_id"],
            "share_symbol": request.form.get("symbol"),
            "name": quote["name"],
            "share_quantity": int(shares),
            "share_price": quote["price"],
            "total_price": shareTotal,
            "date_time": datetime.datetime.now(),
            "cash": currTotal-shareTotal,
            "share_name": quote["name"],
            "share_price_formatted": usd(quote["price"]),
            "total_price_formatted": usd(shareTotal),
            "total_formatted": usd(currTotal-shareTotal)
        }

        # check if the user has enough deposit to make purchase
        if shareTotal > currTotal:
            return apology("You have not enough deposit")
        else:
            # add transaction into record table
            db.execute("INSERT INTO record (user_id, operation, symbol, name, share_quantity, share_price, total_price, date_time)\
                        VALUES(:user_id, :operation, :share_symbol, :name, :share_quantity, :share_price, :total_price, :date_time)",\
                        user_id=transData["user_id"], operation="buy", share_symbol=transData["share_symbol"], name=transData["name"],\
                        share_quantity=transData["share_quantity"], share_price=transData["share_price"],\
                        total_price=transData["total_price"], date_time=transData["date_time"])

            # update cash in user db
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=transData["cash"], id=transData["user_id"])

            # get data from database
            rows = db.execute("SELECT symbol, name, SUM(share_quantity) as sum_share_quantity, share_price, SUM(total_price) FROM record\
                    WHERE user_id=:user_id GROUP BY symbol",\
                    user_id=session["user_id"])

            # get total price of all shares bought
            allSharesPrice = rows[0]["SUM(total_price)"]
            cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
            budget = usd(float(allSharesPrice) + float(cash[0]["cash"]))

            # add formatted values to the dictionary
            for row in rows:
                row.update({"sum_total_price" : usd(float(row["SUM(total_price)"]))})
                row["share_price"] = usd(row["share_price"])

            # update user's portfolio
            return render_template("index.html", rows=rows, budget=budget)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")

    # db.execute("SELECT operation, date_time, ")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Stock is invalid", 400)
        else:
            return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("type password confirmation", 403)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Add user to database
        passHash = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")

        currUser = db.execute("INSERT INTO users (username, hash) VALUES (:username,:passHash)",
                            username=username,passHash=passHash)

        if not currUser:
            return apology("Usename is already taken", 403)
            # return redirect("/register")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Log user in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # return apology("TODO")

    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM record WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

        if not symbols:
            return apology("You have no shares to sell")
        else:
            return render_template("sell.html", symbols=symbols)
    else:
        symbols = db.execute("SELECT symbol FROM record WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

        render_template("sell.html", symbols=symbols)

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)

        if not quote:
            return apology("Stock is invalid", 400)
        elif not shares or not int(shares) > 0:
            return apology("Enter number of shares", 400)

        # update user's portfolio
        return render_template("index.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
