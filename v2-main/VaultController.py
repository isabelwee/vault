import sys
from os import urandom
from hashlib import sha256
from getpass import getpass
from Commands import Commands
from User import User
from PocketBaseController import PocketBaseController

class VaultController:
    SALT_LEN = 16

    pbController = PocketBaseController()
    user = None
    
    def run(self):
        print("Welcome to Vault. Type \'help\' for list of commands.")

        while True:
            cmd = input()
            if cmd == Commands.HELP.value:
                self.help_options()
            elif cmd == Commands.QUIT.value:
                print("See you next time!")
                sys.exit(0)
            elif cmd == Commands.REGISTER.value:
                self.user = self.userRegister(self)
                print(self.user.getEmail())
                print("Account successfully created. You are now logged in.")
            elif cmd == Commands.LOGIN.value:
                self.userLogin(self)
            elif cmd == Commands.PREVIEW.value:
                pass
            elif cmd == Commands.VIEW_ACCOUNT.value:
                pass
            else:
                print("Usage: command")
                print("Type \'help\' to view list of commands")

    def userRegister(self):
        name = input("Enter your name: ")
        email = input("Register an email: ")
        username = input("Create a username: ")
        plaintextPassword = getpass("Create a master password:")
        hashedPassword = self.getHashOf(self, plaintextPassword)

        # create new user record in users collection of database
        user_data = {
            "username": username,
            "email": email,
            "password": hashedPassword,
            "passwordConfirm": hashedPassword,
            "name": name,
            "hashed_master_password": hashedPassword
        }

        self.pbController.createRecord('users', user_data)

        # create user instance
        return User(email, hashedPassword, None)
    
    def userLogin(self):
        username = input("Enter username: ")
        data = self.pbController.getRecord('users', username)
        


    def help_options():
        print("\n\033[1mOPTIONS:\033[0m")
    
        print("\t\033[1mhelp\033[0m")
        print("\t\tGet list of available commands\n")

        print("\t\033[1mq\033[0m")
        print("\t\tLogout and exit Vault\n")
        
        print("\t\033[1mr\033[0m")
        print("\t\tRegister for a new Vault account\n")

        print("\t\033[1ml\033[0m")
        print("\t\tLogin to an existing Vault account\n")

        print("\t\033[1mp\033[0m")
        print("\t\tPreview list of accounts stored in your Vault\n")

        print("\t\033[1mv <platform name>\033[0m")
        print("\t\tView account information of a given platform\n")

    def getHashOf(self, plaintext):
        return sha256(plaintext.encode('utf-8')).hexdigest()


controller = VaultController
controller.run(controller)