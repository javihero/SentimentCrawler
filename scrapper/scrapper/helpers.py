import re
import html


def sanitize_content(data):
    data = html.unescape(data)
    p = re.compile(r'<.*?>')
    return p.sub('', data)
