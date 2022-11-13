import string
from hashlib import pbkdf2_hmac

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random

def getKey(userName, masterPassword):
    '''
    Return key for encryption or decryption using 200000 rounds of PBKDF2-SHA512
    '''
    key = pbkdf2_hmac('sha512', masterPassword.encode(), userName.encode(), 200000, 32)
    return key
    
def getAuthHash(userName, masterPassword):
    '''
    Return authentication hash with one round of hashing of key
    '''
    authHash = pbkdf2_hmac('sha512', getKey(userName, masterPassword), masterPassword.encode(), 1, 32)
    return authHash

def generateIV():
    '''
    Returns 16 bytes of initialization vetor for AES CBC    
    '''
    IV = get_random_bytes(16)
    return IV
def encryptVault(vaultString, key):
    '''
    Return an encrypted vault using AES-256 CBC
    '''
    data = addPad(vaultString)
    iv = generateIV()
    aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = aes.encrypt(str.encode(data))
    return iv + encrypted

def decryptVault(cipherText, key):
    '''
    Return an decrypted vault using AES-256 CBC
    '''
    iv = cipherText[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unPad(aes.decrypt(cipherText[16:])).decode('utf-8')


def addPad(st):
    '''
    Return a padded string
    '''
    Pad = st + (32 - len(st) % 32) * chr(32 - len(st) % 32)
    return Pad

def unPad(st):
    '''
    Return a unpadded string
    '''
    Pad = st[:-ord(st[len(st)-1:])]
    return Pad

def generatePassword(length, passwordOptions=[]):
    '''
    Return a random generated password according to users specification
    length is generated password length
    passwordOption is a String list for example ['Number',Symbols]
    '''
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = '~!@#$%^&*()_+}{[]'
    password = list()

    for i in range(length):
        password.append(random.choice(lowercase))

    if 'upper' in passwordOptions:
        numToReplace = int(length/5) + 1
        for i in range(numToReplace):
            replaceIndex = random.randint(0, length-1)
            password[replaceIndex] = random.choice(uppercase)

    if 'digits' in passwordOptions:
        numToReplace = int(length/5) + 1
        for i in range(numToReplace):
            replaceIndex = random.randint(0, length-1)
            password[replaceIndex] = random.choice(numbers)

    if 'symbols' in passwordOptions:
        numToReplace = int(length/6) + 1
        for i in range(numToReplace):
            replaceIndex = random.randint(0, length-1)
            password[replaceIndex] = random.choice(symbols)
    
    return ''.join(password)
