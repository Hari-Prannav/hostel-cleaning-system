import sqlite3
from flask import session, redirect, url_for, flash

def db_connection():
    conn = sqlite3.connect('hostel.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def login_user(email, password):
    conn = db_connection()
    # Check if user exists with the provided email and password
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
                        (email, password)).fetchone()
    conn.close()

    if user:
        # Store user info in the session for persistent login
        session['user_id'] = user['id']
        session['role'] = user['role']
        session['name'] = user['name']
        session['block'] = user['block']
        session['floor'] = user['floor']
        return user['role']
    
    return None

def logout_user():
    session.clear()