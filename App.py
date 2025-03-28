from flask import Flask, render_template, request, jsonify, session
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "geheime_sleutel"

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL,
                        address TEXT NOT NULL,
                        bike_km_per_day INTEGER DEFAULT 0,
                        is_admin INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@app.route("/register.html", methods=["GET"])
def register_page():
    return render_template("Register.html")

@app.route("/register.html", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    address = data.get("address")
    bike_km_per_day = data.get("bike_km_per_day", 0)

    errors = []
    if not all([username, password, email, address]):
        errors.append("Velden mogen niet leeg zijn.")
    if len(password) < 6 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
        errors.append("Wachtwoord moet minstens 6 tekens, een hoofdletter en een cijfer bevatten.")

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    try:
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email, address, bike_km_per_day) VALUES (?, ?, ?, ?, ?)",
                       (username, hashed_password, email, address, bike_km_per_day))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Registratie succesvol!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "Gebruikersnaam bestaat al."}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        return jsonify({"success": True, "message": "Login succesvol!"})
    return jsonify({"success": False, "error": "Ongeldige gebruikersnaam of wachtwoord."}), 400

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
