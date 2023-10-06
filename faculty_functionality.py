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
                faculty_data['id'], hashed_password, faculty_data['fname'], 
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