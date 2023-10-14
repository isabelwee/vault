from connect_db import connect_to_db
from getpass import getpass
import sql_queries as sql_queries
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
    
    print("Register an email: ")
    email = input()
    # check email is correct format
    print("Create a master password; must include at least one capital letter, one number and one special character: ")
    master_pwd = getpass()

    # check if the password meets password criteria
    print(master_pwd)

