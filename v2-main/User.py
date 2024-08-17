from getpass import getpass
from os import getenv

class User:
    def __init__(self, dbId, email, hashedMasterPassword, accounts):
        self.dbId = dbId
        self.email = email
        self.hashedMasterPassword = hashedMasterPassword

        if accounts is None:
            self.accounts = None
        else:
            for account in accounts:
                self.accounts.append(account)

    def getEmail(self):
        return self.email

    def createAccount(self):
        platform = input("Enter platform name: ")
        username = input("Enter username used for platform: ")
        email = input("Enter email used for platform: ")
        plaintextPassword = getpass("Enter password used for platform: ")

        # encrypt password
        encryption_key = getenv('ENCRYPTION_KEY')


        data = {
            "id": self.dbId,
            "platform_name": platform,
            "username": username,
            "email": email
        }
