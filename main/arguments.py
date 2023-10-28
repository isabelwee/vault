#! /usr/bin/env python3
from connect_db import connect_to_db, close_db
from bcrypt import hashpw, checkpw, gensalt
from main.manage_passwords import get_db_password
from values import Range, Commands
from cryptography.fernet import Fernet
import sql_queries, secrets, string



# TODO: exceptions for when user types in wrong inputs (mainly app_name)
# TODO: implement password generator function
# TODO: update_username function - need to check if there is a username 
# TODO: implement MFA for updating a password ?

def run(cmd):
    db = connect_to_db()
    if cmd[0] == Commands.ADD_GEN.value:
        add_account_gen_pwd(cmd, db)
    elif cmd[0] == Commands.ADD_INPUT.value:
        add_account_has_pwd(cmd, db)
    elif cmd[0] == Commands.DELETE.value:
        ...
    elif cmd[0] == Commands.UPDATE_APP_NAME.value:
        ...
    elif cmd[0] == Commands.UPDATE_USERNAME.value:
        ...
    elif cmd[0] == Commands.UPDATE_EMAIL.value:
        ...
    elif cmd[0] == Commands.UPDATE_PASSWORD.value:
        ...
    elif cmd[0] == Commands.LIST_ACCOUNTS.value:
        ...
    elif cmd[0] == Commands.QUERY_ACCOUNT.value:
        ...
    elif cmd[0] == Commands.HELP.value:
        print_options()
    else: 
        print("Usage: command [<arguments>]")
        print("Enter 'help' to view command options\n")

    close_db(db)


# given account details (email, optionally usrname), adds it to the database as a new account
# generates a password for that user's account
def add_account_gen_pwd(cmd, db):
    if not validate_num_args(cmd[1:], Range.MIN_ADD_GEN_ARGS.value, Range.MAX_ADD_GEN_ARGS.value):
        return

    cur = db.cursor()
    
    password = generate_pwd()
    app_name = cmd[0]
    # TODO: hash password

    # if there is no username
    if len(cmd) == 2:
        user_email = cmd[1]
        cur.execute(sql_queries.db_insert_row_no_username(), [app_name, user_email, password])
    # if there is username
    else:
        username = cmd[1]
        user_email = cmd[2]
        cur.execute(sql_queries.db_insert_row(), [app_name, username, user_email, password])

    
    db.commit()
    cur.close()


# adapted from https://geekflare.com/password-generator-python-code/
def generate_pwd():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    pwd_len = 12
    pwd = ''
    while True:
        for _ in range(pwd_len):
            pwd += ''.join(secrets.choice(alphabet))
        
        if any(char in string.punctuation for char in pwd) and sum(char in string.digits for char in pwd) >= 1:
            break
    
    return pwd

# given account details (email, pwd, optionally usrname), adds it to the database as a new account
def add_account_has_pwd(args, db):
    if validate_num_args(args, Range.MIN_ADD_INPUT, Range.MAX_ADD_INPUT) == False:
        return 
    
    cur = db.cursor()

    app_name = args[0]
    if len(vars(args)) == 3:
        # if there is no username
        user_email = args[1]
        password = args[2]
        cur.execute(sql_queries.db_insert_row_no_username(), [app_name, user_email, password])
    else:
        # if there is a username
        username = args[1]
        user_email = args[2]
        password = args[3]
        cur.execute(sql_queries.db_insert_row(), [app_name, username, user_email, password])
    
    db.commit()
    cur.close()

# given an app name, deletes all related details from the vault
def delete_account(args):
    # TODO: check correct number of args given
    # TODO: check that app name is correct/exists in the database
    db = connect_to_db()
    cur = db.cursor()

    app_name = args[0]
    cur.execute(sql_queries.db_delete_row(), [app_name])

    db.commit()
    cur.close()

# given an old and new app name, updates the database accordingly
def update_app_name(args):
    # TODO: check that app name is correct/exists in the database
    db = connect_to_db()
    cur = db.cursor()

    new_name = args[0]
    old_name = args[1]
    cur.execute(sql_queries.db_update_app_name(), [new_name, old_name])

    db.commit()
    cur.close()

# given the name of an app in the vault, updates the associated username

def update_username(args):
    # TODO: check that app name is correct/exists in the database
    db = connect_to_db()
    cur = db.cursor()

    new_username = args[0]
    app_name = args[1]
    cur.execute(sql_queries.db_update_username(), [new_username, app_name])

    db.commit()
    cur.close()

# given the name of an app in the vault, updates the associated email
def update_email(args):
    # TODO: check that app name is correct/exists in the database
    db = connect_to_db()
    cur = db.cursor()

    new_email = args[0]
    app_name = args[1]
    cur.execute(sql_queries.db_update_email(), [new_email, app_name])

    db.commit()
    cur.close()

def update_password(args):
    # TODO: check that app name is correct/exists in the database
    password = args[0]
    app_name = args[1]

    # get password from database and compare to new password, if the same throw an error
    if not checkpw(password.encode(), get_db_password()):
        print("Error: New password and old password are the same")
        return
    
    hashed_password = hashpw(password, gensalt())
    
    db = connect_to_db()
    cur = db.cursor()

    cur.execute(sql_queries.db_update_password(), [hashed_password, app_name])

    db.commit()
    cur.close()


def list_all_accounts():
    db = connect_to_db()
    cur = db.cursor()

    # get everything from vault
    # iterate through
    cur.execute("SELECT * from Vault")
    print(cur.fetchall)


    # cursor.execute("SELECT * from Vault")
    #     record = cursor.fetchall()  
    #     for i in range(len(record)):
    #         entry = record[i]
    #         for j in range(len(entry)):
    #             titles = ["URL: ", "Username: ", "Password: "]
    #             if titles[j] == "Password: ":
    #                 bytes_row = entry[j]
    #                 password = master_password.decrypt_password(bytes_row, master_password_hash)
    #                 print("Password: " + str(password.decode('utf-8')))
    #             else:
    #                 print(titles[j] + entry[j])

            
    #         print( "----------")


def query_account():
    ...


def validate_num_args(cmd, low, high):
    if (len(cmd) < low or len(cmd) > high):
        print("Incorrect number of arguments")
        print("Enter 'help' to view command options\n")
        return False
    else:
        return True


def print_options():
    print("\n\033[1mOPTIONS:\033[0m")
    
    print("\t\033[1m-a\033[0m <app_name> [<username>] <email>")
    print("\t\tAdd a new account to the vault, password will be auto-generated\n")

    print("\t\033[1m-i\033[0m <app_name> [<username>] <email> <password>")
    print("\t\tAdd a new account to the vault with an existing password\n")
    
    print("\t\033[1m-d\033[0m <app_name>")
    print("\t\tDelete an account in the vault with the given app name\n")

    print("\t\033[1m-uapp\033[0m <new_app_name> <current_app_name>")
    print("\t\tUpdate app name of an existing account\n")

    print("\t\033[1m-uusr\033[0m <new_username> <app_name>")
    print("\t\tUpdates username of account of the given app name\n")

    print("\t\033[1m-uemail\033[0m <new_email> <app_name>")
    print("\t\tUpdates email of account of the given app name\n")

    print("\t\033[1m-upwd\033[0m <new_password> <app_name>")
    print("\t\tUpdates password of account of the given app name\n")

    print("\t\033[1m-l\033[0m")
    print("\t\tList all the accounts in the password vault\n")

    print("\t\033[1m-q\033[0m <app_name>")
    print("\t\tLook up an account by app name\n")

    print("\t\033[1mhelp\033[0m")
    print("\t\tView list of commands\n")

    print("\t\033[1mquit\033[0m")
    print("\t\tLog out of the vault\n")

