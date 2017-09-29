import hashlib
from dplaingestion.mappers.mapper import Mapper

COUCH_ID_BUILDER = lambda src, lname: "--".join((src, lname))


class SacramentoXMLMapper(Mapper):
    def __init__(self, provider_data, key_prefix=None):
        super(SacramentoXMLMapper, self).__init__(provider_data, key_prefix)
        self.metadata = self.provider_data.get('metadata', self.provider_data)

    def map_is_shown_at(self, index=None):
        '''Set is_shownBy as well'''
        self.mapped_data.update({"isShownAt": self.metadata['url'][0]})
        self.mapped_data.update({"isShownBy": self.metadata['thumbnail'][0]})

    def map_ids(self):
        collection_id = self.provider_data['collection'][0]['resource_uri']
        collection_id = collection_id.rsplit('/')[-2]
        doc_id = self.metadata['identifier'][0]
        _id = COUCH_ID_BUILDER(collection_id, doc_id)
        id = hashlib.md5(_id).hexdigest()
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})

    def get_metadata_values(self, source_fields):
        '''Get list of string values from source_fields'''
        data = []
        for field in source_fields:
            d = self.metadata.get(field, [None])[0]
            if d:
                # lists are stored as '|' separated values
                d = [x.strip() for x in d.split('|')]
                data.extend(d)
        return data

    def map_date(self):
        self.update_source_resource({'date': self.metadata['date'][0]})

    def map_description(self):
        self.update_source_resource({
            'description': self.metadata['description'][0]
        })

    def map_subject(self):
        values = self.get_metadata_values(('subject', ))
        value_objs = [{'name': v} for v in values]
        self.update_source_resource({'subject': value_objs})

    def map_title(self):
        self.update_source_resource({'title': self.metadata['title'][0]})

    def map_identifier(self):
        self.update_source_resource({
            'identifier': self.metadata['identifier'][0]
        })

    def map_relation(self):
        self.update_source_resource({
            'relation': self.metadata['collection'][0]
        })
