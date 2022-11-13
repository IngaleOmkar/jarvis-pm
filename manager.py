from library.account import account
from library.api import updateVault
from library.crypto import generatePassword


def EditAccount(lnAccountName, lnUserName, lnPassword, currentsession):
    ErrorMessage = ""
    Error = False
    ANupdate = False
    # check if empty
    if lnAccountName and lnUserName and lnPassword:
        # check password is >8 and <64
        if len(lnPassword) >= 8 and len(lnPassword) <= 64:
            if not currentsession.checkAccountExists(lnAccountName):
                ANupdate = True
            else:
                Error = True
                return {'error': 'Account name already exists'}
            if ANupdate and Error == False:
                new_account = account(lnAccountName, lnUserName, lnPassword)
                currentsession.vault.append(new_account)
                updateVault(currentsession)
                return {'success': 'Account added'}
            else:
                return {'error': 'Unknwon error. No changes made to vault'}
        else:
            return {'error': 'Password must be between 8 and 64 characters'}
    else:
        return {'error': 'All fields are required'}


def editSavedetails(item, newAN, newUN, newP, currentsession):
    ANupdate = False
    UNupdate = False
    Pupdate = False
    OriginalItem = item
    TbcItem = item
    Error = False
    # check not empty
    ErrorMessage = ""
    if newAN and newUN and newP:
        # check password is >8 and <64
        if len(newP) >= 8 and len(newP) <= 64:
            if newAN != OriginalItem.name:
                if not currentsession.checkAccountExists(newAN):
                    TbcItem.name = newAN
                    ANupdate = True
                else:
                    Error = True
                    return {'error': 'This AccountName already exists'}
            if OriginalItem.username != newUN:
                TbcItem.username = newUN
                UNupdate = True
            if OriginalItem.password != newP:
                TbcItem.password = newP
                Pupdate = True
            if (Pupdate or UNupdate or ANupdate) and Error == False:
                if ANupdate:
                    item.name = TbcItem.name
                if UNupdate:
                    item.username = TbcItem.username
                if Pupdate:
                    item.password = TbcItem.password
                updateVault(currentsession)
                return {'success': 'Account edited'}
            else:
                return {'error': 'Unknwon error. No changes made to vault'}

        else:
            return {'error': 'Password must be between 8 and 64 characters'}
    else:
        return {'error': 'All fields are required'}
