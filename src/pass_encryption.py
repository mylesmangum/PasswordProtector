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

def createStrongPassword(length=12):
    return "soStrong!!!!"