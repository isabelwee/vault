import sys
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
                self.userRegister(self)
            elif cmd == Commands.LOGIN.value:
                self.userLogin(self)
            elif cmd == Commands.PREVIEW.value:
                pass
            elif cmd == Commands.VIEW_ACCOUNT.value:
                pass
            elif cmd == Commands.ADD_ACCOUNT.value:
                self.addAccount(self)
            else:
                print("Usage: command")
                print("Type \'help\' to view list of commands")

    def userRegister(self):
        name = input("Enter your name: ")
        email = input("Register an email: ")
        username = input("Create a username: ")
        plaintextPassword = getpass("Create a master password: ")
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

        # get database id of user
        userInfo = self.pbController.getUserRecord(username)
        uId = userInfo['id']

        # create user instance to 'log them in'
        self.user = User(uId, email, hashedPassword, None)
        print("Account successfully created. You are now logged in.")
    
    def userLogin(self):
        if self.user is not None:
            print("Error: Already logged in")

        username = input("Enter username: ")

        # extract user info from database 
        userInfo = self.pbController.getUserRecord(username) 
        if userInfo is None:
            print("Error: user does not exist")
            return
        
        # verify password
        dbPassword = userInfo['hashed_master_password']
        inputPasswordPlaintext = getpass("Enter master password: ")
        inputPasswordHashed = self.getHashOf(self, inputPasswordPlaintext)

        if dbPassword != inputPasswordHashed:
            print("Error: incorrect master password")
            return

        # get user accounts

        self.user = User(userInfo['id'], None, dbPassword, None)
        print("Successfully logged in")


    def addAccount(self):
        if self.user is None:
            print("Error: Please log in or register for a Vault account")
            return
        
        self.user.createAccount()


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

        print("\t\033[1ma\033[0m")
        print("\t\tAdd account information for a new platform\n")

    def getHashOf(self, plaintext):
        return sha256(plaintext.encode('utf-8')).hexdigest()


controller = VaultController
controller.run(controller)