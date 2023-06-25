import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    url = data['url']
    keywords = data['keywords']

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})

    html_content = response.text
    keyword_matches = []
    pdf_files = []

    # Scan for keywords
    for keyword in keywords:
        matches = re.finditer(keyword, html_content, re.IGNORECASE)
        for match in matches:
            keyword_matches.append({'keyword': keyword, 'url': url})

    # Find PDF files
    pdf_urls = re.findall(r'href=[\'"]?([^\'" >]+\.pdf)', html_content, re.IGNORECASE)
    for pdf_url in pdf_urls:
        if not pdf_url.startswith('http'):
            pdf_url = url + pdf_url if not url.endswith('/') else url[:-1] + pdf_url
        pdf_files.append(pdf_url)

    return jsonify({'keywordMatches': keyword_matches, 'pdfFiles': pdf_files})

if __name__ == '__main__':
    app.run()
