import os
from algorithm import RSA, encrypt_RSA, decrypt_RSA
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from dotenv import load_dotenv
RSA_PRIV_KEY = 0
RSA_PUB_KEY = 0
key = b'2^\x9eb}\t\x13\xab,_\xd4\xfa\x0c)]\x95'
def encryptPassword(raw_password, associated_data=b""):
    # Initialization vector should be unique per encryption,
    # but it does not need to be secret.
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
    return (iv, ciphertext, encryptor.tag)

def decryptPassword(associated_data, iv, encrypted_password, tag):
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
        return False
    else:
        return True
    
# iv, ciphertext, tag = encryptPassword(b"mysecretpassword", b"authenticated but unencrypted data")
# print("Ciphertext:", ciphertext)
# print("Tag:", tag)
# iv = b'\x0eAT!\xadg\xdc\xa6K\xd9\xa7T'
# associated_data = b''
# tag = b'\xf0*\xc9r`\x9e\xee\x8b\xfd\xcf\x1d\xaddl\xfa\xcb'
# plaintext = decryptPassword(associated_data, iv, b'\\x146\\xecB\\x8b\\x02\\xd1_', tag)
# print("Plaintext:", plaintext)