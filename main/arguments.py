#! /usr/bin/env python3
from connect_db import connect_to_db, close_db
from bcrypt import hashpw, checkpw, gensalt
from master_pwd import get_db_password
from values import Range
import sql_queries
import argparse



# TODO: exceptions for when user types in wrong inputs (mainly app_name)
# TODO: implement password generator function
# TODO: update_username function - need to check if there is a username 
# TODO: implement MFA for updating a password ?

def run_args(args):
    db = connect_to_db()
    if args.add_gen:
        add_account_gen_pwd(args, db)
    elif args.add_input:
        add_account_has_pwd(args, db)
    elif args.delete:
        ...
    elif args.update_app:
        ...
    elif args.update_username:
        ...
    elif args.update_email:
        ...
    elif args.update_password:
        ...
    elif args.list:
        ...
    elif args.query:
        ...

    close_db(db)


# given account details (email, optionally usrname), adds it to the database as a new account
# generates a password for that user's account
def add_account_gen_pwd(args, db):
    validate_num_args(args, Range.MIN_ADD_GEN_ARGS, Range.MAX_ADD_GEN_ARGS)

    cur = db.cursor()
    
    password = generate_pwd()
    app_name = args[0]
    # TODO: hash password

    if len(vars(args)) == 2:
        # if there is no username
        user_email = args[1]
        cur.execute(sql_queries.db_insert_row_no_username(), [app_name, user_email, password])
    else:
        # if there is username
        username = args[1]
        user_email = args[2]
        cur.execute(sql_queries.db_insert_row(), [app_name, username, user_email, password])

    
    db.commit()
    cur.close()

def generate_pwd():
    ...

# given account details (email, pwd, optionally usrname), adds it to the database as a new account
def add_account_has_pwd(args, db):
    validate_num_args(args, Range.MIN_ADD_INPUT, Range.MAX_ADD_INPUT)

    db = connect_to_db()
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

def validate_num_args(arg, low, high):
    if (len(arg) < low or len(arg) > high):
        raise argparse.ArgumentTypeError('Incorrect number of arguments. View options for more help.')

def add_args(arg_parser):
    arg_parser.add_argument(
        "-a",
        "--add_gen", 
        type=str, 
        nargs=3, 
        help="Add new entry, password will be auto-generated\n"
        "Username is optional",
        metavar=("[APP_NAME]", "<USERNAME>", "[EMAIL]"))

    
    arg_parser.add_argument(
        "-i", 
        "--add_input", 
        type=str, 
        nargs=4, 
        help="Add new entry with manually inputted password\n"
        "Username is optional",
        metavar=("[APP_NAME]", "<USERNAME>", "[EMAIL]", "[PASSWORD]"))
    
    arg_parser.add_argument(
        "-d", 
        "--delete", 
        type=str, 
        nargs=1, 
        help="Delete entry by app name", 
        metavar=("[APP_NAME]"))
    
    arg_parser.add_argument(
        "-uapp",
        "--update_app",
        type=str,
        nargs=2,
        help="Update the app name",
        metavar=("[NEW_APP_NAME]", "[OLD_APP_NAME]"))
    
    arg_parser.add_argument(
        "-uusr",
        "--update_username",
        type=str,
        nargs=2,
        help="Update username of an account",
        metavar=("[APP_NAME]", "[NEW_USERNAME]"))
    
    arg_parser.add_argument(
        "-uemail",
        "--update_email",
        type=str,
        nargs=2,
        help="Update email of an account",
        metavar=("[APP_NAME]", "[NEW_EMAIL]"))
    
    arg_parser.add_argument(
        "-upwd",
        "--update_password",
        type=str,
        nargs=2,
        help="Update password of an account",
        metavar=("[APP_NAME]", "[NEW_PASSWORD]"))
    
    arg_parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all the accounts in the password vault")
    
    arg_parser.add_argument(
        "-q",
        "--query",
        type=str,
        nargs=1,
        help="Look up an account by app name",
        metavar=("[URL]"))

    return arg_parser