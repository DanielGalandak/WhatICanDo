from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

app = Flask(__name__)

def extract_article_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        headline_tag = soup.find('h1')
        headline = headline_tag.text.strip() if headline_tag else None

        date_published = soup.find('time')
        if date_published:
            date_published = date_published.text.strip()
            date_pattern = r"(\d{2}\.\s\d{2}\.\s\d{4})"
            match = re.search(date_pattern, date_published)
            if match:
                date_published = match.group(0)

        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            description = description['content']

        article_body = []
        for paragraph in soup.find_all('p'):
            article_body.append(paragraph.text.strip())

        return {
            "url": url,
            "headline": headline,
            "date_published": date_published,
            "description": description,
            "article_body": article_body
        }
    except:
        return None

def clean_article_body(text):
    if not isinstance(text, list) or not text:
        return ""
    text = "".join(text)
    text = text.strip("[]")

    match_zdroje = re.search(r"(,|\.|\?)?\s*Zdroje:", text)
    match_zdroj = re.search(r"(,|\.|\?)?\s*zdroj:", text)

    if match_zdroje or match_zdroj:
        if match_zdroje:
            text = text[:match_zdroje.start() + 1]
        else:
            text = text[:match_zdroj.start() + 1]

    return text.strip()

def get_zero_gpt_data(text):
    url = "https://api.zerogpt.com/api/detect/detectText"
    headers = {
        'ApiKey': '6a65a997-bc17-4821-9189-3b5edd96f6a1',  
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "text": text,
        "input_text": text
    })
    response = requests.post(url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    return response_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form.get('urls').splitlines()
        df = pd.DataFrame(columns=["url", "headline", "date_published", "description", "article_body"])
        results = []
        for url in urls:
            data = extract_article_data(url)
            if data:
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df['article_body'] = df['article_body'].apply(clean_article_body)
        for index, row in df.iterrows():
            article_body_str = row['article_body']
            zero_gpt_data = get_zero_gpt_data(article_body_str)
            results.append({
                "url": row['url'],
                "headline": row['headline'],
                "date_published": row['date_published'],
                "description": row['description'],
                "article_body": article_body_str,
                "zerogpt_success": zero_gpt_data.get("success", ""),
                "zerogpt_code": zero_gpt_data.get("code", ""),
                "zerogpt_message": zero_gpt_data.get("message", ""),
                "zerogpt_is_human": zero_gpt_data.get("data", {}).get("isHuman", ""),
                "zerogpt_feedback": zero_gpt_data.get("data", {}).get("feedback", ""),
                "zerogpt_detected_language": zero_gpt_data.get("data", {}).get("detected_language", ""),
                "zerogpt_additional_feedback": zero_gpt_data.get("data", {}).get("additional_feedback", ""),
            })
        return render_template('results.html', results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

