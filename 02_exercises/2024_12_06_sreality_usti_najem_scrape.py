import re
import requests
import os
import json

# Regulární výraz
regex_pattern = r'"city":\s*"([^"]+)"|"cityPart":\s*"([^"]+)"|"street":\s*"([^"]+)"|"name":\s*"([^"]+)"|"priceCzk":\s*(\d+)|"priceCzkPerSqM":\s*(\d+)'

# URL ke scrapování
url = 'https://www.sreality.cz/hledani/pronajem/byty/usti-nad-labem?stavba=cihlova&stari=tyden'

# Iterace přes všechny shody
def parse_data(matches: list) -> list:
    results = []
    temp_result = {
        "city": None,
        "cityPart": None,
        "street": None,
        "name": None,
        "priceCzk": None,
        "priceCzkPerSqM": None
    }
    for match in matches:
        if match[0]: temp_result["city"] = match[0]
        elif match[1]: temp_result["cityPart"] = match[1]
        elif match[2]: temp_result["street"] = match[2]
        elif match[3]: temp_result["name"] = match[3]
        elif match[4]: temp_result["priceCzk"] = int(match[4])
        elif match[5]: temp_result["priceCzkPerSqM"] = int(match[5])

        # Kontrola, zda je kompletní inzerát, a přidání do výsledků
        if all(temp_result.values()):
            results.append(temp_result.copy())  # Uložení kopie slovníku
            temp_result = {  # Vyprázdnění pro nový inzerát
                "city": None,
                "cityPart": None,
                "street": None,
                "name": None,
                "priceCzk": None,
                "priceCzkPerSqM": None
            }
    return results

# Funkce pro vytvoření cesty k souboru
def create_file_path() -> str:
    program_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(program_path, 'property_ads.json')

# Funkce pro uložení dat
def save_data(data: list, file_path: str):
    '''Saves scraped data into file'''
    with open(file_path, mode='a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Hlavní funkce
def main():
    # Kompilace regexu pro opakované použití
    rx_sreality = re.compile(regex_pattern)

    # Stahování obsahu webu
    response = requests.get(url)
    response.raise_for_status()  # Zajištění, že odpověď je úspěšná

    # Vyhledání shod v textu stránky
    matches = rx_sreality.findall(response.text)

    # Zpracování a uložení dat
    results = parse_data(matches)
    file_path = create_file_path()
    save_data(results, file_path)

if __name__ == '__main__':
    main()
