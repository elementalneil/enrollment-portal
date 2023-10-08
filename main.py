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


##### AUTH PAGES #####

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


##### CORE FUNCTIONALITY #####

@app.route('/admin_dash')
def admin_dash():
    return render_template('admin_dash.html')

options_data = {
    'A': ['Option A1', 'Option A2', 'Option A3'],
    'B': ['Option B1', 'Option B2', 'Option B3'],
    'C': ['Option C1', 'Option C2', 'Option C3']
}

@app.route('/update_hod', methods=['GET', 'POST'])
def update_hod():
    faculty = Faculty()
    admin = Admin()

    departments_data = {}
    departments = faculty.return_departments()

    for department in departments:
        faculty_list = faculty.get_faculty_list(department[0])  # department[0] returns the id for the department
        # The key of the dictionary is the department name and id, the value is the faculty list of that department
        faculty_ids = [(li[0], li[2]+' '+li[3]) for li in faculty_list]
        departments_data[department[1] + '  (' + department[0] + ')'] = faculty_ids    
        
    selected_option = None
    selected_sub_option = None

    message = None
    if request.method == 'POST':
        selected_option = request.form.get('option')
        selected_sub_option = request.form.get('sub_option')
        if selected_sub_option != None:
            res = admin.promote_to_hod(selected_sub_option)        # The faculty id of the selected sub-option
            if res:
                message = "Department Head Updated Successfully"
            else:
                message = "Unable to Update HoD"

    return render_template('update_hod.html', departments_data = departments_data, message = message,
                            selected_option = selected_option, selected_sub_option = selected_sub_option)


@app.route('/elevate_faculty', methods = ['GET', 'POST'])
def elevate_faculty():
    admin = Admin()
    available_years = admin.get_batch_years()

    faculty = Faculty()
    faculty_list = faculty.get_non_fa_faculties()

    message = None
    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        batch_year = request.form['batch']

        message = admin.elevate_faculty(faculty_id, batch_year)

    return render_template('elevate_faculty.html', message = message,
                           years = available_years, faculty_list = faculty_list)