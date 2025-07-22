from flask import Flask, request, jsonify
import os

from bs4 import BeautifulSoup
import requests

from urllib.parse import urljoin, urlparse
import ipaddress
import socket

app = Flask(__name__)


def is_safe_url(url: str) -> bool:
    """Basic SSRF protection by validating scheme and host."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        try:
            ip = ipaddress.ip_address(hostname)
        except ValueError:
            try:
                ip = ipaddress.ip_address(socket.gethostbyname(hostname))
            except Exception:
                return False

        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
            return False

        return True
    except Exception:
        return False

@app.route('/scrape_rss')
def scrape_rss():

    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url parameter'}), 400
    if not is_safe_url(url):
        return jsonify({'error': 'invalid or unsafe url'}), 400
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
