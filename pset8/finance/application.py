import os
import sqlite3
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from password_strength import PasswordPolicy

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

    # get data for index.html
    rows = db.execute("SELECT symbol, total_share_quantity, cash\
                    FROM dashboard INNER JOIN users ON dashboard.user_id = users.id WHERE user_id = :user_id",
                      user_id=session["user_id"])

    if not rows:
        return apology("You have no shares yet")
    else:
        for row in rows:
            quote_t = lookup(row["symbol"])
            total_all_shares_value = 0
            row.update({'name': quote_t["name"]})
            row.update({'share_price': quote_t["price"]})
            row.update({'total_share_price': quote_t["price"] * row["total_share_quantity"]})
            total_all_shares_value += row["total_share_price"]

        cash = rows[0]["cash"]
        budget = cash + total_all_shares_value

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

        # check if the user has enough deposit to make purchase
        if shareTotal > currTotal:
            return apology("You have not enough deposit")
        else:
            # add transaction into record table
            db.execute("INSERT INTO record (user_id, operation, symbol, name, share_quantity, share_price, total_price,\
                        date_time) VALUES(:user_id, :operation, :share_symbol, :name, :share_quantity, :share_price,\
                        :total_price, :date_time)",
                       user_id=session["user_id"],
                       operation="buy",
                       share_symbol=request.form.get("symbol"),
                       name=quote["name"],
                       share_quantity=int(shares),
                       share_price=quote["price"],
                       total_price=shareTotal,
                       date_time=datetime.datetime.now())

            # update cash in user db
            db.execute("UPDATE users SET cash = cash - :shareTotal WHERE id = :id",
                       shareTotal=shareTotal,
                       id=session["user_id"])

            # try to update dashboard table
            db.execute("UPDATE OR IGNORE dashboard SET total_share_quantity = total_share_quantity + :share_quantity\
                        WHERE user_id=:user_id and symbol=:symbol",
                       symbol=quote["symbol"],
                       share_quantity=int(shares),
                       user_id=session["user_id"])

            # if no update happened (i.e. the row didn't exist) then insert one
            db.execute("INSERT OR IGNORE INTO dashboard (user_id, symbol, total_share_quantity)\
                        VALUES(:user_id, :symbol, :total_share_quantity)",
                       symbol=quote["symbol"],
                       total_share_quantity=int(shares),
                       user_id=session["user_id"])

            # get data for index.html
            rows = db.execute("SELECT symbol, total_share_quantity, cash\
                        FROM dashboard INNER JOIN users ON dashboard.user_id = users.id WHERE user_id = :user_id",
                              user_id=session["user_id"])

            for row in rows:
                quote_t = lookup(row["symbol"])
                total_all_shares_value = 0
                row.update({'name': quote_t["name"]})
                row.update({'share_price': quote_t["price"]})
                row.update({'total_share_price': quote_t["price"] * row["total_share_quantity"]})
                total_all_shares_value += row["total_share_price"]

            cash = rows[0]["cash"]
            budget = cash + total_all_shares_value

            # update user's portfolio
            return render_template("index.html", rows=rows, cash=cash, budget=budget)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    username = request.args.get('username')

    if username and len(username) > 0:
        username_check = db.execute("SELECT username FROM users WHERE username = :username", username=username)

        if username_check:
            return jsonify("false")
        else:
            return jsonify("true")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT operation, symbol, name, share_quantity, share_price, total_price,\
                        date_time FROM record WHERE user_id = :user_id",
                      user_id=session["user_id"])

    return render_template("history.html", rows=rows)


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

        # check password strength
        policy = PasswordPolicy.from_names(
            length=5,  # min length: 8
            uppercase=1,  # need min. 2 uppercase letters
            numbers=1,  # need min. 2 digits
            special=1,  # need min. 2 special characters
        )

        pass_test = policy.test(request.form.get("password"))

        if len(pass_test) != 0:
            return apology("Password must be minimum 5 characters long, must contain at least 1 uppecase letter, "
                           "1 number and 1 special character")

        # Add user to database
        passHash = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")

        currUser = db.execute("INSERT INTO users (username, hash) VALUES (:username,:passHash)",
                              username=username,
                              passHash=passHash)

        if not currUser:
            return render_template("register.html")

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

    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM dashboard WHERE user_id = :user_id",
                             user_id=session["user_id"])

        if not symbols:
            return apology("You have no shares to sell")
        else:
            return render_template("sell.html", symbols=symbols)
    else:
        symbols = db.execute("SELECT symbol FROM dashboard WHERE user_id = :user_id",
                             user_id=session["user_id"])

        render_template("sell.html", symbols=symbols)

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = lookup(symbol)

        if not quote:
            return apology("Stock is invalid", 400)
        elif not shares or not int(shares) > 0:
            return apology("Enter number of shares", 400)

        shares_owned = db.execute("SELECT total_share_quantity FROM dashboard WHERE symbol = :symbol\
                    and user_id = :user_id",
                                  symbol=symbol,
                                  user_id=session["user_id"])

        if shares > shares_owned[0]["total_share_quantity"]:
            return apology("You own not enough shares", 400)

        # store current price
        saved_share_price = quote["price"]

        # add transaction into record table
        db.execute("INSERT INTO record (user_id, operation, symbol, name, share_quantity, share_price, total_price,\
                    date_time) VALUES(:user_id, :operation, :share_symbol, :name, (-1 * :share_quantity), :share_price,\
                    (-1 * :total_price), :date_time)",
                   user_id=session["user_id"],
                   operation="sell",
                   share_symbol=quote["symbol"],
                   name=quote["name"],
                   share_quantity=shares,
                   share_price=saved_share_price,
                   total_price=saved_share_price * shares,
                   date_time=datetime.datetime.now())

        # update cash in user db
        db.execute("UPDATE users SET cash = cash + :total_price WHERE id = :id",
                   total_price=saved_share_price * shares,
                   id=session["user_id"])

        # update dashboard table
        db.execute("UPDATE dashboard SET total_share_quantity = total_share_quantity - :share_quantity\
                    WHERE user_id=:user_id and symbol=:symbol",
                   symbol=quote["symbol"],
                   share_quantity=shares,
                   user_id=session["user_id"])

        # get data for index.html
        rows = db.execute("SELECT symbol, total_share_quantity, cash\
                    FROM dashboard INNER JOIN users ON dashboard.user_id = users.id WHERE user_id = :user_id",
                          user_id=session["user_id"])

        for row in rows:
            quote_t = lookup(row["symbol"])
            total_all_shares_value = 0
            row.update({'name': quote_t["name"]})
            row.update({'share_price': quote_t["price"]})
            row.update({'total_share_price': quote_t["price"] * row["total_share_quantity"]})
            total_all_shares_value += row["total_share_price"]

        cash = rows[0]["cash"]
        budget = cash + total_all_shares_value

        # update user's portfolio
        return render_template("index.html", rows=rows, cash=cash, budget=budget)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change_pass():

    if request.method == "GET":
        return render_template("change_pass.html")
    else:
        if not request.form.get("old_pass"):
            return apology("Must provide your current password", 403)

        elif not request.form.get("new_pass"):
            return apology("Must provide new password", 403)

        elif not request.form.get("new_pass_confirmation"):
            return apology("Type password confirmation", 403)

        elif not request.form.get("new_pass") == request.form.get("new_pass_confirmation"):
            return apology("Passwords do not match", 403)

        elif request.form.get("old_pass") == request.form.get("new_pass"):
            return apology("New password must be different", 403)

        # Query database for hash
        rows = db.execute("SELECT hash FROM users WHERE id = :id",
                          id=session["user_id"])

        # Ensure hash exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old_pass")):
            return apology("You provided invalid password", 403)

        # if password was found
        new_pass_hash = generate_password_hash(request.form.get("new_pass"))

        db.execute("UPDATE users SET hash = :new_pass_hash WHERE id = :id",
                   id=session["user_id"],
                   new_pass_hash=new_pass_hash)

        return apology("Your password was successfully changed!", 200)
