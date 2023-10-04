from flask import Flask
from flask import request, redirect, render_template, url_for, session

from db_init import initialize
from faculty_functionality import Faculty
from admin_functionality import Admin
from student_functionality import Student

app = Flask(__name__)
app.secret_key = b'F#%JGTs@WjzHGGLSidT6ZVz9'

initialize()

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login_admin", methods=['GET', 'POST'])
def login_admin():
    admin = Admin()

    error = None
    if request.method == 'POST':
        admin_id = request.form['username']
        password = request.form['password']

        return_message = admin.admin_login(admin_id, password)
        if return_message == 'Successfully Logged In':
            session['id'] = admin_id
            session['user_type'] = 'admin'
            session['username'] = admin.get_details(admin_id)[2]      # 2nd index contains fname
            return redirect(url_for('index'))
        else:
            error = return_message

    return render_template('login_admin.html', error = error)


@app.route("/register_faculty", methods=['GET', 'POST'])
def register_faculty():
    faculty = Faculty()
    department_list = faculty.return_departments()

    error = None
    if request.method == 'POST':
        data = {}
        data['id'] = request.form.get('id')
        data['password'] = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        data['fname'] = request.form.get('first-name')
        data['lname'] = request.form.get('last-name')
        data['email'] = request.form.get('email')
        data['contact'] = request.form.get('contact-number')
        data['department_id'] = request.form.get('department-id')

        if data['password'] != confirm_password:
            error = 'Password does not match Confirm Password'
        else:
            return_message = faculty.register(data)
            if return_message == "Successfully Registered":
                session['id'] = data['id']
                session['user_type'] = 'faculty'
                session['username'] = data['fname']
                return redirect(url_for('index'))
            else:
                error = return_message

    return render_template('register_faculty.html', department_list = department_list, error = error)


@app.route("/login_faculty", methods=['GET', 'POST'])
def login_faculty():
    faculty = Faculty()

    error = None
    if request.method == 'POST':
        faculty_id = request.form['username']
        password = request.form['password']

        return_message = faculty.faculty_login(faculty_id, password)
        if return_message == 'Successfully Logged In':
            session['id'] = faculty_id
            session['user_type'] = 'faculty'
            session['username'] = faculty.get_details(faculty_id)[2]      # 2nd index contains fname
            return redirect(url_for('index'))
        else:
            error = return_message

    return render_template('login_faculty.html', error = error)


@app.route("/register_student", methods=['GET', 'POST'])
def register_student():
    student = Student()
    department_list = student.return_departments()

    error = None
    if request.method == 'POST':
        data = {}
        data['id'] = request.form.get('id')
        data['password'] = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        data['fname'] = request.form.get('first-name')
        data['lname'] = request.form.get('last-name')
        data['email'] = request.form.get('email')
        data['contact'] = request.form.get('contact-number')
        data['batch'] = request.form.get('batch')
        data['department_id'] = request.form.get('department-id')

        if data['password'] != confirm_password:
            error = 'Password does not match Confirm Password'
        else:
            return_message = student.register(data)
            if return_message == "Successfully Registered":
                session['id'] = data['id']
                session['user_type'] = 'student'
                session['username'] = data['fname']
                return redirect(url_for('index'))
            else:
                error = return_message

    return render_template('register_student.html', department_list = department_list, error = error)


@app.route("/login_student", methods=['GET', 'POST'])
def login_student():
    student = Student()

    error = None
    if request.method == 'POST':
        student_id = request.form['username']
        password = request.form['password']

        return_message = student.student_login(student_id, password)
        if return_message == 'Successfully Logged In':
            session['id'] = student_id
            session['user_type'] = 'student'
            session['username'] = student.get_details(student_id)[2]      # 2nd index contains fname
            return redirect(url_for('index'))
        else:
            error = return_message

    return render_template('login_student.html', error = error)


@app.route("/logout")
def logout():
    session.pop('id')
    return redirect(url_for('index'))