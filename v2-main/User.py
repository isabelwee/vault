
class User:
    # for logging in user
    def __init__(self, email, hashedMasterPassword, accounts):
        self.email = email
        self.hashedMasterPassword = hashedMasterPassword
        
        if accounts is None:
            self.accounts = None
        else:
            for account in accounts:
                self.accounts.append(account)

    def getEmail(self):
        return self.email
