import sqlite3
import bcrypt

class Student:
    def register(self, student_data):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id, email FROM Student')

        rows = cursor.fetchall()
        id_values = [row[0] for row in rows]
        email_values = [row[1] for row in rows]

        cursor.execute('SELECT did FROM Department')
        rows = cursor.fetchall()
        did_values = [row[0] for row in rows]

        return_message = ""

        if student_data['id'] in id_values:
            return_message = "Student Already Registered"
        elif student_data['email'] in email_values:
            return_message = "Email is Already Registered"
        elif student_data['department_id'] not in did_values:
            return_message = "Department does not Exist"
        else:
            password = bytes(student_data['password'], 'utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cursor.execute('INSERT INTO Student VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
                student_data['id'], hashed_password, student_data['fname'], 
                student_data['lname'], student_data['email'], student_data['contact'],
                student_data['batch'], student_data['department_id']
            ))

            connection.commit()
            return_message = "Successfully Registered"

        cursor.close()
        connection.close()
        return return_message
            
        
    def student_login(self, student_id, password):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Student WHERE id = ?', (student_id, ))
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
    

    def get_details(self, student_id):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Student WHERE id = ?', (student_id, ))
        row = res.fetchone()

        cursor.close()
        connection.close()

        return row