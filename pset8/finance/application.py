import os

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


def balance():
    id = session["user_id"]
    row = db.execute(f"select cash from users where id = {id}")
    return float(row[0]["cash"])


def insert_transaction(typeT, symbol, price, shares, total):
    id = session["user_id"]
    typeT = typeT.upper()
    totalUser = total
    if typeT == 'S':
        shares *= -1
        totalUser *= -1

    db.execute(f"update users set cash = cash - {totalUser} where id = {id} ")
    db.execute("insert into transactions (type, symbol, price, shares, total, user_id) " +
               f"values ('{typeT}', '{symbol}', '{price}', '{shares}', '{total}', '{id}')")


def get_user_stocks():
    id = session["user_id"]
    result = db.execute(
        f"SELECT symbol, sum(shares) as shares FROM transactions WHERE user_id = {id} GROUP BY symbol HAVING sum(shares) > 0")
    return result


def get_stock_shares(symbol):
    id = session["user_id"]
    result = db.execute(
        f"SELECT sum(shares) as shares FROM transactions WHERE user_id = {id} and symbol = '{symbol}' GROUP BY symbol")
    return int(result[0]["shares"])


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_stocks = get_user_stocks()
    total = 0
    for s in user_stocks:
        result = lookup(s["symbol"])
        s["price"] = result["price"]
        s["total"] = s["shares"] * s["price"]
        total += s["total"]

    user_balance = balance()
    total += user_balance
    return render_template("index.html", user={"cash": user_balance, "total": total, "list": user_stocks})


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("symbol required.")
        symbol = symbol.upper()

        shares = request.form.get("shares")
        if not shares:
            return apology("number of shares required.")
        shares = int(shares)

        if shares <= 0:
            return apology("number of shares must be a positivy integer.")

        user_balance = balance()
        stock = lookup(symbol)
        price = float(stock['price'])
        total = price * shares
        if total > user_balance:
            apology("insufficient funds.")

        insert_transaction('B', symbol, price, shares, total)

        return redirect("/history")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    rows = db.execute(f"select * from transactions where user_id = {id} order by date desc")
    return render_template("history.html", list=rows)


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
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        result = lookup(request.form.get("symbol"))
        return render_template("quoted.html", quote=result)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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

        if len(rows) > 0:
            return apology("username already exists", 403)

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        db.execute(f"INSERT INTO users (username, hash) VALUES('{username}', '{hash}')")

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_stocks = get_user_stocks()
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("symbol required.")
        symbol = symbol.upper()

        shares = request.form.get("shares")
        if not shares:
            return apology("number of shares required.")
        shares = int(shares)

        stock_shares = get_stock_shares(symbol)
        if shares > stock_shares:
            return apology("Not enough shares to sell")

        stock = lookup(symbol)
        price = stock["price"]
        total = price * shares
        insert_transaction('S', symbol, price, shares, total)

        return redirect("/history")
    else:
        return render_template("sell.html", stocks=user_stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
