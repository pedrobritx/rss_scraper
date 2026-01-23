from urllib.parse import urlparse, urlunparse

def normalize_url(url: str) -> str:
    """
    Normalize a URL to its canonical form.
    """
    try:
        parsed = urlparse(url)
        # minimal normalization: consistent scheme, lower case netloc
        return urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    except Exception:
        return url
