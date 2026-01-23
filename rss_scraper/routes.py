from flask import Blueprint, request, jsonify, render_template
from rss_scraper.scraper.discover import discover_feeds
from rss_scraper.scraper.validate import validate_feed
from rss_scraper.security import is_safe_url
import time

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/scrape_rss')
def scrape_rss():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url parameter', 'feeds': []}), 400
    
    start_time = time.time()
    errors = []
    feeds = []
    
    try:
        # The discover_feeds function currently returns simple dicts, 
        # we will adapt them to the new schema here or update discover.py later.
        # For now, let's keep it compatible but wrap in the new response structure
        raw_links = discover_feeds(url)
        
        for link in raw_links:
            # Validate each discovered link to get real type and status
            val_res = validate_feed(link['link'])
            
            feeds.append({
                "url": link['link'],
                "title": link['title'],
                "type": val_res['type'], 
                "source": "discovered", # This could be refined if we tracked source in discover.py
                "status": val_res['status'],
                "error": val_res['error']
            })
            
    except ValueError as e:
         return jsonify({'error': str(e), 'feeds': []}), 400
    except Exception as e:
        errors.append(str(e))
        return jsonify({'error': str(e), 'feeds': [], 'errors': errors}), 500

    scan_ms = int((time.time() - start_time) * 1000)
    
    # Legacy compatibility: return rss_links field if frontend expects it, 
    # but our plan says we update frontend. We will stick to new schema.
    # New schema: { feeds: [], errors: [], scan_ms: ... }
    
    return jsonify({
        'feeds': feeds,
        'errors': errors,
        'scan_ms': scan_ms,
        # Keep legacy field briefly if needed or just switch frontend immediately.
        # Plan says "Frontend cleanup" next, so we can break it now.
        'rss_links': raw_links # Optional fallback
    })
