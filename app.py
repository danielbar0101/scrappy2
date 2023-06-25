import requests
from bs4 import BeautifulSoup
import threading
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

scan_thread = None
stop_flag = False


def scan_website(url, keywords):
    def scan_recursive(url):
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
                return result
        except requests.exceptions.RequestException:
            return None

def scan_worker():
    try:
        with app.app_context():
            result = scan_recursive(current_url)
            return jsonify(result)
    except Exception as e:
        print(f"Error occurred during scanning: {str(e)}")
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

    stop_flag = False
    scan_thread = threading.Thread(target=scan_website, args=(url, keywords))
    scan_thread.start()

    return jsonify({"message": "Scan started."})


@app.route('/stop', methods=['POST'])
def stop_scan():
    global stop_flag

    stop_flag = True
    return jsonify({"message": "Scan stopped."})


if __name__ == '__main__':
    app.run(debug=True)
