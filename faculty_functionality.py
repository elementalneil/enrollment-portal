import sqlite3
import bcrypt

class Faculty:
    def register(self, faculty_data):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id, email FROM Faculty')

        rows = cursor.fetchall()
        id_values = [row[0] for row in rows]
        email_values = [row[1] for row in rows]

        cursor.execute('SELECT did FROM Department')
        rows = cursor.fetchall()
        did_values = [row[0] for row in rows]

        return_message = ""

        if faculty_data['id'] in id_values:
            return_message = "Faculty Already Registered"
        elif faculty_data['email'] in email_values:
            return_message = "Email is Already Registered"
        elif faculty_data['department_id'] not in did_values:
            return_message = "Department does not Exist"
        else:
            password = bytes(faculty_data['password'], 'utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cursor.execute('INSERT INTO Faculty VALUES (?, ?, ?, ?, ?, ?, ?)', (
                faculty_data['id'].lower(), hashed_password, faculty_data['fname'], 
                faculty_data['lname'], faculty_data['email'], faculty_data['contact'],
                faculty_data['department_id']
            ))

            connection.commit()
            return_message = "Successfully Registered"

        cursor.close()
        connection.close()
        return return_message
            
        
    def faculty_login(self, faculty_id, password):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        faculty_id = faculty_id.lower()
        res = cursor.execute('SELECT * FROM Faculty WHERE id = ?', (faculty_id, ))
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
        

    def return_departments(self):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Department')
        data = res.fetchall()

        cursor.close()
        connection.close()

        return data
    

    def get_details(self, faculty_id):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Faculty WHERE id = ?', (faculty_id, ))
        row = res.fetchone()

        cursor.close()
        connection.close()

        return row
    

    def get_faculty_list(self, department_id):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Faculty WHERE department_id = ?', (department_id, ))
        rows = res.fetchall()

        cursor.close()
        connection.close()

        return rows
    

    def get_non_fa_faculties(self):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Faculty WHERE id NOT IN (SELECT fid FROM FacultyAdvisor)')
        rows = res.fetchall()

        cursor.close()
        connection.close()

        return rows
    

    def is_advisor(self, faculty_id):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT COUNT(*) FROM FacultyAdvisor WHERE fid = ?', (faculty_id, ))
        count = res.fetchone()[0]

        cursor.close()
        connection.close()

        if count == 0:
            return False
        else:
            return True
        

    def get_active_registrations(self, faculty_id):
        if not self.is_advisor(faculty_id):
            return 'Should be a Faculty Advisor'
        
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT batch FROM FacultyAdvisor WHERE fid = ?', (faculty_id, ))
        batch = res.fetchone()[0]

        query = '''
            SELECT a.student_id, s.fname || ' ' || s.lname, a.course_id, c.cname, f.fname || ' ' || f.lname
            FROM Application a 
            JOIN Student s ON a.student_id = s.id
            JOIN Course c ON a.course_id = c.cid
            JOIN Faculty f ON c.faculty = f.id
            WHERE s.batch = ?;
        '''
        res = cursor.execute(query, (batch, ))
        rows = res.fetchall()

        return rows


    def accept_registration(self, course_id, student_id):
        connection = sqlite3.connect('Server.db')
        cursor = connection.cursor()

        res = cursor.execute('SELECT COUNT(*) FROM Application WHERE course_id = ? AND student_id = ?', 
                             (course_id, student_id))
        count = res.fetchone()[0]

        return_str = ""
        if count == 0:
            return_str = 'Incorrect Application Details'
        else:
            cursor.execute('DELETE FROM Application WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            cursor.execute('INSERT INTO Accepted VALUES(?, ?)', (course_id, student_id))
            connection.commit()
            return_str = 'Registration Accepted'

        cursor.close()
        connection.close()

        return return_str
    

    def reject_registration(self, course_id, student_id):
        connection = sqlite3.connect('Server.db')
        cursor = connection.cursor()

        res = cursor.execute('SELECT COUNT(*) FROM Application WHERE course_id = ? AND student_id = ?', 
                             (course_id, student_id))
        count = res.fetchone()[0]

        return_str = ""
        if count == 0:
            return_str = 'Incorrect Application Details'
        else:
            cursor.execute('DELETE FROM Application WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            cursor.execute('INSERT INTO Rejected VALUES(?, ?)', (course_id, student_id))
            connection.commit()
            return_str = 'Registration Rejected'

        cursor.close()
        connection.close()

        return return_str