from ast import literal_eval
# from encrypt_string import symEncrypt, symDecrypt
import re
import os
import sys
import readline
from dotenv import load_dotenv
from argon2 import PasswordHasher
from database_interface import createDatabase, createItem, searchTable
from pass_encryption import encryptPassword, decryptPassword, checkPassword, createStrongPassword, suggestPassword
iv = b'6\xc3"\x15\xd8\x16\x80H\xb7\xd6K!'
associated_data = b''
tag = b'\xaa\xa0\x85\xce\xd5[O\xf2\x14m\x8fO\x19\n\x9c\x0b'
placeholder = b'\xa02\xbd\x12>\xe3\x92\xe5'
name_characters = "[^a-zA-Z0-9]"

def input_with_prefill(message, prefill):
    def hook():
        readline.insert_text(prefill)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    try:
        return input(message)
    finally:
        readline.set_pre_input_hook()

def createAccount():
    user_name = ""
    account_name = ""
    print("We are creating account.")
    print("Please enter the user this account is for (Alphanumeric Characters Only): ")
    user_name = chooseUser()
    account_name = input("Please use alphanumeric characters only to create your account name:\n")
    scrubbed_name = re.sub(name_characters, "", account_name)
    if scrubbed_name == account_name:
        print("Would you like a generated password? (y/n):")
        gen_option= input()
        generated_password = ""
        if gen_option.lower() == 'y':
            generated_password = suggestPassword()
        print(f"Please input a password for {scrubbed_name}'s account: ")
        raw_pass = input_with_prefill("", generated_password)
        while not checkPassword(raw_pass):
            raw_pass = input_with_prefill("", raw_pass)
        while not createStrongPassword(raw_pass):
            raw_pass = input_with_prefill("", raw_pass)
        iv, encrypted_pass, tag = encryptPassword(raw_pass.encode('utf-8'), associated_data)
        storePasswords(user_name, scrubbed_name, encrypted_pass, iv, tag)
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
        runLoop("developer")
    for item in password_list:
        print(f"Account: {item[0]}")
        print(f"encrypted Password: {item[1]}")
        print(f"Password: {decryptPassword(associated_data, item[2], item[1], item[3])}")
        print("-----"*10)



def runLoop(mode):
    print("If adding a new account, please type \"ADD\"")
    print("If searching for a password, please type \"FIND\" (only for developers)")
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
            if mode != "developer":
                print("You are not a developer.\n")
                runLoop(mode)
                return
            searchAccount()
        elif cleanedAction == "EXIT":
            print("Goodbye!")
            sys.exit()
        else:
            # TODO 
            # List all names of tables that are accessable.
            # Implement private public key for access of each table.
            pass
        runLoop(mode)

def invalidCharacter(error_step):
    '''Gives error message for invalid character, argument should be text to let user know where they put the error'''
    print(f"It seems that you used an invalid character during {error_step}, please try again")

def storePasswords(user, name, password, iv="", tag="", developer_mode=False):
    # decode the byte type to be writable in a text file
    if not developer_mode:
        createItem(user, name, password, iv, tag)
    else:
        print("stored!")
        with open(".env", "w", encoding="utf-8") as env_file:
            env_file.write(f"DEVELOPER_PASSWORD={password}\n")        

def createMasterPassword():
    print("Please create a master password for developer mode: ")
    raw_pass = input()
    while not checkPassword(raw_pass):
        print("The password you have chosen is too common, please choose a different password.")
        raw_pass = input_with_prefill("", raw_pass)
    while not createStrongPassword(raw_pass):
        raw_pass = input_with_prefill("", raw_pass)
    encrypted_pass = PasswordHasher().hash(raw_pass)
    storePasswords("developer", "master_password", encrypted_pass, developer_mode=True)

    
if __name__ == "__main__":
    load_dotenv()
    mode = "user"
    if not os.getenv("DEVELOPER_PASSWORD"):
        createMasterPassword()
    else:
        print("Enter the developer password if you are a developer, else just press enter: ")
        try:
            dev_password = input()
            hashed_password = os.getenv("DEVELOPER_PASSWORD")
            PasswordHasher().verify(hashed_password, dev_password)
            print("Do you want to reset the password? (y/n): ")
            reset_choice = input().lower()
            if reset_choice == 'y':
                createMasterPassword()
            print("You are in developer mode")
            mode = "developer"
        except Exception as e:
            print("Password incorrect... Continuing in user mode.")
    print("Welcome!\n")
    runLoop(mode)