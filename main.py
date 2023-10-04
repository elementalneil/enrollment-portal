from flask import Flask
from flask import request, redirect, render_template, url_for

from db_init import initialize
from faculty_functionality import Faculty

app = Flask(__name__)
app.secret_key = b'F#%JGTs@WjzHGGLSidT6ZVz9'

initialize()

@app.route("/")
def index():
    return render_template('index.html')


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
            return redirect(url_for('index'))
        else:
            error = return_message

    return render_template('login_faculty.html', error = error)