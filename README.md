# 🧹 Hostel Cleaning System

A web application that enables hostel students to raise room cleaning requests online and track their status in real time, streamlining communication between students and cleaning staff.

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Python, Flask 3.1.3                 |
| Auth         | Flask-Login 0.6.3                   |
| Templating   | Jinja2 3.1.6                        |
| Frontend     | HTML, CSS (static assets)           |
| Security     | Werkzeug 3.1.6, itsdangerous 2.2.0  |
| Utilities    | Blinker, Click, Colorama            |

---

## 📁 Project Structure
```
hostel-cleaning-system/
│
├── app.py              # Application entry point; initializes and runs the Flask app
├── auth.py             # Authentication logic (login, logout, session handling)
├── models.py           # Database models (User, CleaningRequest, etc.)
├── init_db.py          # Script to initialize and seed the database
├── requirements.txt    # Python dependencies
├── .gitignore
│
├── routes/             # Route handlers / blueprints (student, staff, admin views)
│
├── templates/          # Jinja2 HTML templates for all pages
│
└── static/             # Static assets (CSS, JS, images)
```
