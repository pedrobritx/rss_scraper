from flask import Flask, request, jsonify
from flask_cors import CORS


from bs4 import BeautifulSoup
import requests

from urllib.parse import urljoin, urlparse
import ipaddress
import socket
import os
import re

from typing import List, Dict

app = Flask(__name__)
CORS(app)


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


def extract_feed_links(soup: BeautifulSoup, base: str) -> List[Dict[str, str]]:
    """Return a list of feed links discovered in the given page."""
    results: List[Dict[str, str]] = []
    seen = set()

    rss_type_re = re.compile(r"(?:application|text)/(?:rss|atom)(?:\+xml)?|xml", re.I)

    for tag in soup.find_all("link", href=True):
        href = tag["href"]
        type_attr = tag.get("type", "")
        rels = " ".join(tag.get("rel", [])) if tag.get("rel") else ""

        if rss_type_re.search(type_attr) or (
            "alternate" in rels.lower() and re.search(r"(rss|atom|feed)", href, re.I)
        ):
            url = urljoin(base, href)
            if url not in seen:
                results.append({"title": tag.get("title") or href, "link": url})
                seen.add(url)

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.search(r"(rss|atom|feed)", href, re.I):
            url = urljoin(base, href)
            if url not in seen:
                results.append({"title": a.get_text(strip=True) or href, "link": url})
                seen.add(url)

    return results

@app.route('/scrape_rss')
def scrape_rss():

    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url parameter'}), 400
    if not is_safe_url(url):
        return jsonify({'error': 'invalid or unsafe url'}), 400
    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')

        base = resp.url
        links = extract_feed_links(soup, base)

        # try common feed URL patterns if nothing found
        if not links:
            parsed = urlparse(resp.url)
            base_root = f"{parsed.scheme}://{parsed.netloc}"
            patterns = [
                "feed",
                "feed/",
                "rss",
                "rss.xml",
                "atom.xml",
                "feed.xml",
                "index.xml",
                "feeds/posts/default?alt=rss",
            ]

            existing = {l["link"] for l in links}

            for p in patterns:
                guess = urljoin(base_root + "/", p)
                if guess in existing:
                    continue
                if not is_safe_url(guess):
                    continue
                try:
                    r = requests.get(
                        guess,
                        timeout=5,
                        headers={"User-Agent": "Mozilla/5.0"},
                    )
                    if r.status_code == 200 and (
                        "xml" in r.headers.get("Content-Type", "").lower()
                        or re.search(r"<(rss|feed)", r.text, re.I)
                    ):
                        links.append({"title": p, "link": guess})
                        existing.add(guess)
                except Exception:
                    pass

        return jsonify({'rss_links': links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
