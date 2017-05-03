import json
import os.path
import hashlib
from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
#select_id = __import__("dplaingestion.akamod.select-id")

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))

class FlickrMapper(Mapper):
    '''This is the most basic mapping of the flickr photo api to dc metadata
    It is a very thin model, but you can get isShownAt, isShownBy, title & a
    description from it by just mapping elements.
    '''

    def __init__(self, provider_data, key_prefix=None):
        super(FlickrMapper, self).__init__(provider_data, key_prefix)

    def map_is_shown_at(self, index=None):
        '''Set is_shownBy as well'''
        pass

    def map_date(self):
        pass

    def map_description(self):
        pass

    def map_spatial(self):
        pass

    def map_subject(self):
        pass

    def map_title(self):
        pass

    def map_format(self):
        pass
