from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "geheime_sleutel"

# MySQL database configuration
MYSQL_HOST = 'localhost'  # change this to your MySQL host
MYSQL_USER = 'root'       # change this to your MySQL user
MYSQL_PASSWORD = ''       # change this to your MySQL password
MYSQL_DATABASE = 'your_database_name'  # change this to your MySQL database name

USE_DATABASE = True  # Set to True to use MySQL, or False to use in-memory temp_users

# In-memory temporary user storage (for testing)
temp_users = {}

# Function to get MySQL connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    return conn

# Initialize the database (create the table if it doesn't exist)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            bike_km_per_day INT DEFAULT 0,
            is_admin INT DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

if USE_DATABASE:
    init_db()

@app.route("/")
def home():
    return render_template("Index.html")

@app.route("/register.html", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        address = request.form["address"]

        if USE_DATABASE:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return "Gebruiker bestaat al."
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, password, email, address) VALUES (%s, %s, %s, %s)",
                           (username, hashed_password, email, address))
            conn.commit()
            conn.close()
        else:
            if username in temp_users:
                return "Gebruiker bestaat al."
            hashed_password = generate_password_hash(password)
            temp_users[username] = {
                "password": hashed_password,
                "email": email,
                "address": address,
                "bike_km_per_day": 0,
                "is_admin": False
            }

        return redirect(url_for("login_page"))

    return render_template("Register.html")

@app.route("/login.html", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if USE_DATABASE:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()
            if user and check_password_hash(user["password"], password):
                session["username"] = user["username"]
                session["is_admin"] = bool(user["is_admin"])
                return redirect(url_for("home"))
            else:
                return "Onjuiste gebruikersnaam of wachtwoord."
        else:
            user = temp_users.get(username)
            if user and check_password_hash(user["password"], password):
                session["username"] = username
                session["is_admin"] = user["is_admin"]
                return redirect(url_for("home"))
            else:
                return "Onjuiste gebruikersnaam of wachtwoord."

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/admin.html")
def admin_page():
    if not session.get("is_admin"):
        return "Toegang geweigerd."
    return render_template("admin.html")

@app.route("/admin_instellingen.html")
def admin_page():
    if not session.get("is_admin"):
        return "Toegang geweigerd."
    return render_template("admin_instellingen.html")

if __name__ == "__main__":
    app.run(debug=True)
