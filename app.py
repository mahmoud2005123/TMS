from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mahmoud'
app.config['MYSQL_DB'] = 'training_mm'

# Initialize MySQL
mysql = MySQL(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('الرجاء تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[5]
            flash(f'مرحباً بك {user[3]}', 'success')
            return redirect(url_for('dashboard'))
        
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    
    # Get statistics
    stats = {}
    
    # Count students
    cur.execute('SELECT COUNT(*) FROM students')
    stats['students'] = cur.fetchone()[0]
    
    # Count organizations
    cur.execute('SELECT COUNT(*) FROM organizations')
    stats['organizations'] = cur.fetchone()[0]
    
    # Count reports
    cur.execute('SELECT COUNT(*) FROM training_reports')
    stats['reports'] = cur.fetchone()[0]
    
    # Count evaluations
    cur.execute('SELECT COUNT(*) FROM evaluations')
    stats['evaluations'] = cur.fetchone()[0]
    
    cur.close()
    return render_template('dashboard.html', stats=stats)

@app.route('/students')
@login_required
def students():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    students = cur.fetchall()
    cur.close()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        program = request.form['program']
        enrollment_year = request.form['enrollment_year']
        cgpa = request.form['cgpa']
        email = request.form['email']
        phone = request.form['phone']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute('''
                INSERT INTO students 
                (student_id, student_name, program, enrollment_year, cgpa, email, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (student_id, student_name, program, enrollment_year, cgpa, email, phone))
            mysql.connection.commit()
            flash('تم إضافة الطالب بنجاح', 'success')
        except Exception as e:
            flash(f'حدث خطأ: {str(e)}', 'error')
        finally:
            cur.close()
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

@app.route('/organizations')
@login_required
def organizations():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM organizations')
    organizations = cur.fetchall()
    cur.close()
    return render_template('organizations.html', organizations=organizations)

@app.route('/reports')
@login_required
def reports():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT r.*, s.student_name, o.organization_name 
        FROM training_reports r
        JOIN students s ON r.student_id = s.student_id
        JOIN organizations o ON r.organization_id = o.organization_id
    ''')
    reports = cur.fetchall()
    cur.close()
    return render_template('reports.html', reports=reports)

@app.route('/profile')
@login_required
def profile():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True) 