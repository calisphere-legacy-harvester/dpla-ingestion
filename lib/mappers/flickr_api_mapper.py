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

    def map_is_shown_at(self):
        urls = self.provider_data['urls']
        for url in urls:
            if url['type'] == 'photopage':
                self.mapped_data['isShownAt'] = url['text']

    def map_date(self):
        pass

    def map_description(self):
        self.mapped_data['sourceResource']['description'] = \
                self.provider_data['description']['text']

    def map_spatial(self):
        pass

    def map_subject(self):
        pass

    def map_title(self):
        self.mapped_data['sourceResource']['title'] = self.provider_data['title']['text']

    def map_format(self):
        pass
