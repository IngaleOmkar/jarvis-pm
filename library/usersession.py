from library.account import account

class usersession(object):

    def __init__(self, userName, authHash, key, clipboard, lock, vault=[]):
        self.userName = userName
        self.authHash = authHash
        self.key = key
        self.vault = vault
        self.lock = lock
        self.clipboard = clipboard

    def clearVault(self):
        self.vault = []
        
    def getUserAccount(self, name):
        account = next((a for a in self.vault if a.name == name), None)
        return account

    def checkAccountExists(self, name):
        account = name in self.getUserAccountNames()
        return account

    def getUserAccountNames(self):
        accountNames = sorted([a.name for a in self.vault])
        return accountNames

    def display_account(self, name):
        self.getUserAccount(name).display()

    def deleteAccount(self, name):
        self.vault.remove(self.getUserAccount(name))

    def vaultToDictionary(self):
        dictionary = [a.__dict__ for a in self.vault]
        return dictionary

    def dictionaryToVault(self, dictionary):
        for x in dictionary:
            self.vault.append(account(x['name'], x['username'], x['password']))