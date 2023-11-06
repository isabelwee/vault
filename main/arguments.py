#! /usr/bin/env python3
from connect_db import connect_to_db, close_db
from bcrypt import hashpw, checkpw, gensalt
from manage_passwords import get_db_masterpwd, generate_pwd, encrypt_password, decrypt_password
from manage_account import account_exists
from getpass import getpass
from values import Range, Commands
from psycopg2.errors import UniqueViolation
import sql_queries, binascii


def run(cmd):
    db = connect_to_db()
    if cmd == Commands.ADD_GEN.value:
        add_account(db, True)
    elif cmd == Commands.ADD_INPUT.value:
        add_account(db, False)
    elif cmd == Commands.DELETE.value:
        delete_account(db)
    elif cmd == Commands.UPDATE_APP_NAME.value:
        update_app_name(db)
    elif cmd == Commands.UPDATE_USERNAME.value:
        update_username(db)
    elif cmd == Commands.UPDATE_EMAIL.value:
        update_email(db)
    elif cmd == Commands.UPDATE_PASSWORD.value:
        update_password(db)
    elif cmd == Commands.LIST_ACCOUNTS.value:
        list_all_accounts(db)
    elif cmd == Commands.QUERY_ACCOUNT.value:
        query_account(db)
    elif cmd == Commands.HELP.value:
        print_options()
    else: 
        print("Usage: command")
        print("Enter 'help' to view command options\n")

    close_db(db)


# creates a new account in the database with the inputted details
def add_account(db, gen_pwd):
    cur = db.cursor()

    app_name = input("Enter app name: ")
    email = input("Enter email: ")
    username = input("Enter username: ")

    if gen_pwd:
        password = generate_pwd()
    else:
        password = getpass("Enter password: ")

    password = encrypt_password(password)

    try:
        cur.execute(sql_queries.db_insert_row(), [app_name, username, email, password])
    except UniqueViolation:
        print(f"An account for {app_name} already exists")
    else:
        print(f"Account for {app_name} successfully created")
    
    db.commit()
    cur.close()


# given an app name, deletes all related details from the vault
def delete_account(db):
    cur = db.cursor()

    app_name = input("Enter app name of account to delete: ")

    if not account_exists(app_name):
        print(f"An account for {app_name} does not exist")
    else:
        cur.execute(sql_queries.db_delete_row(), [app_name])
        print(f"Account for {app_name} successfully deleted")

    db.commit()
    cur.close()

# given an old and new app name, updates the database accordingly
def update_app_name(db):
    db = connect_to_db()
    cur = db.cursor()

    old_name = input("Enter current name of app: ")
    if not account_exists(old_name):
        print(f"An account for {old_name} does not exist")
    else:
        new_name = input("Enter new name: ")
        cur.execute(sql_queries.db_update_app_name(), [new_name, old_name])
        print(f"App name successfully updated to {new_name}")

    db.commit()
    cur.close()

# given the name of an app in the vault, updates the associated username
def update_username(db):
    db = connect_to_db()
    cur = db.cursor()

    app_name = input("Enter app name of the username to change: ")
    if not account_exists(app_name):
        print(f"An account for {app_name} does not exist")
    else:
        new_username = input("Enter new username: ")
        cur.execute(sql_queries.db_update_username(), [new_username, app_name])
        print(f"Username for {app_name} successfully updated to {new_username}")

    db.commit()
    cur.close()

# given the name of an app in the vault, updates the associated email
def update_email(db):
    db = connect_to_db()
    cur = db.cursor()

    app_name = input("Enter app name of the email to change: ")
    if not account_exists(app_name):
        print(f"An account for {app_name} does not exist")
    else:
        new_email = input("Enter new email: ")
        cur.execute(sql_queries.db_update_email(), [new_email, app_name])
        print(f"Email for {app_name} successfully updated to {new_email}")
    
    db.commit()
    cur.close()

def update_password(db):
    db = connect_to_db()
    cur = db.cursor()

    app_name = input("Enter app name of the password to change: ")
    if not account_exists(app_name):
        print(f"An account for {app_name} does not exist")
    else:
        new_password = encrypt_password(input("Enter new password: ")) 
        cur.execute(sql_queries.db_update_password(), [new_password, app_name]) 
        print(f"Password for {app_name} successfully updated")

    db.commit()
    cur.close()


def list_all_accounts(db):
    cur = db.cursor()

    cur.execute(sql_queries.db_fetch_vault())
    accounts = cur.fetchall()

    for account in accounts:
        if account[0] == '~':
            continue

        app_name = account[0]
        username = account[1]
        email = account[2]
        password = decrypt_password(account[3])

        list_account(app_name, username, email, password)

def query_account(db):
    cur = db.cursor()

    print("Warning: password will be displayed. Do you wish to continue? [y/n]: ")
    app_name = input("Enter the app name of the account you want to view: ")

    cur.execute(sql_queries.db_get_row(), [app_name])
    account = cur.fetchall()

    try:
        username = account[0][1]
        email = account[0][2]
        password = decrypt_password(account[0][3])
    except IndexError:
        print("Error: Account for that app doesn't exist\n")
    else:
        list_account(app_name, username, email, password)

def list_account(app_name, username, email, password):
    print("---------------------------------------------------------------------------")
    print(f"\033[1m{app_name.upper()}\033[0m")
    print(f"Username: {username}")
    print(f"Email:    {email}")
    print(f"Password: {password}")
    print("---------------------------------------------------------------------------")


def print_options():
    print("\n\033[1mOPTIONS:\033[0m")
    
    print("\t\033[1m-a\033")
    print("\t\tAdd a new account to the vault, password will be auto-generated\n")

    print("\t\033[1m-i\033[0m")
    print("\t\tAdd a new account to the vault with an existing password\n")
    
    print("\t\033[1m-d\033[0m")
    print("\t\tDelete an account in the vault with the given app name\n")

    print("\t\033[1m-uapp\033[0m")
    print("\t\tUpdate app name of an existing account\n")

    print("\t\033[1m-uusr\033[0m")
    print("\t\tUpdates username of account of the given app name\n")

    print("\t\033[1m-uemail\033[0m")
    print("\t\tUpdates email of account of the given app name\n")

    print("\t\033[1m-upwd\033[0m")
    print("\t\tUpdates password of account of the given app name\n")

    print("\t\033[1m-l\033[0m")
    print("\t\tList all the accounts in the password vault\n")

    print("\t\033[1m-q\033[0m")
    print("\t\tLook up an account by app name\n")

    print("\t\033[1mhelp\033[0m")
    print("\t\tView list of commands\n")

    print("\t\033[1mquit\033[0m")
    print("\t\tLog out of the vault\n")

