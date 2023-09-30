import sqlite3
import bcrypt

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

        if row != None:
            password = bytes(password, 'utf-8')
            if(bcrypt.checkpw(password, row[1])):
                return 'Successfully Logged In'
            else:
                return 'Incorrect Password'
        else:
            return 'Incorrect Username'


def __main__():
    admin_data = {}

    choice1 = input('Press 1 to Register, 2 to Login or anything else to Exit: ')

    if choice1 == '1':
        print('Admin Register: ')
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
                else:
                    print('Admin is Already Registered')
            else:
                print('Aborted by User')
        else:
            print('Password should match Confirm Password')

    elif choice1 == '2':
        print('Admin Login:')
        admin_id = input('Admin Id: ')
        password = input('Password: ')

        admin = Admin()
        print(admin.admin_login(admin_id, password))

    else:
        print('Aborted by User')


if __name__ == '__main__':
    __main__()