import base64
import json

import pyrebase

from library.crypto import decryptVault, encryptVault, getAuthHash, getKey
from library.usersession import usersession


def getConfig():
    '''
    returns firebase api connection
    '''
    # config={"apiKey": "AIzaSyCRrMaXBPx_GVbBJZzaaFsZxEeOGeh13xk",
    #         "authDomain": "cz4010project.firebaseapp.com",
    #         "databaseURL": "https://cz4010project-default-rtdb.asia-southeast1.firebasedatabase.app",
    #         "projectId": "cz4010project",
    #         "storageBucket": "cz4010project.appspot.com",
    #         "messagingSenderId": "292722857382",
    #         "appId": "1:292722857382:web:522e87a4bef65ff4ffab67",
    #         "measurementId": "G-PHMDGQ089W"}

    config = {"apiKey": "AIzaSyCcdNC18e2HGMLuWMWk9f78Nalkv0lM43k",
              "authDomain": "password-manager-f6d9c.firebaseapp.com",
              "databaseURL": "https://password-manager-f6d9c-default-rtdb.europe-west1.firebasedatabase.app",
              "projectId": "password-manager-f6d9c",
              "storageBucket": "password-manager-f6d9c.appspot.com",
              "messagingSenderId": "197187861509",
              "appId": "1:197187861509:web:70ae9f6dc76ad1e246306c",
              "measurementId": "G-BDP19VMP24"}
    return config


def initializeDatabaseConnection():
    '''
    initialize firebase connection
    '''
    firebase = pyrebase.initialize_app(config=getConfig())
    global db
    db = firebase.database()


def login(username, password):
    '''
    Check if user exists
    if exist decrypt vault and return session
    '''
    authHash = getAuthHash(username, password)
    dbAuthHash = str(db.child("CZ4010DB").child(
        "users").child(username).child('authHash').get().val())
    if dbAuthHash == base64.b64encode(authHash).decode():
        cipher = base64.b64decode(str(db.child("CZ4010DB").child(
            "users").child(username).child('vault').get().val()))
        lock = db.child("CZ4010DB").child("users").child(
            username).child('lock').get().val()
        clipboard = db.child("CZ4010DB").child("users").child(
            username).child('clipboard').get().val()
        key = getKey(username, password)
        vaultStrings = decryptVault(cipher, key)
        vaultDictionary = json.loads(vaultStrings)
        session = usersession(username, authHash, key, clipboard, lock)
        session.clearVault()
        session.dictionaryToVault(vaultDictionary)
        return session
    else:
        return False


def createNewAccount(username, password):
    '''
    Check if username have been used 
    if new user create a empty vault and call updatevault
    and return new session
    '''
    authHash = getAuthHash(username, password)
    snapshot = db.child("CZ4010DB").child("users").child(username)
    if str(snapshot.child('userName').get().val()) == username:
        return False
    else:
        key = getKey(username, password)
        vault = []
        session = usersession(username, authHash, key, 5000, 0, vault)
        updateVault(session)
        return session


def updateVault(session):
    '''
    Encrypt the vault and update it to google firebase
    '''
    snapshot = db.child("CZ4010DB").child("users").child(session.userName)
    vaultDict = session.vaultToDictionary()
    encryptedVault = encryptVault(json.dumps(vaultDict), session.key)
    body = {
        'userName': session.userName,
        'authHash': base64.b64encode(session.authHash).decode(),
        'clipboard': session.clipboard,
        'lock': session.lock,
        'vault': base64.b64encode(encryptedVault).decode(),
    }
    snapshot.update(body)
