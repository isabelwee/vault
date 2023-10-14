from connect_db import connect_to_db
from getpass import getpass
from master_pwd import get_hashed_masterpwd
import sql_queries 
import re


# checks if user has a password vault
def account_exists():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(sql_queries.get_row(), ['admin_account'])
    account = cur.fetchall()

    return False if not account else True

# creates a new vault account
def create_account():
    print("It seems you don't have an account. Let's begin the registration process :)")
    print("---------------------------------------------------------------------------")
    email = register_email()
    hashed_password = register_password()
    db_create_account(email, hashed_password)
    print("Account successfully created!")
    print("---------------------------------------------------------------------------")

def register_email():
    print("Register an email: ")
    while True:
        email = input()
        if not re.search(r'@[a-z]+\.com', email):
            print("Incorrect email format, try again")
        else:
            return email

def register_password():
    print("Create a master password. must include at least one capital letter, one number and one special character: ")
    while True:
        password = getpass()
        if len(password) < 8:
            print("Make sure your password is at least 8 letters")
        elif re.search('[0-9]',password) is None:
            print("Make sure your password has a number in it")
        elif re.search('[A-Z]',password) is None: 
            print("Make sure your password has a capital letter in it")
        elif re.search('[!@#$%^&*()]',password) is None: 
            print("Make sure your password has a special character in it")
        else:
            print("Re-enter password: ")
            password_validate = getpass()
            if (password != password_validate):
                print("Passwords do not match. Retry a new password:")
                break
        break

# hash password

def db_create_account(email, password):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(sql_queries.insert_row(), ['~', email, email, password])

