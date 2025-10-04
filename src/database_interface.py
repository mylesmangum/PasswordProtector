import sqlite3
# from encrypt_string import symEncrypt
def createDatabase(user):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    new_table = f"""
                CREATE TABLE IF NOT EXISTS {user} (
                Username VARCHAR(50) NOT NULL,
                Password VARCHAR(255) NOT NULL
                );
                """
    connection_obj.execute(new_table)
    connection_obj.commit()
    connection_obj.close()

def createItem(user, name, password):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    cursor_obj = connection_obj.cursor()
    my_pass = password
    try:
        new_item = f"""
                    INSERT INTO {user} (Username, Password) VALUES ("{name}", "{my_pass}")
                    """
        cursor_obj.execute(new_item)
        print("success!")
        connection_obj.commit()
    except:
        print("There seems to be an issue with the user you're trying to access.")
    finally:
        print(f"Storing {name}\'s password: {password}")
        connection_obj.commit()
        connection_obj.close()

def searchTable(user):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    cursor_obj = connection_obj.cursor()
    data_items = []
    try:
        print("Here's the data")
        cursor_obj.execute(f"""SELECT * FROM {user}""")
        output = cursor_obj.fetchall()
        for row in output:
            data_items.append(row)
    except:
        print("There seems to be an issue with the user you're trying to access.")
    finally:
        connection_obj.close()
        print(data_items)
        return data_items


def searchAccounts(user):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    cursor_obj = connection_obj.cursor()
    data_items = []
    try:
        print("Here's the data")
        cursor_obj.execute(f"""SELECT * FROM {user}""")
        output = cursor_obj.fetchall()
        for row in output:
            data_items.append(row[0])
    except Exception as e:
        print(e)
    finally:
        connection_obj.close()
        print(data_items)
        return data_items
