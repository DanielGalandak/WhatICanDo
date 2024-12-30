

def nacti_json_soubor(file_path):
    """
    Načte cestu k databázi ve formátu JSON.
    Args:
    - file_path - cesta k databázi
    Returns:
    - dict/list/None: Načtená data ve formě slovníku nebo seznamu, nebo None pokud dojde k chybě.
    """
    import json
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None    
    
def uloz_json_soubor(file_path, new_data):
    import json
    try:
        # Načtení existujících dat
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
            if not isinstance(data, list):  # Kontrola, zda načtená data jsou seznam
                data = []
        except (FileNotFoundError, json.JSONDecodeError):  # Soubor neexistuje nebo je prázdný
            data = []

        # Přidání nového záznamu do seznamu
        data.append(new_data)

        # Uložení upravených dat zpět do souboru
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        return str(e)  # Vrací popis chyby, pokud dojde k nějaké při zápisu

