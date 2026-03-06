from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from auth import login_user, logout_user

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session' # Required for session storage

# --- HELPER FUNCTIONS ---
def get_db_connection():
    conn = sqlite3.connect('hostel.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- ROUTES ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('email') # This will now take 24BCE0659 or STAFF_065
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ? AND password = ?', 
                           (user_id, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            session['block'] = user['block']
            session['floor'] = user['floor']
            
            if user['role'] == 'student': return redirect(url_for('student_dashboard'))
            if user['role'] == 'cleaner': return redirect(url_for('cleaner_dashboard'))
            if user['role'] == 'admin': return redirect(url_for('admin_dashboard'))
        
        flash("Invalid ID or Password", "danger")
    return render_template('login.html')

# --- DASHBOARDS ---

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    # Fetch this specific student's request history
    my_requests = conn.execute('SELECT * FROM requests WHERE student_id = ? ORDER BY id DESC', 
                               (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('student/dashboard.html', my_requests=my_requests)

@app.route('/cleaner/dashboard')
def cleaner_dashboard():
    if 'user_id' not in session or session.get('role') != 'cleaner':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    # Fetch ALL rooms assigned to this specific cleaner that aren't cleaned yet
    tasks = conn.execute('''
        SELECT r.id, r.room_no, r.status, u.name as student_name 
        FROM requests r
        JOIN users u ON r.student_id = u.id
        WHERE r.cleaner_id = ? AND r.status != 'Cleaned'
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('cleaner/dashboard.html', tasks=tasks)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    # Fetch all requests, joining with user names for students and cleaners
    all_requests = conn.execute('''
        SELECT r.id, r.room_no, r.status, 
               s.name as student_name, 
               c.name as cleaner_name
        FROM requests r
        JOIN users s ON r.student_id = s.id
        LEFT JOIN users c ON r.cleaner_id = c.id
        ORDER BY r.id DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/dashboard.html', requests=all_requests)

# --- LOGIC ROUTES ---

@app.route('/student/request', methods=['POST'])
def handle_request():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    room_no = request.form.get('room_no')
    student_id = session.get('user_id')
    block = session.get('block')
    floor = session.get('floor')

    conn = get_db_connection()
    
    # 1. FIND THE CLEANER FOR THIS SPECIFIC FLOOR
    # We look for a cleaner in the same Block and Floor
    cleaner = conn.execute('''
        SELECT id FROM users 
        WHERE role = 'cleaner' AND block = ? AND floor = ? 
        LIMIT 1
    ''', (block, floor)).fetchone()

    # 2. INSERT THE REQUEST
    if cleaner:
        # If a cleaner exists for this floor, assign them immediately
        conn.execute('''
            INSERT INTO requests (student_id, cleaner_id, room_no, status) 
            VALUES (?, ?, ?, 'Assigned')
        ''', (student_id, cleaner['id'], room_no))
        flash(f"Request for Room {room_no} assigned to Floor Cleaner.", "success")
    else:
        # If no cleaner is assigned to this floor yet, set as Pending
        conn.execute('''
            INSERT INTO requests (student_id, room_no, status) 
            VALUES (?, ?, 'Pending')
        ''', (student_id, room_no))
        flash(f"Request for Room {room_no} submitted (Pending cleaner assignment).", "info")

    conn.commit()
    conn.close()
    return redirect(url_for('student_dashboard'))

@app.route('/cleaner/complete/<int:request_id>', methods=['POST'])
def mark_cleaned(request_id):
    conn = sqlite3.connect('hostel.db')
    cursor = conn.cursor()
    
    # Update status to 'Cleaned'
    cursor.execute('UPDATE requests SET status = "Cleaned" WHERE id = ?', (request_id,))
    
    conn.commit()
    conn.close()
    return redirect(url_for('cleaner_dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)