import pytest
from unittest.mock import patch, MagicMock
from rss_scraper.scraper.validate import validate_feed

def test_validate_feed_rss():
    with patch('requests.get') as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {'Content-Type': 'application/rss+xml'}
        mock_resp.iter_content.return_value = [b'<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>']
        mock_get.return_value = mock_resp

        result = validate_feed("http://example.com/rss")
        assert result['status'] == 'valid'
        assert result['type'] == 'rss'
        assert result['error'] is None

def test_validate_feed_atom():
    with patch('requests.get') as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {'Content-Type': 'application/atom+xml'}
        mock_resp.iter_content.return_value = [b'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"></feed>']
        mock_get.return_value = mock_resp

        result = validate_feed("http://example.com/atom")
        assert result['status'] == 'valid'
        assert result['type'] == 'atom'
        assert result['error'] is None

def test_validate_feed_invalid_content():
    with patch('requests.get') as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {'Content-Type': 'text/html'}
        mock_resp.iter_content.return_value = [b'<html><body>Not a feed</body></html>']
        mock_get.return_value = mock_resp

        result = validate_feed("http://example.com/page")
        assert result['status'] == 'invalid'
        assert result['type'] == 'unknown'
        assert result['error'] is not None

def test_validate_feed_404():
    with patch('requests.get') as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        result = validate_feed("http://example.com/404")
        assert result['status'] == 'error'
        assert "404" in result['error']

def test_validate_feed_exception():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")

        result = validate_feed("http://example.com/error")
        assert result['status'] == 'error'
        assert "Connection error" in result['error']
