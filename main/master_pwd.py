from bcrypt import checkpw
from getpass import getpass
from connect_db import connect_to_db
import sql_queries
import sys

# Checks if input is same as password stored in the database 
def login():
    # verify password
    input = getpass("Enter master password: ").encode()
    if not checkpw(input, get_db_password()):
        print("Incorrect password. Run the program again.")
        sys.exit(0)
    else:
        print("Successfully logged in!")


def get_db_password():
    db = connect_to_db()
    cur = db.cursor()

    cur.execute(sql_queries.db_get_row(), ['~'])
    account = cur.fetchall()
    cur.close()

    return account[0][4]