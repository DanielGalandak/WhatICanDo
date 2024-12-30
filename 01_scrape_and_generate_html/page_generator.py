# page_generator_3.py

import json

json_path = r'web_scraping.json'
html_path = r'09_list.html '
tag_pattern = '<a href="{url}"><h2>{title}</h2><img src="{img}" alt="{title}"></a>'
replace_mark = '<!-- HTML -->'

def read_json(path: str) -> list:
    with open(json_path, encoding='utf-8') as file:
        return json.load(file)

def read_html(path: str) -> str:
    with open(html_path, encoding='utf-8') as file:
        return file.read()

def parse_data(template: str, data) -> str:
    indentation = '\n' + ' ' * 8
    return indentation.join(tag_pattern.format(**item) for item in data)
                                            # '**item' - rozbalí slovník item na pojmenované argumenty
    
def insert_content(content: str, html_string: str, replace_mark: str) -> str:
    return html_string.replace(replace_mark, content)

def save_html(path: str, data: str):
    with open(path, mode='w', encoding='utf-8') as file:
        file.write(data)

def main():
    data = read_json(json_path)
    html_string = read_html(html_path)
    content = parse_data(tag_pattern, data)
    new_html = insert_content(content, html_string, replace_mark)
    save_html(html_path, new_html)

if __name__ == '__main__':
    main()
