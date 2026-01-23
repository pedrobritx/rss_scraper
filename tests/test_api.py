import pytest
from rss_scraper import create_app
import json

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"RSS Scraper" in response.data

def test_scrape_rss_missing_url(client):
    response = client.get("/scrape_rss")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["feeds"] == []

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert b"OK" in response.data
