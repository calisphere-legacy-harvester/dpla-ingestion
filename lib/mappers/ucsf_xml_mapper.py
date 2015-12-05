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
        self.metadata = self.provider_data.get('metadata', self.provider_data)

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

    def get_metadata_values(self, source_fields):
        '''Get list of string values from source_fields'''
        data = []
        for field in source_fields:
            d = self.metadata.get(field, [None])[0]
            if d:
                #lists are stored as ';' separated values
                d = [ x.strip() for x in d.split(';') ]
                data.extend(d)
        return data

    def _map_metadata_fields(self, fieldname, source_fields):
        '''Map a number source UCSF fields to a sourceResource
        '''
        data = self.get_metadata_values(source_fields)
        self.update_source_resource({fieldname: data}) 

    def map_creator(self):
        self._map_metadata_fields('creator', ('au', 'aup', 'auo'))

    def map_date(self):
        self._map_metadata_fields('date', ('dd',))

    def map_description(self):
        self._map_metadata_fields('description', ('desc', 'cond', 'usage',))

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

    def map_language(self):
        '''Contains name when not english?
        From gallaher corpus:
        Arabic
        Chinese
        French
        German
        Greek
        Hindu
        Italian
        Russian
        Spanish

        and "; " separted list of the above

        We'll need to convert these to ISO 3-letter language equivalents:
        Arabic - ara, Chinese - chi, Dutch - dut, French - fre, German - ger,
        Greek - gre, Hindu - hin, Italian - ita, Russian - rus, Spanish - spa"
        '''
        iso_map = {'Arabic' : 'ara',
                'Chinese': 'chi',
                'French': 'fre',
                'German': 'ger',
                'Greek': 'gre',
                'Hindu': 'hin',
                'Italian': 'ita',
                'Russian': 'rus',
                'Spanish': 'spa',
        }
        lang_list = None
        lg = self.metadata.get('lg', [None])[0]
        if lg:
            lang_list = [{'name':l.strip(), 'iso639_9':iso_map[l.strip()]} for
                l in lg.split(';')]
        if not lang_list:
            lang_list = [{'name':'English', 'iso639_9': 'eng'}]
        self.update_source_resource({'language': lang_list})

    def map_spatial(self):
        '''does this need to map to spatial['country']'''
        cts = self.metadata.get('ct', [None,])[0]
        if cts:
            countries = [ c.strip() for c in cts.split(';')]
            self.update_source_resource({'spatial': countries})

    def map_subject(self):
        '''"
        <brd>: Brand
        <men>: Mentioned
        <meno>: Organizations mentioned
        <org>: Organizations mentioned
        <menp>: Persons mentioned
        <per>: Persons mentioned
        
        2015-05-05 : move brand ('brd') from description to subject

        2015-05-05 : dropping becauses mostly redundant:
                            <cc>: Copied, 
                            <cco>: Organizations copied
                            <ccp>: Person copied
                            <rc>: Recipients
                            <rco>: Organization recipients
                            <rcp>: Person recipients
        '''
        values = self.get_metadata_values(('brd', 'men', 'meno',
                                  'menp', 'org', 'per', ))
        value_objs = [{'name': v} for v in values]
        self.update_source_resource({'subject': value_objs}) 
        
    def map_title(self):
        self.update_source_resource({'title': self.metadata['ti']})

    def map_format(self):
        self._map_metadata_fields('format', ('dt',))
