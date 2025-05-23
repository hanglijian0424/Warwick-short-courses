from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import sqlite3
# Some parts of code are generated by chatgpt
# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session management

# SQLite database file
DB = 'internship.db'

# ------------------------------------------
# DATABASE INITIALIZATION （Chatgpt generated）
# ------------------------------------------
def init_db():
    """
    Initialize SQLite database.
    Creates 'applications' table if it doesn't already exist.
    """
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                statement TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            );
        """)

# ------------------------------------------
# PUBLIC ROUTES
# ------------------------------------------
@app.route('/')
def index():
    """
    Public landing page showing course information and CTA.
    """
    return render_template('index.html')

"""
Student behaviors, apply and check statement
"""
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        course_name = request.form['course_name'].strip()
        statement = request.form['statement'].strip()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #Insert new fields into the database
        with sqlite3.connect(DB) as conn:
            conn.execute("""
                INSERT INTO applications (name, email, course_name, statement, timestamp)
                VALUES (?, ?, ?, ?, ?);
            """, (name, email, course_name, statement, timestamp))
        return redirect('/thankyou')
    return render_template('apply.html')
@app.route('/check', methods=['GET', 'POST'])
def check_status():
    """
    Allow applicant to view their submitted course and status by email.（
    """
    if request.method == 'POST':
        email = request.form['email'].strip()
        with sqlite3.connect(DB) as conn:
            cursor = conn.execute("""
                SELECT name, course_name, statement, timestamp, status
                FROM applications
                WHERE email = ?
                ORDER BY id DESC LIMIT 1;
            """, (email,))
            application = cursor.fetchone()

        if application:
            return render_template('status.html', app=application, email=email)
        else:
            return render_template('status.html', error="No application found for this email.")
    return render_template('check.html')
@app.route('/thankyou')
def thankyou():
    """
    Confirmation page after application is submitted.
    """
    return render_template('thankyou.html')

# ------------------------------------------
# ADMIN LOGIN & SESSION
# ------------------------------------------
@app.route('/login', methods=['GET', 'POST'])#（Chatgpt generated）
def login():
    """
    Admin login page.
    Uses hardcoded credentials: admin / admin
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            return render_template('login.html', error='Invalid login credentials.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logs out the admin and clears session data.
    """
    session.pop('admin', None)
    return redirect('/')

# ------------------------------------------
# ADMIN DASHBOARD
# ------------------------------------------
@app.route('/admin/dashboard')
def dashboard():
    """
    Admin dashboard displaying all applications.
    Requires admin session.
    """
    if not session.get('admin'):
        return redirect('/login')

    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("""
            SELECT id, name, email, statement, timestamp, status
            FROM applications ORDER BY id DESC;
        """)
        applications = cursor.fetchall()

    return render_template('dashboard.html', applications=applications)

@app.route('/admin/view/<int:app_id>')
def view_application(app_id):
    """
    View detailed information of a single application.
    """
    if not session.get('admin'):
        return redirect('/login')

    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("""
            SELECT id, name, email, statement, timestamp, status
            FROM applications WHERE id = ?;
        """, (app_id,))
        app_data = cursor.fetchone()

    if app_data is None:
        return "<p>Application not found.</p>"

    return render_template('view.html', app=app_data)

# ------------------------------------------
# ADMIN ACTIONS
# ------------------------------------------
@app.route('/admin/accept/<int:app_id>')#（Chatgpt generated）
def accept_application(app_id):
    """
    Mark an application as 'accepted' and preview email message.
    """
    if not session.get('admin'):
        return redirect('/login')

    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("SELECT name, email FROM applications WHERE id = ?", (app_id,))
        app_data = cursor.fetchone()

        if app_data:
            name, email = app_data
            conn.execute("UPDATE applications SET status = 'accepted' WHERE id = ?", (app_id,))
        else:
            return redirect('/admin/dashboard')

    message = f"""Dear {name},

We are pleased to inform you that your application for our short course has been accepted.
Please arrive on time and bring a copy of this email for verification.

Best regards,
Warwick Short Courses Team"""

    return render_template('email.html', email=email, message=message)

@app.route('/admin/reject/<int:app_id>')
def reject_application(app_id):
    """
    Mark an application as 'rejected' and preview rejection email.
    """
    if not session.get('admin'):
        return redirect('/login')

    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("SELECT name, email FROM applications WHERE id = ?", (app_id,))
        app_data = cursor.fetchone()

        if app_data:
            name, email = app_data
            conn.execute("UPDATE applications SET status = 'rejected' WHERE id = ?", (app_id,))
        else:
            return redirect('/admin/dashboard')

    message = f"""Dear {name},

Thank you for your application. Unfortunately, we are unable to offer you a place this time.
We encourage you to apply again for future courses.

Best regards,
Warwick Short Courses Team"""

    return render_template('email.html', email=email, message=message)

@app.route('/admin/delete/<int:app_id>')
def delete_application(app_id):
    """
    Permanently delete an application from the database. （Chatgpt generated）
    """
    if not session.get('admin'):
        return redirect('/login')

    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))

    return redirect('/admin/dashboard')

# ------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------
if __name__ == '__main__':
    init_db()  # Initialize database before first request
    app.run(host='0.0.0.0', port=5000, debug=True)

