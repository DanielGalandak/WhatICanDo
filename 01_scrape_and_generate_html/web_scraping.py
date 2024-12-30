# web_scraping.py

import re
import requests
import json

# toto je vytvořené v https://pythex.org/ a definuje to část html, kterou chceme scapovat
pattern = r'<div class="inzeratynadpis"><a href="(.*?)">\s*<img src="(.*?)" class="obrazek" alt="(.*?)"'

rx_bazos = re.compile(pattern) # vytvoří optimalizovanou verzi regulárního výrazu, vytvoří to objekt regulárního výrazu

# url na stránku, z níž stáhneme celé html
url = 'https://mobil.bazos.cz/'

# vrací odpověď v níž je cele html
response = requests.get(url)

# pomocí findall a definovaného patternu vytáhne konkrétní části html a uloží je do proměnné result
result = rx_bazos.findall(response.text)

data = []

for url, img, title in result:
    item = {'url': url, 'img': img, 'title': title}
    data.append(item)

PATH = r'web_scraping.json'

with open(PATH, mode='w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)








