#! /usr/bin/env python3
import connect_db
import argparse
import master_pwd
from getpass import getpass
from init_account import account_exists, create_account


def main():
    # TODO: create account feature
    # check if account exists, if not, pass it into create account function
    if not account_exists():
        create_account()

    arg_parser = argparse.ArgumentParser(
        description="Local Password Manager Vault", usage="[options]"
    )

    # TODO: encrypt and hash master password 
    master_pwd_plain = getpass("Enter master password: ").encode()
    hashed = master_pwd.get_hashed_masterpwd(master_pwd_plain)
    # check masterpwd
    

main()