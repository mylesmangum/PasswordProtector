def encryptPassword(raw_password):
    # Placeholder for actual encryption logic
    return f"encrypted({raw_password})"

def decryptPassword(encrypted_password):
    # Placeholder for actual decryption logic
    if encrypted_password.startswith("encrypted(") and encrypted_password.endswith(")"):
        return encrypted_password[len("encrypted("):-1]
    return encrypted_password

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