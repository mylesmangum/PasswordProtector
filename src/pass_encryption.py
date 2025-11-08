import os
from algorithm import RSA, encrypt_RSA, decrypt_RSA
RSA_PRIV_KEY = 0
RSA_PUB_KEY = 0
def encryptPassword(raw_password):
    try:
        privKey = os.environ["RSA_PRIV_KEY"]
        pubKey = os.environ["RSA_PUB_KEY"]
    except:
        print("Building new keys...")
        RSA_PUB_KEY, RSA_PRIV_KEY = RSA(23, 41)
        os.environ["RSA_PRIV_KEY"] = str(RSA_PRIV_KEY)
        os.environ["RSA_PUB_KEY"] = str(RSA_PUB_KEY)
    raw_password = encrypt_RSA(raw_password, RSA_PUB_KEY[0], RSA_PUB_KEY[1])
    # Placeholder for actual encryption logic
    return raw_password

def decryptPassword(encrypted_password):
    # Placeholder for actual decryption logic
    RSA_PUB_KEY, RSA_PRIV_KEY = RSA(23, 41)
    decrypted = decrypt_RSA(list(encrypted_password), RSA_PRIV_KEY[0], RSA_PRIV_KEY[1])
    return decrypted

def checkPassword(raw_password):
    if raw_password == "password123":
        return False
    return True

def createStrongPassword(password):
    hasSpecialCharacter = False
    for char in password:
        if not (char.isdigit() or char.isalnum()):
            hasSpecialCharacter = True
            break

    if not any(char.isdigit() for char in password):
        print("It's recommended you have at least one number in your password")
        return False
    elif len(password) <= 7:
        print("It's recommended you have a password greater than 7 characters")
        return False
    elif not hasSpecialCharacter:
        print("It's recommended you have at least one special character in your password")
    else:
        return True