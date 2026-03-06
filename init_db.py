import sqlite3

def init_db():
    conn = sqlite3.connect('hostel.db')
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, 
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            name TEXT NOT NULL,
            block TEXT,
            floor TEXT
        )
    ''')

    # Create Requests Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            cleaner_id TEXT,
            room_no TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(student_id) REFERENCES users(id),
            FOREIGN KEY(cleaner_id) REFERENCES users(id)
        )
    ''')

    # --- POPULATE DATA ---
    users = [
        # ADMIN
        ('ADMIN_001', 'admin123', 'admin', 'System Admin', 'All', 'All'),
        
        # STUDENTS (Floor 1 & 2)
        ('24BCE0659', '123', 'student', 'Patrick', 'A', '1'),
        ('24BIS0547', '123', 'student', 'Anjali', 'A', '1'),
        ('22MIS1098', '123', 'student', 'Rahul', 'A', '2'),
        
        # CLEANERS (Assigned to specific floors)
        ('STAFF_065', '123', 'cleaner', 'Bob (Floor 1)', 'A', '1'),
        ('STAFF_043', '123', 'cleaner', 'Suresh (Floor 2)', 'A', '2')
    ]

    cursor.executemany('INSERT OR REPLACE INTO users VALUES (?,?,?,?,?,?)', users)
    
    conn.commit()
    conn.close()
    print("Database initialized with custom IDs!")

if __name__ == "__main__":
    init_db()