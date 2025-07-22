from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/scrape_rss')
def scrape_rss():
    """Fetch RSS/Atom links from a given URL."""
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/114.0 Safari/537.36'
        )
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return jsonify({'error': str(exc)}), 500

    soup = BeautifulSoup(resp.text, 'html.parser')
    rss_links = []
    for tag in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
        href = tag.get('href')
        if href:
            rss_links.append({
                'title': tag.get('title', ''),
                'link': urljoin(resp.url, href)
            })

    return jsonify({'rss_links': rss_links})

if __name__ == '__main__':
    app.run(debug=True)
