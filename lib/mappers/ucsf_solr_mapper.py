import json
import os.path
import hashlib
from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
#select_id = __import__("dplaingestion.akamod.select-id")

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))

class UCSFSolrFeedMapper(Mapper):

    def __init__(self, provider_data, key_prefix=None):
        super(UCSFSolrFeedMapper, self).__init__(provider_data, key_prefix)
        self.metadata = self.provider_data

    def map_ids(self):
        collection_id = self.provider_data['collection'][0]['resource_uri']
        collection_id = collection_id.rsplit('/')[-2]
        doc_id = self.provider_data['id']
        _id = COUCH_ID_BUILDER(collection_id, doc_id)
        id  = hashlib.md5(_id).hexdigest()
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})

    def map_is_shown_at(self, index=None):
        '''Set is_shownBy as well'''
        id_local = self.metadata['id']
        is_shown_by_path = '/'.join([ c for c in id_local[:4]])
        is_shown_at = 'https://industrydocuments.library.ucsf.edu/tobacco/docs/#id={}'.format(id_local)
        is_shown_by_base = 'https://s3-us-west-2.amazonaws.com/edu.ucsf.library.iddl.artifacts/'
        is_shown_by = ''.join((is_shown_by_base, is_shown_by_path,
                                '/{}/{}_thumb.png'.format(id_local, id_local)))
        self.mapped_data.update({"isShownAt": is_shown_at})
        self.mapped_data.update({"isShownBy": is_shown_by})

    def map_creator(self):
        self.update_source_resource({'creator': self.metadata.get('author')})

    def map_title(self):
        self.update_source_resource({'title': [self.metadata.get('title', None)]})

    def map_date(self):
        self.update_source_resource({'date': [self.metadata.get('documentdate',
            None)]})

    def map_description(self):
        description_str = self.metadata.get('description', None)
        if description_str:
            descriptions = description_str.split(';')
            self.update_source_resource({'description':
                [ s.strip() for s in descriptions]})

    def map_extent(self):
        '''The extent for these is the number of pages in the pdf.
        Given as a list of a single integer, let's format a bit
        '''
        pages = int(self.metadata.get('pages', '0'))
        if pages:
            extent = '{} page'.format(pages)
            if pages > 1:
                extent += 's'
            self.update_source_resource({'extent':extent})

    def map_identifier(self):
        ids = [self.metadata['id'], self.metadata['tid']]
        if 'bates' in self.metadata:
            ids.append(self.metadata['bates'])
        if 'case' in self.metadata:
            ids.extend(self.metadata['case'])
        self.update_source_resource({'identifier':ids})

    def map_relation(self):
        self.update_source_resource({'relation':
            self.metadata.get('source_collection_name')})

    def map_subject(self):
        '''brand, mentioned, organization & person'''
        subjects = []
        if 'brand' in self.metadata:
            subjects.extend(self.metadata['brand'])
        if 'mentioned' in self.metadata:
            subjects.extend(self.metadata['mentioned'])
        if 'organization' in self.metadata:
            subjects.extend(self.metadata['organization'])
        if 'person' in self.metadata:
            subjects.extend(self.metadata['person'])
        if subjects:
            self.update_source_resource({'subject': subjects})

    def map_spatial(self):
        countries = self.metadata.get('country', '').split(';')
        if countries:
            self.update_source_resource({'spatial':
                [ {'text': c.strip() } for c in countries]})

    def map_type(self):
        '''Map type & genre'''
        if 'type' in self.metadata:
            self.update_source_resource({'genre': self.metadata['type']})

