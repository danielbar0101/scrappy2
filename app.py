import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

scan_thread = None
stop_flag = False


def scan_website(url, keywords):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text.lower()
            keyword_matches = []
            for keyword in keywords:
                if keyword.lower() in content:
                    keyword_matches.append({"keyword": keyword, "url": url})

            pdf_files = []
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.endswith(".pdf"):
                    pdf_files.append(href)

            result = {
                "keywordMatches": keyword_matches,
                "pdfFiles": pdf_files
            }
            return jsonify(result)
    except requests.exceptions.RequestException:
        return jsonify({"message": "Error occurred during scanning."})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def start_scan():
    global scan_thread, stop_flag

    if scan_thread is not None and scan_thread.is_alive():
        return jsonify({"message": "Scan already in progress."})

    url = request.json['url']
    keywords = request.json['keywords']

    scan_thread = scan_website(url, keywords)
    return scan_thread


if __name__ == '__main__':
    app.run(debug=True)
