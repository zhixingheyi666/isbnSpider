# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


from .LOG_sf  import logger 
__author__ = 'flyfree'


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError:
        return None
        #logger.exception('getTitle Failure:')
        #logger.warn('getTitle Failure')
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
        #badContent = bsObj.nonExisitingTag.anotherTag
    except AttributeError:
        return None
        #logger.exception('Tag wad not found')
        #logger.warn('Tag wad not found')
    else:
        logger.info('Title:\t%s',title) 
        return title
            

