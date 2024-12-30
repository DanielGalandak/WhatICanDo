import os
import json

# Základní cesty
program_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(program_path, "project_list.json")
project_dir_path = os.path.join(program_path, "projects")

# Vytvoření složky pro projekty, pokud neexistuje
if not os.path.exists(project_dir_path):
    os.makedirs(project_dir_path)

def pridat_projekt(new_project_name):
    """
    Funkce pro přidání nového projektu do seznamu a vytvoření souboru JSON pro tento projekt.
    Args:
        new_project_name (str): Název nového projektu.
    Returns:
        Tuple[str, str]: Cesta k souboru projektu a název projektu.
    """
    # Cesta k souboru projektu
    project_file_path = os.path.join(project_dir_path, new_project_name + ".json")
    
    # Načtení existujícího seznamu projektů, pokud existuje
    if os.path.exists(file_path):
        with open(file_path, "r") as jsonfile:
            project_list = json.load(jsonfile)
    else:
        project_list = {}
    
    # Přidání nebo aktualizace projektu v seznamu
    project_list[new_project_name] = project_file_path

    # Uložení aktualizovaného seznamu projektů
    with open(file_path, "w") as jsonfile:
        json.dump(project_list, jsonfile, indent=4)

    # Vytvoření prázdného souboru JSON pro nový projekt, pokud neexistuje
    if not os.path.exists(project_file_path):
        with open(project_file_path, "w") as jsonfile:
            json.dump({}, jsonfile, indent=4)

    return project_file_path, new_project_name
