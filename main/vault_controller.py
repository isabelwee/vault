#! /usr/bin/env python3
import argparse
from master_pwd import login
from init_account import account_exists, create_account
from connect_db import close_db
from arguments import add_args, run_args


def main():
    # Create a vault account if the user does not have one yet
    if not account_exists():
        create_account()

    arg_parser = argparse.ArgumentParser(
        description="Local Password Manager Vault", usage="[options]"
    )

    # Prompt user to log in 
    print("Log into your account")
    login()
    
    # TODO: write up commands 
    arg_parser = add_args(arg_parser)
    args = arg_parser.parse_args()
    run_args(args)

    
    close_db()



main()