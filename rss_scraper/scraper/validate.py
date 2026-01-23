import requests
import re
from typing import Dict, Any

def validate_feed(url: str) -> Dict[str, Any]:
    """
    Validates if a URL points to a valid RSS or Atom feed.
    """
    try:
        # Stream the request to avoid downloading large files if it's not a feed
        resp = requests.get(url, stream=True, timeout=10, headers={'User-Agent': 'Mozilla/5.0 RSS-Scraper/1.0'})
        
        # Check status code first
        if resp.status_code != 200:
             return {"status": "error", "error": f"HTTP {resp.status_code}", "type": "unknown"}

        # Check Content-Type header
        content_type = resp.headers.get('Content-Type', '').lower()
        
        # Read a chunk of the content to check for signatures
        # We only need the beginning of the file to identify xml/rss/atom
        chunk = ''
        for data in resp.iter_content(chunk_size=1024):
            chunk += data.decode('utf-8', errors='ignore')
            if len(chunk) > 2048: # Check first 2KB should be enough
                break
        
        chunk_lower = chunk.lower()
        
        feed_type = "unknown"
        is_valid = False

        if "application/rss+xml" in content_type or \
           "application/atom+xml" in content_type or \
           "text/xml" in content_type or \
           "application/xml" in content_type:
            # high confidence from header, but let's verify content
            pass
        
        if "<rss" in chunk_lower or "<rdf:rdf" in chunk_lower:
             feed_type = "rss"
             is_valid = True
        elif "<feed" in chunk_lower:
             feed_type = "atom"
             is_valid = True
        elif "xml" in content_type:
             # Fallback if header says XML but we didn't match root tag yet (maybe comment or doctype first)
             # Regex for a more loose check if needed, but let's stick to root elements for now
             if re.search(r"<(rss|feed|rdf:RDF)", chunk, re.I):
                  if "rss" in chunk_lower or "rdf" in chunk_lower:
                       feed_type = "rss"
                  else:
                       feed_type = "atom"
                  is_valid = True

        if is_valid:
             return {"status": "valid", "type": feed_type, "error": None}
        else:
             return {"status": "invalid", "type": "unknown", "error": "Does not appear to be a valid RSS/Atom feed"}

    except Exception as e:
        return {"status": "error", "error": str(e), "type": "unknown"}
