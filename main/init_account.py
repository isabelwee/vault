from connect_db import connect_to_db
from getpass import getpass
import sql_queries as sql_queries

# checks if user has a password vault
def account_exists():
    db = connect_to_db()
    cur = db.cursor()
    cur.execute(sql_queries.get_row(), ['admin_account'])
    account = cur.fetchall()

    return False if not account else True

# creates a new vault account
def create_account():
    email = input("Register an email: ")
    master_pwd = getpass("Enter master password: ").encode()
