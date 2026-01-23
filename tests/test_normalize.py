from rss_scraper.scraper.normalize import normalize_url

def test_normalize_simple():
    url = "HTTP://Example.COM/Foo"
    assert normalize_url(url) == "http://example.com/Foo"

def test_normalize_query():
    url = "https://example.com/feed?a=1&b=2"
    assert normalize_url(url) == "https://example.com/feed?a=1&b=2"
