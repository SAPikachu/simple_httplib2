from .HttpSession import HttpSession
from urllib.parse import urlparse, urlunparse

def request(url, method_name, debug=False, session_kwargs=None, **kwargs):
    session_kwargs = session_kwargs or {}
    parsed = urlparse(url)
    host = urlunparse(parsed[:2] + ('', '', '', ''))
    session = HttpSession(host, **session_kwargs)
    session.debug = debug

    path = urlunparse(('', '') + parsed[2:])
    return getattr(session, method_name)(path, **kwargs)

def get(url, **kwargs):
    return request(url, "get", **kwargs)

def post(url, body, **kwargs):
    return request(url, "post", body=body, **kwargs)

def post_multipart(url, body, **kwargs):
    return request(url, "post_multipart", body=body, **kwargs)

