#! /usr/bin/env python3
import connect_db
import argparse
import getpass


def main():
    arg_parser = argparse.ArgumentParser(
        description="Local Password Manager Vault", usage="[options]"
    )

    master_password_plain = getpass.getpass("Enter master password: ").encode()
    print(master_password_plain)


main()