#! /usr/bin/env python3
import argparse, sys
from master_pwd import login
from init_account import account_exists, create_account
from connect_db import close_db
from arguments import run, print_options
from values import Commands

def main():
    # Create a vault account if the user does not have one yet
    if not account_exists():
        create_account()

    # Prompt user to log in 
    print("Log into your account")
    login()
    
    # TODO: write up commands 
    # arg_parser = add_args(arg_parser)
    # args = arg_parser.parse_args()
    while True:
        cmd = input("Enter command: ").split(' ')
        if cmd[0] == Commands.QUIT_PROGRAM.value:
            print("Logging out")
            sys.exit(0)
        else:
            run(cmd)


main()