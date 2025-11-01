from ast import literal_eval
# from encrypt_string import symEncrypt, symDecrypt
import re
from database_interface import createDatabase, createItem, searchTable
from pass_encryption import encryptPassword, decryptPassword, checkPassword

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
        if(not checkPassword(raw_pass)):
            print("The password you have chosen is too common, please choose a different password.")
            createAccount()
            return
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
        print(f"Password: {item[1]}")
        print("-----"*10)



def runLoop():
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

def storePasswords(user, name, password):
    # decode the byte type to be writable in a text file
    createItem(user, name, password)
    
if __name__ == "__main__":
    print("Welcome!  Please enter name to continue.")
    runLoop()