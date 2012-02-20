import httplib2
from urllib.parse import urlencode, urlparse, urlunparse, ParseResult
from http.cookies import SimpleCookie
from .data_handler import handle_data
from .multipart import encode_multipart_formdata

HTTPLIB2_ORG_RESPONSE_KEY = "_original_response"

class HttpSession:


    def hack_httplib2_response():
        original_init = httplib2.Response.__init__
        info_key = HTTPLIB2_ORG_RESPONSE_KEY
        
        def hacked_init(self, info):
            self[info_key] = info
            original_init(self, info)

        httplib2.Response.__init__ = hacked_init

    hack_httplib2_response()

    def __init__(
            self, 
            host, 
            initial_cookies=None, 
            default_encoding="utf-8",
            disable_ssl_certificate_validation=False):

        self.http = httplib2.Http(disable_ssl_certificate_validation=disable_ssl_certificate_validation)
        self.host = host
        self.url_template_parts = urlparse(host)
        self.cookies = SimpleCookie()
        self.default_headers = {}
        if initial_cookies:
            self.cookies.load(initial_cookies)

        self.default_encoding = default_encoding

        self.debug = False

    def make_url(self, path):
        parts = urlparse(path)
        new_parts = []
        for name in ParseResult._fields:
            input_value = getattr(parts, name)
            template_value = getattr(self.url_template_parts, name)
            if input_value:
                new_parts.append(input_value)
            else:
                new_parts.append(template_value)
                
        return urlunparse(new_parts)

    def debug_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def request(
            self,
            path, 
            method,
            body=None, 
            query={},
            headers={}, 
            encoding=None,
            data_type="text",
            update_cookies=True):
        
        self.debug_print("*** request start ***")
        self.debug_print("method:", method)

        url = self.make_url(path)
        self.debug_print("url:", url)

        if isinstance(body, dict):
            body = urlencode(body)

        new_headers = dict(self.default_headers)
        new_headers.update(headers)
        headers = new_headers
        self.debug_print("headers:", headers)
        
        if body:
            has_content_type = False
            for key in headers.keys():
                if key.lower() == "content-type":
                    has_content_type = True
                    break

            if not has_content_type:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

            self.debug_print("body:", body)

        

        if query:
            sep = "?" in url and "&" or "?"
            if isinstance(query, dict):
                query = urlencode(query)

            url = url + sep + query
            self.debug_print("query:", query)

        cookie_content = self.cookies.output(attrs=[], header='', sep=';')
        cookie_content = cookie_content.strip()

        if cookie_content:
            headers["Cookie"] = cookie_content
            self.debug_print("cookie:", cookie_content)

        resp, content = self.http.request(
                url, method, headers=headers, body=body)

        self.debug_print("")
        self.debug_print("response:", content)

        content_type = "text/plain"

        resp_headers = resp[HTTPLIB2_ORG_RESPONSE_KEY].getheaders()
        for k, v in resp_headers:
            lowered_k = k.lower()
            if lowered_k == "set-cookie" and update_cookies:
                self.cookies.load(v)

            if lowered_k == "content-type":
                content_type = v

        return handle_data(
                content, 
                data_type=data_type, 
                mime=content_type,
                encoding=encoding or self.default_encoding)

    def get(self, path, query=None, **kwargs):
        return self.request(path, method="GET", query=query, **kwargs)

    def post(self, path, body, **kwargs):
        return self.request(path, body=body, method="POST", **kwargs)

    def post_multipart(self, path, body, headers={}, **kwargs):
        encoded_body, content_type = encode_multipart_formdata(body)
        new_headers = dict(headers)
        new_headers["Content-Type"] = content_type
        return self.post(path, encoded_body, headers=new_headers, **kwargs)

