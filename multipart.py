# urllib3/filepost.py
# Copyright 2008-2011 Andrey Petrov and contributors (see CONTRIBUTORS.txt)
#
# This module is part of urllib3 and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

# Ported to Python 3 by SAPikachu

import mimetypes
import random
import string

from io import BytesIO, BufferedWriter


class StringBytesWriter(BufferedWriter):
    def __init__(self, encoding="utf-8", *args, **kwargs):
        super().__init__(BytesIO(), *args, **kwargs)
        self.encoding = encoding

    def write(self, data):
        if isinstance(data, str):
            return super().write(data.encode(self.encoding))
        else:
            return super().write(data)

    def getvalue(self):
        self.flush()
        return self.raw.getvalue()

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def choose_boundary():
    return ''.join(
        [random.choice(string.ascii_letters + string.digits)
         for x in range(60)])

def encode_multipart_formdata(fields, boundary=None):
    """
    Encode a dictionary of ``fields`` using the multipart/form-data mime format.

    :param fields:
        Dictionary of fields. The key is treated as the field name, and the
        value as the body of the form-data. If the value is a tuple of two
        elements, then the first element is treated as the filename of the
        form-data section.

    :param boundary:
        If not specified, then a random boundary will be generated using
        :func:`mimetools.choose_boundary`.
    """
    body = StringBytesWriter()
    if boundary is None:
        boundary = choose_boundary()

    for fieldname, value in fields.items():
        body.write('--%s\r\n' % (boundary))

        if isinstance(value, tuple):
            filename, data = value
            body.write('Content-Disposition: form-data; name="%s"; '
                               'filename="%s"\r\n' % (fieldname, filename))
            body.write('Content-Type: %s\r\n\r\n' %
                       (get_content_type(filename)))
        else:
            data = value
            body.write('Content-Disposition: form-data; name="%s"\r\n'
                               % (fieldname))
            body.write('Content-Type: text/plain\r\n\r\n')

        if isinstance(data, int):
            data = str(data)  # Backwards compatibility

        body.write(data)

        body.write('\r\n')

    body.write('--%s--\r\n' % (boundary))

    content_type = 'multipart/form-data; boundary=%s' % boundary

    return body.getvalue(), content_type

if __name__ == "__main__":
    print("Test output:")
    print(encode_multipart_formdata({
        "test_field": "1",
        "file1": b"test1",
        "file2": ("file2.jpg", b"test2"),
        "file3": (r"c:\file3.jpg", b'test3'),
    })[0].decode("utf-8"))
