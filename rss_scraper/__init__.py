from flask import Flask
from flask_cors import CORS
import os

def create_app(test_config=None):
    # Initialize app with correct template/static folders
    # logical structure: rss_scraper package (this file is here) -> templates is sibling? 
    # Current structure on disk: rss_scraper/rss_scraper/__init__.py
    # Templates are at rss_scraper/rss_scraper/templates (because we moved them to rss_scraper/templates which is inside the inner rss_scraper package?)
    # Wait, my rename command was:
    # mkdir -p rss_scraper/templates
    # mv index.html rss_scraper/templates/
    # So `rss_scraper/templates` exists.
    # The package is `rss_scraper`.
    # So the structure is:
    # root/
    #   rss_scraper/ (package dir)
    #     __init__.py
    #     routes.py
    #     templates/
    #     static/
    
    app = Flask(__name__, instance_relative_config=True) # defaults template_folder='templates', static_folder='static' relative to module
    CORS(app)

    @app.route('/health')
    def health():
        return 'OK'

    from . import routes
    app.register_blueprint(routes.bp)

    return app
