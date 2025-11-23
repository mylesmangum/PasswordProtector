import sqlite3

# from encrypt_string import symEncrypt
def createDatabase(user):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    new_table = f"""
                CREATE TABLE IF NOT EXISTS {user} (
                Username VARCHAR(50) NOT NULL,
                Password BLOB NOT NULL,
                IV BLOB,
                Tag BLOB
                );
                """
    connection_obj.execute(new_table)
    connection_obj.commit()
    connection_obj.close()

def createItem(user, name, password, iv, tag):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    cursor_obj = connection_obj.cursor()
    my_pass = password
    try:
        new_item = f"""
                    INSERT INTO {user} (Username, Password, IV, Tag) VALUES ("{name}", ?, ?, ?)
                    """
        cursor_obj.execute(new_item, (my_pass, iv, tag))
        print("success!")
        connection_obj.commit()
    except Exception as e:
        print("There seems to be an issue with the user you're trying to access.", e)
    finally:
        print(f"Storing {name}\'s password: {password}\n")
        connection_obj.commit()
        connection_obj.close()

def searchTable(user):
    database_name = "passwords.db"
    connection_obj = sqlite3.connect(database_name)
    cursor_obj = connection_obj.cursor()
    data_items = []
    try:
        print("Here's the data")
        connection_obj.text_factory(bytes)
        cursor_obj.execute(f"""SELECT * FROM {user}""")
        output = cursor_obj.fetchall()
        for row in output:
            data_items.append(row)
    except Exception as e:
        print("There seems to be an issue with the user you're trying to access.", e)
    finally:
        connection_obj.close()
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
        return data_items
