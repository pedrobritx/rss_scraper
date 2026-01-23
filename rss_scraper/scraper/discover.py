import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
from rss_scraper.security import is_safe_url
from rss_scraper.scraper.validate import validate_feed

def extract_feed_links(soup: BeautifulSoup, base: str) -> List[Dict[str, str]]:
    """Return a list of feed links discovered in the given page."""
    results: List[Dict[str, str]] = []
    seen: Set[str] = set()

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

def discover_feeds(url: str) -> List[Dict[str, str]]:
    """
    Main discovery logic:
    1. Fetch URL
    2. Parse HTML
    3. Extract links
    4. Heuristic fallback
    """
    try:
        if not is_safe_url(url):
            raise ValueError("Invalid or unsafe URL")

        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 RSS-Scraper/1.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        base_url = resp.url
        links = extract_feed_links(soup, base_url)
        
        # Heuristic fallback if no links found
        if not links:
            parsed = urlparse(base_url)
            root = f"{parsed.scheme}://{parsed.netloc}"
            patterns = [
                'feed', 'feed/', 'rss', 'rss.xml', 'atom.xml',
                'feed.xml', 'index.xml', 'feeds/posts/default?alt=rss'
            ]
            for p in patterns:
                guess = urljoin(root + '/', p)
                # Check duplication
                if any(link['link'] == guess for link in links):
                    continue
                if not is_safe_url(guess):
                    continue
                
                res = validate_feed(guess)
                if res['status'] == 'valid':
                    links.append({'title': p, 'link': guess})
        
        return links
    except Exception as e:
        # Re-raise so caller can handle
        raise e
