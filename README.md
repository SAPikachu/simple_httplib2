This is a wrapper of httplib2 ( http://code.google.com/p/httplib2/ ) to make it easier to use. I made it solely for my work, it may contain many bugs and please use it at your own risk.

# Features not found in original httplib2

* Simple cookie support
* Multipart POST

# Requirements

* Python 3
* httplib2 installed

# Some examples

1. Simple GET

    from simple_httplib2 import http
    result = http.get("http://www.example.com/test.html")

2. Simple POST

    from simple_httplib2 import http
    result = http.post("http://www.example.com/action", 
                       body={
                           "foo": "bar",
                           "foo2": "bar2",
                       })

3. Multipart POST

    from simple_httplib2 import http
    data = read_photo() # data is expected to be bytes
    result = http.post_multipart("http://www.example.com/upload_file", 
                       body={
                           "foo": "bar",
                           "foo2": "bar2",
                           "file": ("some_photo.jpg", data),
                       })

4. Session support (cookies)

    from simple_httplib2 import HttpSession
    session = HttpSession("http://www.example.com/")
    result = session.post("/login", body={ ... })
    # ...
    result = session.get("/protected_data")

5. Data types

    from simple_httplib2 import http
    # supported data types: xml, json
    result = http.get("http://www.example.com/data.json", data_type="json")
    print(result["some_key"])

# License (Simplified BSD License)

Copyright (c) 2011, SAPikachu
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
