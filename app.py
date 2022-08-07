import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trips.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/booking", methods = ["GET", "POST"])
def booking():
    if request.method == "GET":
        return render_template("booking_form.html")
    if request.method == "POST":
        user_id = session["user_id"]
        offer_id = request.form.get("offer_id")
        hot = db.execute("SELECT * FROM last_minute WHERE offer_id = ?", offer_id)
        name = request.form.get("tourist_name")
        surname = request.form.get("tourist_surname")
        birthday = request.form.get("tourist_birthday")
        passport = request.form.get("tourist_passport")
        booking_ref = 100001
        for offer_id in orders:
            booking_ref += 1
        if not name or not surname or not birthday or not passport:
            return apology("All the fields are required", 400)
        db.execute("INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id, offer_id, booking_ref, hot[0]["country"], hot[0]["hotel"], hot[0]["departure_date"], hot[0]["arrival_date"], hot[0]["price"], name, surname, birthday, passport)
        return redirect("/user-cabinet")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        for char in password:
            if char not in confirmation:
                return apology("Confirm your password", 400)
        if not username or not password or not confirmation:
            return apology("Provide username and password", 400)
        users = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(users) == 1:
            return apology("Sorry, username already exists", 400)
        db.execute("INSERT INTO users VALUES(?, ?, ?)", id(username), username, hash)
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

@app.route("/user-cabinet", methods=["GET", "POST"])
@login_required
def orders():
    orders = db.execute("SELECT * FROM orders WHERE user_id = ?", session["user_id"])
    if not orders:
        return flash("You have no orders")
    return render_template("user-cabinet.html", orders = orders)

@app.route("/online-search")
def online_search():
    return render_template("online-search.html")

@app.route("/last-minute")
def last_minute():
    offers = db.execute("SELECT * FROM last_minute")
    return render_template("last-minute.html", offers = offers)