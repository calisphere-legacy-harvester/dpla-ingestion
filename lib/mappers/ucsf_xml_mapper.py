import json
import os.path
import hashlib
from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
#select_id = __import__("dplaingestion.akamod.select-id")

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))

class UCSFXMLFeedMapper(Mapper):

    def __init__(self, provider_data, key_prefix=None):
        super(UCSFXMLFeedMapper, self).__init__(provider_data, key_prefix)
        self.metadata = self.provider_data['metadata']

    def map_is_shown_at(self, index=None):
        '''Set is_shownBy as well'''
        is_shown_at = self.provider_data['uri']
        self.mapped_data.update({"isShownAt": is_shown_at})
        self.mapped_data.update({"isShownBy": os.path.join(is_shown_at, 'pdf')})

    def map_ids(self):
        collection_id = self.provider_data['collection'][0]['resource_uri']
        collection_id = collection_id.rsplit('/')[-2]
        doc_id = self.provider_data['tid']
        _id = COUCH_ID_BUILDER(collection_id, doc_id)
        id  = hashlib.md5(_id).hexdigest()
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})

    def _map_metadata_fields(self, fieldname, source_fields):
        '''Map a number source UCSF fields to a sourceResource
        '''
        data = []
        for field in source_fields:
            data.extend(self.metadata.get(field, []))
        self.update_source_resource({fieldname: data}) 

    def map_creator(self):
        self._map_metadata_fields('creator', ('au', 'aup', 'auo'))

    def map_date(self):
        self._map_metadata_fields('date', ('dd',))

    def map_description(self):
        self._map_metadata_fields('description', ('desc', 'cond', 'brd', 'usage',))

    def map_extent(self):
        '''The extent for these is the number of pages in the pdf.
        Given as a list of a single integer, let's format a bit
        '''
        pages = int(self.metadata.get('pg', ['0'])[0])
        if pages:
            extent = '{} page'.format(pages)
            if pages > 1:
                extent += 's'
            self.update_source_resource({'extent':extent})

