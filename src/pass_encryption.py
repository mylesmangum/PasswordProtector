import os
from algorithm import RSA, encrypt_RSA, decrypt_RSA
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
import bcrypt
from dotenv import load_dotenv
RSA_PRIV_KEY = 0
RSA_PUB_KEY = 0
def encryptPassword(raw_password, associated_data=b""):
    key = os.urandom(16)
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(raw_password) + encryptor.finalize()
    print(ciphertext)
    return (iv, ciphertext, encryptor.tag, key)

def decryptPassword(key, associated_data, iv, encrypted_password, tag):
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(encrypted_password) + decryptor.finalize()

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
    
iv, ciphertext, tag, key = encryptPassword("Hello", b"MySecretPassword", b"authenticated but unencrypted data")
print(decryptPassword(key, b"authenticated but unencrypted data", iv, ciphertext, tag))
load_dotenv()
print(os.getenv("DEVELOPER_PASSWORD"))