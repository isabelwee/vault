#! /usr/bin/env python3
import sys
from manage_account import account_exists, create_account, login
from arguments import run
from values import Commands

def main():
    # Create a vault account if the user does not have one yet
    if not account_exists('~'):
        create_account()

    # Prompt user to log in 
    print("Log into your account")
    login()
    
    
    while True:
        cmd = input("Enter command: ")
        if cmd == Commands.QUIT_PROGRAM.value:
            print("Logging out")
            sys.exit(0)
        else:
            run(cmd)


main()