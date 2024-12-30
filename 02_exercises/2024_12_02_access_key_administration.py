# 2024_12_02_access_key_administration.py

'''
Příklad 3: Správa přístupových klíčů
Napište program, který:

Načte soubor keys.json, kde jsou uloženy veřejné přístupové klíče a jejich popis.
Umožní přidat nový klíč (klíč bude hashován pomocí sha256 a uložen do souboru spolu s popisem).
Umožní vyhledávat klíče podle hashe a vrátit jejich popis.
Umožní exportovat seznam klíčů a jejich hashů do nového souboru ve formátu JSON.
'''

{
    "keys": [
        {
            "hash": "a7b91cbde5c07b183deac1d5e6d1d94a7b84d00d8b4ab19219e2ed7a9c6d405e",
            "description": "Admin access key"
        },
        {
            "hash": "a710b9b06aa3e5f647b1d8eb7c912c62db2520f91b5b92f51feca5df80c658d2",
            "description": "User access key for limited permissions"
        }
    ]
}


import json
import os
import hashlib


PATH = r'access_key_administration.json'

def read_data(PATH):
    try:

        with open(PATH, encoding='utf-8') as file:
            return json.load(file)
        
    except:
        not os.path.exists(PATH)
        return {"keys": []}
    
def save_data(dictionary):
    with open(PATH, mode='w', encoding='utf-8') as file:
        json.dump(dictionary, file)

def hash_entry(user_input):
    hash_value = hashlib.sha256(user_input.encode())
    return hash_value.hexdigest()

def data_entry():
    word_to_hash = input('Enter word to be hashed: ')
    explanatory_note = input('Enter a description of a hash: ')

    return word_to_hash, explanatory_note

def export_to_new_file():
    '''
    Creates a path for a new copy of a data
    Args: 
    Returns: str. new_file_path
    '''
    try:

        new_file_name = input('Enter the name of a new .json file:\n')
        if not new_file_name.endswith('.json'):
            new_file_name += '.json'
        program_path = os.path.dirname(os.path.abspath(__file__))
        new_file_path = os.path.join(program_path, new_file_name)
        return True, new_file_path
    
    except FileNotFoundError:
        return False, 'Probably wrong symbols for a file name used, or something else went wrong..'



def find_by_hashkey(hash_entry, data):
    '''
    Searches a hash in a database
    Args: dictionary, data loaded from json file
    Returns: dictionary if the hash is found in database and string if not
    '''
    
    for record in data['keys']:
        if record.get('hash') == hash_entry:
            return True, record

    else:
        return False, 'hash is not in the database'
    
def main():
    """Main program loop"""
    while True:
        action = input(
            'Choose an action:\n'
            '| New record: "n" |\n'
            '| Search a word in database: "s" |\n'
            '| Export data into new file: "e" |\n'
            '| Quit: "q" |\n'
            )
        
        if action == 'n':
            data = read_data(PATH)
            word_to_hash, explanatory_note = data_entry()
            hash_value = hash_entry(word_to_hash)
            new_record = {}
            new_record.update({
                "hash": hash_value, 
                "description": explanatory_note
            })
            data['keys'].append(new_record)
            save_data(data)


        if action == 's':
            data = read_data(PATH)
            word_to_hash = input('Enter word to be hashed: ')
            hash_value = hash_entry(word_to_hash)
            result, record = find_by_hashkey(hash_value, data)
            if result == True:
                print(record)
            else:
                print(record)


        if action == 'e':
            data = read_data(PATH)
            success, value = export_to_new_file()
            if success == True:
                print(f'{value}')
                with open(value, mode='w', encoding='utf-8') as file:
                    json.dump(data, file)
            else:
                print(value)
            

        if action == 'q':
            break

        else:
            print("Invalid action. Please choose 'n', 's', 'e', or 'q'.")


if __name__ == '__main__':
    main()
