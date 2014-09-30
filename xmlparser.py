#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''This module is responsible for parsing the xml and retunring the matching track to executor module'''

import xml.etree.ElementTree as ET

def parseTrackXML(xml,trackstring):
    '''This function parses xml, iterates throug track nodes,extracts required data and returns the matching track href to executor module
    Parameter:
            xml - xml response from Spotify search API
            trackstring - seached track
    Exception:
            catches the xml parse exception and return None (TBD - can be modified as per requirement)
    '''
    trackhref = None
    root = None
    try:
            root = ET.fromstring(xml)
    except Exception, e:
            ## This need to modify to propogate the exception to higher level (if necessary ), at the moment returning 'None'
            ## so that execution does not throw error and exit for this particular string
            return None
    namespaces={'n' : 'http://www.spotify.com/ns/music/1'}
    for track in root.findall("./n:track",namespaces):
            href = track.get('href')
            trackname = track.find('n:name',namespaces).text
            # Break the parsing loop when first matching track is found.
            if trackname.lower() == trackstring.lower():
                trackhref = href
                break
    return trackhref       
