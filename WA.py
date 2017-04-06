#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wolframalpha

app_id = 'Wolfram|Alpha API key'
client = wolframalpha.Client(app_id)
params = (
    ('format', 'plaintext'),
    ('reinterpret', 'true'),
    ('location', 'dummy, LOCATION'),
    ('ip', '8.8.8.8'),
    ('latlong','0, 0')
)

def search(query):
    try:
        res = client.query(query, params=params)
    except Exception as e:
        print ('query failed:', e)
        return ('query failure!')
    sres = ''
    try:
        sres = (next(res.results).text)
    except Exception as e:
        print (e)
        try:
            sres += 'Input interpretation: ' + res.details['Input interpretation'] + '\n'
        except Exception as e:
            sres = 'No primary results, alternative processing not yet implemented!'
        try:
            sres += 'Description: ' + res.details['Description'] + '\n'
        except:
            pass
        try:
            sres += res.details['Basic information'] + '\n'
        except:
            pass
        try:
            sres += 'Current evidence: ' + res.details['Current evidence'] + '\n'
        except:
            pass
    try:
        if res.details['Input interpretation'].endswith('(English word)'):
            try:
                sres += '\nFirst known use in English: ' + res.details['First known use in English'] + '\n'
            except:
                pass
            try:
                sres += 'Word origins: ' + res.details['Word origins']
            except:
                pass
            try:
                sres += 'Word origins: ' + res.details['Word origin']
            except:
                pass
            try:
                sres += 'Overall typical frequency: ' + res.details['Overall typical frequency'] + '\n'
            except:
                pass
            try:
                sres += 'Synonyms: ' + res.details['Synonyms'] + '\n'
            except:
                pass
            try:
                sres += 'Antonyms: ' + res.details['Antonyms']
            except:
                pass
    except Exception as e:
        print (e)

    return sres
