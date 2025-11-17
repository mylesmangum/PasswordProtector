from ast import literal_eval
# from encrypt_string import symEncrypt, symDecrypt
import re
import os
from dotenv import load_dotenv
from database_interface import createDatabase, createItem, searchTable
from pass_encryption import encryptPassword, decryptPassword, checkPassword, createStrongPassword

name_characters = "[^a-zA-Z0-9]"
def createAccount():
    user_name = ""
    account_name = ""
    print("We are creating account.")
    print("Please enter the user this account is for (Alphanumeric Characters Only): ")
    user_name = chooseUser()
    account_name = input("Please use alphanumeric characters only to create your account name:\n")
    scrubbed_name = re.sub(name_characters, "", account_name)
    if scrubbed_name == account_name:
        print(f"Please input a password for {scrubbed_name}'s account: ")
        raw_pass = input()
        encrypted_pass = encryptPassword(raw_pass)
        while not checkPassword(raw_pass):
            print("The password you have chosen is too common, please choose a different password.")
            raw_pass = input()
        while not createStrongPassword(raw_pass):
            raw_pass = input()
        storePasswords(user_name, scrubbed_name, encrypted_pass)
    else:
        invalidCharacter("name creation")
        createAccount()

def chooseUser(): 
    user_name = input()
    scrubbed_user_name = re.sub(name_characters, "", user_name)
    if scrubbed_user_name != user_name:
        print("Seems like you're trying to do something silly here ;) Goodbye.")
        quit()
    createDatabase(scrubbed_user_name)
    return scrubbed_user_name

def searchAccount():
    user_name = ""
    print("Please enter the user you are trying to access: ")
    user_name = chooseUser()
    password_list = searchTable(user_name)
    if password_list == []:
        print(f"It seems there's something wrong with the input of user {user_name}, please check the spelling or if there are any passwords saved for {user_name}")
        runLoop()
    for item in password_list:
        print(f"Account: {item[0]}")
        print(f"Password: {decryptPassword(item[1])}")
        print("-----"*10)



def runLoop():
    if not os.getenv("DEVELOPER_PASSWORD"):
        createMasterPassword()
    else:
        print("Enter the developer password if you are a developer, else just press enter: ")
        dev_password = input()
        if dev_password == decryptPassword(os.getenv("DEVELOPER_PASSWORD")):
            print("You are in developer mode")
            
    print("If adding a new account, please type \"ADD\"")
    print("If searching for a password, please type \"FIND\"")
    print("To exit, please type \"EXIT\"")
    action = input()
    try:
        cleanedAction = "".join(filter(str.isalnum, action)) # Maybe change this to regex?  Might be faster and I can give input if they're doing something bad
        cleanedAction = cleanedAction.upper()
    except ValueError as e:
        print(e)
        print("Please relaunch and do something normal.")
        return
    if isinstance(cleanedAction, str):
        if cleanedAction == "ADD":
            createAccount()
        elif cleanedAction == "FIND":
            searchAccount()
        elif cleanedAction == "EXIT":
            print("Goodbye!")
            quit()
        else:
            # TODO 
            # List all names of tables that are accessable.
            # Implement private public key for access of each table.
            pass
        runLoop()

def invalidCharacter(error_step):
    '''Gives error message for invalid character, argument should be text to let user know where they put the error'''
    print(f"It seems that you used an invalid character during {error_step}, please try again")

def storePasswords(user, name, password, developer_mode=False):
    # decode the byte type to be writable in a text file
    if not developer_mode:
        createItem(user, name, password)
    else:
        print("stored!")
        with open(".env", "w", encoding="utf-8") as env_file:
            env_file.write(f"DEVELOPER_PASSWORD={password}\n")        

def createMasterPassword():
    print("Please put in a master password for develper mode: ")
    raw_pass = input()
    while not checkPassword(raw_pass):
        print("The password you have chosen is too common, please choose a different password.")
        raw_pass = input()
    while not createStrongPassword(raw_pass):
        raw_pass = input()
    encrypted_pass = encryptPassword(raw_pass)
    storePasswords("developer", "master_password", encrypted_pass, developer_mode=True)

    
if __name__ == "__main__":
    load_dotenv()
    print("Welcome!  Please enter name to continue.")
    runLoop()