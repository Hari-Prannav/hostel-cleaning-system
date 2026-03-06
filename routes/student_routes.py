@app.route('/student/request', methods=['POST'])
def request_cleaning():
    room_no = request.form.get('room_no')
    block = session.get('block')
    floor = session.get('floor')

    conn = sqlite3.connect('hostel.db')
    cursor = conn.cursor()

    # Find Available Cleaner in the same Block and Floor
    cleaner = cursor.execute('''SELECT id FROM users 
                                WHERE role = 'cleaner' 
                                AND block = ? AND floor = ? 
                                AND id NOT IN (SELECT cleaner_id FROM requests WHERE status = 'Assigned')
                                LIMIT 1''', (block, floor)).fetchone()

    if cleaner:
        cursor.execute('''INSERT INTO requests (student_id, cleaner_id, room_no, status) 
                          VALUES (?, ?, ?, 'Assigned')''', 
                       (session['user_id'], cleaner[0], room_no))
    else:
        cursor.execute('''INSERT INTO requests (student_id, room_no, status) 
                          VALUES (?, ?, 'Pending')''', 
                       (session['user_id'], room_no))
    
    conn.commit()
    conn.close()
    return redirect(url_for('student_dashboard'))