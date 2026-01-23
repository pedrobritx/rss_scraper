import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from rss_scraper.scraper.discover import extract_feed_links, discover_feeds

def test_extract_feed_links_rss():
    html = """
    <html>
        <head>
            <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="RSS Feed">
        </head>
        <body></body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    base = "http://example.com"
    links = extract_feed_links(soup, base)
    assert len(links) == 1
    assert links[0]["link"] == "http://example.com/feed.xml"
    assert links[0]["title"] == "RSS Feed"

def test_extract_feed_links_anchor_tag():
    html = """
    <html>
        <body>
            <a href="/rss">RSS Feed</a>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    base = "http://example.com"
    links = extract_feed_links(soup, base)
    assert len(links) == 1
    assert links[0]["link"] == "http://example.com/rss"

@patch("rss_scraper.scraper.discover.requests.get")
@patch("rss_scraper.scraper.discover.is_safe_url")
def test_discover_feeds_success(mock_is_safe, mock_get):
    mock_is_safe.return_value = True
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.url = "http://example.com"
    mock_response.content = b"""
    <html>
        <head>
            <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="RSS Feed">
        </head>
    </html>
    """
    mock_get.return_value = mock_response
    
    links = discover_feeds("http://example.com")
    assert len(links) == 1
    assert links[0]["link"] == "http://example.com/feed.xml"
