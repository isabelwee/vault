#! /usr/bin/env python3
from connect_db import connect_to_db
import sql_queries

def run_args(args):
    if args.add_gen:
        add_account_gen_pwd(args)
    elif args.add_input:
        add_account_has_pwd(args)
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


# given account details, adds it to the database as a new row
def add_account_gen_pwd(args):
    db = connect_to_db()
    cur = db.cursor()
    
    password = generate_pwd()
    # check number of arguments to see if there's a username
    if len(vars(args)) == 2:
        # if there is no username
        ...
    else:
        # if there is username
        cur.execute(sql_queries.insert_row(), [args[0], args[1], args[2], password])

    
    db.commit()

    cur.close()

# TODO: implement function
def generate_pwd():
    ...

def add_args(arg_parser):
    arg_parser.add_argument(
        "-a",
        "--add_gen", 
        type=str, 
        nargs='2,3', 
        help="Add new entry, password will be auto-generated\n"
        "Username is optional",
        metavar=("[APP_NAME]", "<USERNAME>", "[EMAIL]"))
    
    arg_parser.add_argument(
        "-i", 
        "--add_input", 
        type=str, 
        nargs='3,4', 
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
        type=str,
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