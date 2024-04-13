import requests
import lxml.html
from lxml import etree


html = requests.get('https://www.python.org/').content
tree = lxml.html.document_fromstring(html)
title = tree.xpath('/html/head/title/text()')
print(title)
