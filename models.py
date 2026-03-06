import sqlite3

def init_db():
    conn = sqlite3.connect('hostel.db')
    cursor = conn.cursor()
    
    # Users Table (Students, Cleaners, Admins)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT,
        name TEXT,
        block TEXT,
        floor TEXT
    )''')

    # Cleaning Requests Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        cleaner_id INTEGER,
        room_no TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(student_id) REFERENCES users(id),
        FOREIGN KEY(cleaner_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()