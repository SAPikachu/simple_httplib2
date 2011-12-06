
def handle_xml(s):
    from xml.dom.minidom import parseString

    return parseString(s)

def handle_json(s):
    import json
    
    return json.loads(s)

def handle_text(s):
    return s

mime_mappings = {
    "application/xml": "xml",
    "text/xml": "xml",
    "application/json": "json",
    "text/json": "json",
    "text/x-json": "json",
    "text/plain": "text",
}

handler_mappings = {
    "xml": handle_xml,
    "json": handle_json,
    "text": handle_text,
}

def mime_to_data_type(mime, default="text"):
    actual_mime = mime.split(";")[0].strip().lower()

    return mime_mappings.get(actual_mime, default)

def handle_data(content, data_type="text", mime="", encoding="utf-8"):
    if data_type == "auto":
        data_type = mime_to_data_type(mime)

    if data_type == "bytes":
        return content

    content = content.decode(encoding)

    return handler_mappings[data_type](content)
