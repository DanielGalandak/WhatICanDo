import json
import hashlib
import os

PATH = r'user_authentization.json'

# Načtení dat ze souboru
def read_data(PATH):
    if not os.path.exists(PATH):
        # Pokud soubor neexistuje, vytvoříme výchozí strukturu
        return {"users": {}}
    with open(PATH, encoding='utf-8') as file:
        return json.load(file)

# Uložení dat do souboru
def save_data(dictionary, PATH):
    with open(PATH, mode='w', encoding='utf-8') as file:
        json.dump(dictionary, file, indent=4)

# Registrace nového uživatele
def registration():
    username = input('Insert username: ')
    while True:
        password = input('Insert password: ')
        password_repeat = input('Repeat the inserted password: ')
        if password == password_repeat:
            break
        else:
            print('Inserted passwords do not match.')
    return username, password

# Hashování hesla
def password_hash(password):
    hash_value = hashlib.sha256(password.encode())
    return hash_value.hexdigest()

# Přihlášení uživatele
def login():
    username_insert = input('Insert username: ')
    password_insert = input('Insert password: ')
    return username_insert, password_insert

# Hlavní program
def main():
    while True:
        action = input('Choose action: \n|Registration: insert "r"|\n|Login: insert "l"|\n|Exit: insert "e"|\n')
        if action == 'e':
            break
        elif action == 'r':
            users = read_data(PATH)
            
            # Zajištění existence klíče "users"
            if "users" not in users:
                users["users"] = {}
            
            username, password = registration()
            hashed_password = password_hash(password)
            
            if username in users["users"]:
                print('This username already exists. Please choose another one.')
            else:
                users["users"][username] = hashed_password
                save_data(users, PATH)
                print('Registration successful.')
        elif action == 'l':
            users = read_data(PATH)
            
            if "users" not in users:
                print("No users registered yet.")
                continue
            
            username, password = login()
            hashed_password = password_hash(password)

            if username in users["users"] and users["users"][username] == hashed_password:
                print('Successfully logged in.')
            else:
                print('Invalid username or password.')
        else:
            print('Invalid action choice.')

if __name__ == '__main__':
    main()
