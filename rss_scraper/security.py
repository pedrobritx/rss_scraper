import ipaddress
import socket
from urllib.parse import urlparse

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
