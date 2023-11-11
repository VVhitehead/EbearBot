#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import pprint
from googleapiclient.discovery import build

def search(query):
    service = build("customsearch", "v1",
        developerKey="AIzaSyDRRpR3GS1F1_jKNNM9HCNd2wJQyPG3oN0")

    sresults = ''
    tab3mulator = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; '

    res = service.cse().list(
        q = query,
        cx = '013053304011924071846:qhbjw-op0bs',
        num = 3,
        safe = 'off',
        lr = 'lang_en',
    ).execute()

    #pprint.pprint(res)

    i = 0
    if res['searchInformation']['totalResults'] == '0':
        return 'No results found.'
    for item in enumerate(res['items']):
        for thing in item:
            if type(thing) is dict:
                i += 1
                sresults += tab3mulator + str(i) + ') ' + thing['title'] + '\n'
                sresults += thing['snippet'] + '\n' + thing['link'] + '\n'

    sresults += '---'

    return sresults
