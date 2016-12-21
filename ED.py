#!/usr/bin/env python

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
import json
import re
import pprint

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'} # 'proper' ID

def search(query):
    q = {'srsearch': query}
    query = urlencode(q)
    url = 'https://encyclopediadramatica.se/api.php?action=query&list=search&format=json&' + query
    http = Request(url, None, headers)
    r = urlopen(http)
    encoding = r.headers.get_content_charset()
    theObject = json.loads(r.read().decode(encoding))
    resl = ''

    for index, result in enumerate(theObject['query']['search']):
        resl += ((str(index + 1) + ') ' + result['title'])) + ': '
        resl += 'https://encyclopediadramatica.se/' + result['title'].replace(' ', '_')
        resl += '\n'

    if resl == '':
        resl += 'No Results Found.'

    return resl
