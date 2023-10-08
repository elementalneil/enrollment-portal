import sqlite3
import bcrypt
import datetime

class Admin:
    def register(self, admin_data):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Admin')

        rows = cursor.fetchall()
        id_values = [row[0] for row in rows]

        if admin_data['id'] in id_values:
            cursor.close()
            connection.close()
            return False
        else:
            password = bytes(admin_data['password'], 'utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cursor.execute('INSERT INTO Admin VALUES (?, ?, ?, ?, ?, ?)', (
                admin_data['id'], hashed_password, admin_data['fname'], 
                admin_data['lname'], admin_data['email'], admin_data['contact']
            ))

            connection.commit()

            cursor.close()
            connection.close()
            return True
        
    def admin_login(self, admin_id, password):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Admin WHERE id = ?', (admin_id, ))
        row = res.fetchone()

        cursor.close()
        connection.close()

        if row != None:
            password = bytes(password, 'utf-8')
            if(bcrypt.checkpw(password, row[1])):
                return 'Successfully Logged In'
            else:
                return 'Incorrect Password'
        else:
            return 'Incorrect Username'
        

    def get_details(self, admin_id):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Admin WHERE id = ?', (admin_id, ))
        row = res.fetchone()

        cursor.close()
        connection.close()

        return row
        

    def create_department(self, dept_data):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        if 'hod_id' in dept_data:
            cursor.execute('INSERT INTO Department VALUES (?, ?, ?)', 
                           (dept_data['did'], dept_data['dname'], dept_data['hod_id']))
        else:
            cursor.execute('INSERT INTO Department(did, dname) VALUES (?, ?)', 
                           (dept_data['did'], dept_data['dname']))
            
        connection.commit()
        cursor.close()
        connection.close()
            

    def return_departments(self):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Department')
        data = res.fetchall()

        cursor.close()
        connection.close()

        return data
    

    def promote_to_hod(self, faculty_id):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT department_id FROM Faculty WHERE id = ?', (faculty_id, ))
        department_id = res.fetchone()[0]

        print(department_id)

        return_val = False
        if faculty_id != None:
            res = cursor.execute('UPDATE Department SET hod_id = ? WHERE did = ?', (faculty_id, department_id))
            return_val = True
            connection.commit()

        cursor.close()
        connection.close()

        return return_val
    

    # elevates a faculty with give faculty_id to hod of the given batch
    def elevate_faculty(self, faculty_id, batch):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT COUNT(*) FROM Faculty WHERE id = ?', (faculty_id, ))
        count = res.fetchone()[0]

        return_str = ""
        if count == 0:
            return_str = "Faculty ID is incorrect"
        else:
            # Check if already FA of some batch
            # Check if FA of that batch already exists
            # If none then insert
            res = cursor.execute('SELECT COUNT(*) FROM FacultyAdvisor WHERE fid = ?', (faculty_id, ))
            count = res.fetchone()[0]
            if count != 0:
                return_str = "Faculty is already an FA"
            else:
                res = cursor.execute('SELECT COUNT(*) FROM FacultyAdvisor WHERE batch = ?', (batch, ))
                count = res.fetchone()[0]
                if count != 0:
                    return_str = "There is already an FA for this batch"
                else:
                    cursor.execute('INSERT INTO FacultyAdvisor VALUES (?, ?)', (faculty_id, batch))
                    connection.commit()
                    return_str = "Faculty Advisor Created Successfully"

        cursor.close()
        connection.close()
        return return_str
    

    def get_batch_years(self):
        current_year = datetime.datetime.now().year

        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT batch FROM FacultyAdvisor')
        rows = res.fetchall()

        cursor.close()
        connection.close()

        all_years = set([year for year in range(current_year - 4, current_year + 1)])
        set_years = set([row[0] for row in rows])

        return list(all_years.difference(set_years))


def post_login(admin_obj):
    if admin_obj is None:
        return
    
    choice = int(input('''Admin Options: 
                       Press 1 to Create Department
                       Press 2 to View Departments
                       Press 3 to Create a Faculty Advisor
                       Press 4 to Exit
                       Enter Choice: '''))
    
    if choice == 1:
        print('\nEnter Details')
        dept_data = {}
        dept_data['did'] = input('Enter Department Id: ')
        dept_data['dname'] = input('Enter Department Name: ')

        admin_obj.create_department(dept_data)

    elif choice == 2:
        data = admin_obj.return_departments()
        print(data)

    elif choice == 3:
        print('\nEnter Details')
        faculty_id = input('Enter Faculty Id: ')
        batch = input('Enter Batch Year: ')

        result = admin_obj.elevate_faculty(faculty_id, batch)
        print(result)

    else:
        print('Aborted by User')
        return

    
def __main__():
    admin_data = {}

    choice1 = input('Press 1 to Register, 2 to Login or anything else to Exit: ')

    if choice1 == '1':
        print('Admin Register')
        admin_data['id'] = input('Enter id: ')
        admin_data['password'] = input('Password: ')
        cnf_pw = input('Confirm Password: ')
        admin_data['fname'] = input('First Name: ')
        admin_data['lname'] = input('Last Name: ')
        admin_data['email'] = input('Email: ')
        admin_data['contact'] = input('Contact Number: ')

        admin = Admin()
        if admin_data['password'] == cnf_pw:
            choice = input('\nConfirm(Y/N): ')
            if choice == 'Y' or choice == 'y':
                if admin.register(admin_data):
                    print('Succesfully Registered')
                    post_login(admin)
                else:
                    print('Admin is Already Registered')
            else:
                print('Aborted by User')
        else:
            print('Password should match Confirm Password')

    elif choice1 == '2':
        print('Admin Login')
        admin_id = input('Admin Id: ')
        password = input('Password: ')

        admin = Admin()
        login_status = admin.admin_login(admin_id, password)
        print(login_status)

        if login_status == "Successfully Logged In":
            post_login(admin)

    else:
        print('Aborted by User')


if __name__ == '__main__':
    __main__()