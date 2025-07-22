from flask import Flask, request, jsonify
import os

from bs4 import BeautifulSoup
import requests

from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/scrape_rss')
def scrape_rss():

    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url parameter'}), 400
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = []
        # link tags for RSS/Atom feeds
        for tag in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
            href = tag.get('href')
            if href:
                links.append({'title': tag.get('title') or href, 'link': urljoin(resp.url, href)})
        # anchor tags that look like feeds
        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'rss' in href or 'feed' in href:
                item = {'title': a.get_text(strip=True) or href, 'link': urljoin(resp.url, href)}
                if item not in links:
                    links.append(item)
        return jsonify({'rss_links': links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
