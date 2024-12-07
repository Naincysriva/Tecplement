from flask import Flask, render_template, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '../frontend/templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../frontend/static'))

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            return jsonify({"error": "All fields are required!"}), 400

        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters!"}), 400

        hashed_password = generate_password_hash(password)
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, hashed_password))
            conn.commit()
            conn.close()
            return jsonify({"message": "WELCOME TO THIS PAGE!"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already registered!"}), 400

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            return jsonify({"message": f"Welcome back TO This Page, {user[1]}!"}), 200
        else:
            return jsonify({"error": "Invalid email or password!"}), 400

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


