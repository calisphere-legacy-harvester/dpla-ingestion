import hashlib
from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import getprop
from akara import logger

COUCH_ID_BUILDER = lambda src, lname: "--".join((src, lname))


class UCD_JSONMapper(Mapper):
    def __init__(self, provider_data, key_prefix=None):
        super(UCD_JSONMapper, self).__init__(provider_data, key_prefix)
        self.metadata = self.provider_data.get('metadata', self.provider_data)

    def map_is_shown_by(self, index=None):
        isShownBy = None
        if 'thumbnailUrl' in self.metadata:
            isShownBy = "https://digital.ucdavis.edu" + getprop(self.metadata, 'thumbnailUrl')
        if isShownBy:
            self.mapped_data.update({'isShownBy': isShownBy})

    def map_is_shown_at(self, index=None):
        isShownAt = None
        if '@id' in self.metadata:
            recordID = getprop(self.metadata, '@id')
            isShownAt = "https://digital.ucdavis.edu" + recordID
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    def map_ids(self):
        collection_id = self.provider_data.get('collection',{})[0].get('resource_uri')
        collection_id = collection_id.rsplit('/')[-2]
        #get ARK for _id, if possible
        doc_id = None
        for i in self.metadata.get('identifier'):
            if 'ark:/' in i:
                doc_id = i
        if not doc_id:
            doc_id = self.metadata.get('identifier')[0]
        _id = COUCH_ID_BUILDER(collection_id, doc_id)
        id = hashlib.md5(_id).hexdigest()
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})

    def map_title(self):
        if 'name' in self.metadata:
            self.update_source_resource({'title': self.metadata.get('name')})

    def map_date(self):
        if 'datePublished' in self.metadata:
            self.update_source_resource({
                'date': self.metadata.get('datePublished')
            })

    def map_description(self):
        if 'description' in self.metadata:
            self.update_source_resource({
                'description': self.metadata.get('description')
            })

    def map_subject(self):
        if 'about' in self.metadata:
            values = self.metadata.get('about')
            if isinstance(values, dict):
                subject = [{'name': values['name']}]
            elif isinstance(values, basestring):
                subject = [{'name': values}]
            else:
                for v in values:
                    subject = [{'name': v['name']} for v in values]
            self.update_source_resource({'subject': subject})

    def map_format(self):
        if 'material' in self.metadata:
            self.update_source_resource({'format': self.metadata.get('material')})

    def map_creator(self):
        if 'creator' in self.metadata:
            if isinstance(self.metadata['creator'], list):
                for p in self.metadata['creator']:
                    if 'name' in p:
                        creator = p['name']
            elif isinstance(self.metadata['creator'], dict):
                if 'name' in self.metadata['creator']:
                    creator = self.metadata['creator'].values()
            else:
                if 'name' in self.metadata['creator']:
                    creator = self.metadata['creator']
            if creator:
                self.update_source_resource({'creator': creator})

    def map_identifier(self):
        identifiers = []
        if 'identifier' in self.metadata:
            for i in self.metadata.get('identifier'):
                identifiers.append(i)
        if identifiers:
            self.update_source_resource({'identifier': identifiers})

    def map_publisher(self):
        if 'publisher' in self.metadata:
            if isinstance(self.metadata['publisher'], list):
                for p in self.metadata['publisher']:
                    if 'name' in p:
                        publish = p['name']
            elif isinstance(self.metadata['publisher'], dict):
                if 'name' in self.metadata['publisher']:
                    publish = self.metadata['publisher'].values()
            else:
                if 'name' in self.metadata['publisher']:
                    publish = self.metadata['publisher']
            if publish:
                self.update_source_resource({'publisher': publish})

    def map_type(self):
        restrict_types = ["CreativeWork", "MediaObject"]
        if 'type' in self.metadata:
            if not isinstance(self.metadata['type'], basestring):
                for t in self.metadata['type']:
                    if t.startswith(tuple(restrict_types)):
                        continue
                    else:
                        self.update_source_resource({'type': t})
            else:
                self.update_source_resource({'type': self.metadata['type']})

    def map_rights(self):
        if 'license' in self.metadata:
            self.update_source_resource({'rightsURI': self.metadata['license']})
