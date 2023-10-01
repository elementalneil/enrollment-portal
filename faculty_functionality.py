import sqlite3
import bcrypt

class Faculty:
    def register(self, faculty_data):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM Faculty')

        rows = cursor.fetchall()
        id_values = [row[0] for row in rows]

        if faculty_data['id'] in id_values:
            cursor.close()
            connection.close()
            return False
        else:
            password = bytes(faculty_data['password'], 'utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cursor.execute('INSERT INTO Faculty VALUES (?, ?, ?, ?, ?, ?, ?)', (
                faculty_data['id'], hashed_password, faculty_data['fname'], 
                faculty_data['lname'], faculty_data['email'], faculty_data['contact'],
                faculty_data['department_id']
            ))

            connection.commit()

            cursor.close()
            connection.close()
            return True
        
    def faculty_login(self, faculty_id, password):
        connection = sqlite3.connect("Server.db")
        cursor = connection.cursor()

        res = cursor.execute('SELECT * FROM Faculty WHERE id = ?', (faculty_id, ))
        row = res.fetchone()

        if row != None:
            password = bytes(password, 'utf-8')
            if(bcrypt.checkpw(password, row[1])):
                return 'Successfully Logged In'
            else:
                return 'Incorrect Password'
        else:
            return 'Incorrect Username'