from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        connection = self.connect()
        if not connection:
            return None
        cursor = connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                connection.commit()
        except Error as e:
            print(f"Database query error: {e}")
        finally:
            cursor.close()
            connection.close()
        return result

class UserManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def register_user(self, username, password, email):
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        params = (username, hashed_password, email)
        self.db_manager.execute_query(query, params)

    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s"
        user = self.db_manager.execute_query(query, (username,), fetch_one=True)
        if user and check_password_hash(user['password'], password):
            return user
        return None

# Flask App Factory

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'  # Vervang dit door een veilige sleutel

    db_manager = DatabaseManager(
        host='localhost',
        user='your_user',
        password='your_password',
        database='your_database'
    )
    user_manager = UserManager(db_manager)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = user_manager.authenticate_user(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials', 'danger')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            try:
                user_manager.register_user(username, password, email)
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Registration failed: {str(e)}', 'danger')
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged out successfully.', 'info')
        return redirect(url_for('login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


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
