#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''This module is responsible for making a http request to Spotify search API and returning a xml response.

'''
import traceback
import urllib2
from urllib import urlencode

def fetch_xml(searchstr):
    '''This Function is responsible making the http request and returning the response to calling function.
    Parameter:
            searchstr - a string which is used as an argument to the request url
    Return:
            responsexml - an xml like object
    Exception: HTTPError,URLError,HTTPException,Exception
    
    '''
    req = urllib2.Request('http://ws.spotify.com/search/1/track?'+urlencode({'q': searchstr}))
    #print req.get_full_url()
    try:
        response = urllib2.urlopen(req)
    except Exception:
        raise
    responsexml = response.read()
    return responsexml
