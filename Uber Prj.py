from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "ride_booking_secret_key"


# -------------------------
# DATABASE
# -------------------------

def get_db():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS rides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rider_id INTEGER NOT NULL,
            driver_id INTEGER,
            pickup TEXT NOT NULL,
            destination TEXT NOT NULL,
            distance REAL NOT NULL,
            fare REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    db.commit()
    db.close()


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# REGISTER
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        db = get_db()

        try:
            db.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, password, role)
            )

            db.commit()

        except sqlite3.IntegrityError:
            db.close()
            return "Email already registered."

        db.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()

        user = db.execute(
            """
            SELECT * FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        db.close()

        if user:

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "driver":
                return redirect(url_for("driver_dashboard"))

            return redirect(url_for("rider_dashboard"))

        return "Invalid email or password."

    return render_template("login.html")


# -------------------------
# RIDER DASHBOARD
# -------------------------

@app.route("/rider")
def rider_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    rides = db.execute(
        """
        SELECT rides.*, users.name AS driver_name
        FROM rides
        LEFT JOIN users
        ON rides.driver_id = users.id
        WHERE rides.rider_id = ?
        ORDER BY rides.id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template(
        "rider.html",
        rides=rides,
        name=session["name"]
    )


# -------------------------
# REQUEST RIDE
# -------------------------

@app.route("/request_ride", methods=["POST"])
def request_ride():

    if "user_id" not in session:
        return redirect(url_for("login"))

    pickup = request.form["pickup"]
    destination = request.form["destination"]

    # Temporary distance calculation.
    # Later we'll replace this with Google Maps.
    distance = random.uniform(2, 20)

    # Simple fare calculation
    base_fare = 1000
    price_per_km = 300

    fare = base_fare + (distance * price_per_km)

    db = get_db()

    db.execute(
        """
        INSERT INTO rides
        (rider_id, pickup, destination, distance, fare, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session["user_id"],
            pickup,
            destination,
            round(distance, 2),
            round(fare, 2),
            "Requested"
        )
    )

    db.commit()
    db.close()

    return redirect(url_for("rider_dashboard"))


# -------------------------
# DRIVER DASHBOARD
# -------------------------

@app.route("/driver")
def driver_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    rides = db.execute(
        """
        SELECT rides.*, users.name AS rider_name
        FROM rides
        JOIN users
        ON rides.rider_id = users.id
        WHERE rides.status = 'Requested'
        ORDER BY rides.id DESC
        """
    ).fetchall()

    my_rides = db.execute(
        """
        SELECT rides.*, users.name AS rider_name
        FROM rides
        JOIN users
        ON rides.rider_id = users.id
        WHERE rides.driver_id = ?
        ORDER BY rides.id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    db.close()

    return render_template(
        "driver.html",
        rides=rides,
        my_rides=my_rides,
        name=session["name"]
    )


# -------------------------
# ACCEPT RIDE
# -------------------------

@app.route("/accept/<int:ride_id>")
def accept_ride(ride_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    db.execute(
        """
        UPDATE rides
        SET driver_id = ?,
            status = 'Driver Accepted'
        WHERE id = ?
        AND status = 'Requested'
        """,
        (session["user_id"], ride_id)
    )

    db.commit()
    db.close()

    return redirect(url_for("driver_dashboard"))


# -------------------------
# START RIDE
# -------------------------

@app.route("/start/<int:ride_id>")
def start_ride(ride_id):

    db = get_db()

    db.execute(
        """
        UPDATE rides
        SET status = 'Ride Started'
        WHERE id = ?
        """,
        (ride_id,)
    )

    db.commit()
    db.close()

    return redirect(url_for("driver_dashboard"))


# -------------------------
# COMPLETE RIDE
# -------------------------

@app.route("/complete/<int:ride_id>")
def complete_ride(ride_id):

    db = get_db()

    db.execute(
        """
        UPDATE rides
        SET status = 'Completed'
        WHERE id = ?
        """,
        (ride_id,)
    )

    db.commit()
    db.close()

    return redirect(url_for("driver_dashboard"))


# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# -------------------------
# START APPLICATION
# -------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    <!DOCTYPE html>
<html>

<head>
    <title>RideGo</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>

    <nav>
        <h2>🚗 RideGo</h2>

        <div>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
        </div>
    </nav>

    <main class="hero">

        <h1>Your ride, your way.</h1>

        <p>Book a ride quickly and easily.</p>

        <a class="button" href="/register">
            Get Started
        </a>

    </main>

</body>

</html>
<!DOCTYPE html>
<html>

<head>
    <title>Login</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>

<div class="container">

    <h1>Login</h1>

    <form method="POST">

        <input
            type="email"
            name="email"
            placeholder="Email"
            required
        >

        <input
            type="password"
            name="password"
            placeholder="Password"
            required
        >

        <button type="submit">
            Login
        </button>

    </form>

    <p>
        Don't have an account?
        <a href="/register">Register</a>
    </p>

</div>

</body>

</html>
<!DOCTYPE html>
<html>

<head>
    <title>Rider Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>

<nav>

    <h2>🚗 RideGo</h2>

    <div>
        <span>Hello, {{ name }}</span>
        <a href="/logout">Logout</a>
    </div>

</nav>


<div class="dashboard">

    <h1>Book a Ride</h1>

    <form
        method="POST"
        action="/request_ride"
    >

        <input
            type="text"
            name="pickup"
            placeholder="Pickup location"
            required
        >

        <input
            type="text"
            name="destination"
            placeholder="Where are you going?"
            required
        >

        <button type="submit">
            🚕 Request Ride
        </button>

    </form>


    <h2>Your Rides</h2>

    {% for ride in rides %}

    <div class="ride-card">

        <h3>
            Ride #{{ ride["id"] }}
        </h3>

        <p>
            📍 {{ ride["pickup"] }}
        </p>

        <p>
            🏁 {{ ride["destination"] }}
        </p>

        <p>
            Distance:
            {{ ride["distance"] }} km
        </p>

        <p>
            Fare:
            ₦{{ "%.2f"|format(ride["fare"]) }}
        </p>

        <strong>
            Status: {{ ride["status"] }}
        </strong>

        {% if ride["driver_name"] %}

        <p>
            Driver:
            {{ ride["driver_name"] }}
        </p>

        {% endif %}

    </div>

    {% else %}

    <p>You haven't requested any rides yet.</p>

    {% endfor %}

</div>

</body>

</html>
<!DOCTYPE html>
<html>

<head>
    <title>Driver Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
</head>

<body>

<nav>

    <h2>🚗 RideGo Driver</h2>

    <div>
        <span>Hello, {{ name }}</span>
        <a href="/logout">Logout</a>
    </div>

</nav>


<div class="dashboard">

    <h1>Available Ride Requests</h1>

    {% for ride in rides %}

    <div class="ride-card">

        <h3>
            Ride #{{ ride["id"] }}
        </h3>

        <p>
            Rider:
            {{ ride["rider_name"] }}
        </p>

        <p>
            📍 Pickup:
            {{ ride["pickup"] }}
        </p>

        <p>
            🏁 Destination:
            {{ ride["destination"] }}
        </p>

        <p>
            Distance:
            {{ ride["distance"] }} km
        </p>

        <p>
            Fare:
            ₦{{ "%.2f"|format(ride["fare"]) }}
        </p>

        <a
            class="button"
            href="/accept/{{ ride['id'] }}"
        >
            Accept Ride
        </a>

    </div>

    {% else %}

    <p>
        No ride requests available.
    </p>

    {% endfor %}


    <h1>My Rides</h1>

    {% for ride in my_rides %}

    <div class="ride-card">

        <h3>
            Ride #{{ ride["id"] }}
        </h3>

        <p>
            Rider: {{ ride["rider_name"] }}
        </p>

        <p>
            {{ ride["pickup"] }}
            →
            {{ ride["destination"] }}
        </p>

        <p>
            Fare:
            ₦{{ "%.2f"|format(ride["fare"]) }}
        </p>

        <strong>
            {{ ride["status"] }}
        </strong>

        {% if ride["status"] == "Driver Accepted" %}

        <br><br>

        <a
            class="button"
            href="/start/{{ ride['id'] }}"
        >
            Start Ride
        </a>

        {% elif ride["status"] == "Ride Started" %}

        <br><br>

        <a
            class="button"
            href="/complete/{{ ride['id'] }}"
        >
            Complete Ride
        </a>

        {% endif %}

    </div>

    {% endfor %}

</div>

</body>

</html>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    color: #222;
}

nav {
    background: #111;
    color: white;
    padding: 20px 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
}

.hero {
    text-align: center;
    padding: 120px 20px;
}

.hero h1 {
    font-size: 50px;
}

.hero p {
    font-size: 20px;
}

.button,
button {
    display: inline-block;
    background: #111;
    color: white;
    padding: 12px 25px;
    border: none;
    border-radius: 6px;
    text-decoration: none;
    cursor: pointer;
}

.container {
    width: 400px;
    max-width: 90%;
    margin: 80px auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

input,
select {
    padding: 14px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 16px;
}

.dashboard {
    width: 900px;
    max-width: 90%;
    margin: 40px auto;
}

.ride-card {
    background: white;
    padding: 20px;
    margin: 20px 0;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}