import hashlib
from dplaingestion.mappers.mapper import Mapper

COUCH_ID_BUILDER = lambda src, lname: "--".join((src, lname))


class eMuseumXMLMapper(Mapper):
    def __init__(self, provider_data, key_prefix=None):
        super(eMuseumXMLMapper, self).__init__(provider_data, key_prefix)

    def map_is_shown_at(self, index=None):
        '''Set is_shown_By as well'''
        if 'id' in self.provider_data:
            id_local = self.provider_data.get('id',{}).get('text')
            if id_local:
                is_shown_at = ''.join(('http://digitalcollections.hoover.org/objects/', id_local))
                self.mapped_data.update({"isShownAt": is_shown_at})
        if 'primaryMedia' in self.provider_data:
            thumb = self.provider_data.get('primaryMedia',{}).get('text')
            if thumb:
                is_shown_by = ''.join(('http://digitalcollections.hoover.org', thumb))
                self.mapped_data.update({"isShownBy": is_shown_by})
        # Use 'youtubeThumbnail' for isShownBy instead, if present
        if 'youtubeThumbnail' in self.provider_data:
            self.mapped_data.update({"isShownBy": self.provider_data.get('youtubeThumbnail',{}).get('text')})

    def map_ids(self):
        collection_id = self.provider_data.get('collection',{})[0].get('resource_uri')
        collection_id = collection_id.rsplit('/')[-2]
        doc_id = self.provider_data.get('id',{}).get('text')
        _id = COUCH_ID_BUILDER(collection_id, doc_id)
        id = hashlib.md5(_id).hexdigest()
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})

    def map_date(self):
        if 'displayDate' in self.provider_data:
            self.update_source_resource({
                'date': self.provider_data.get('displayDate',{}).get('text')
            })

    def map_title(self):
        if 'title' in self.provider_data:
            self.update_source_resource({
                'title': self.provider_data.get('title',{}).get('text')
            })

    def map_creator(self):
        if 'primaryMaker' in self.provider_data:
            self.update_source_resource({
                'creator': self.provider_data.get('primaryMaker',{}).get('text')
            })

    def map_identifier(self):
        if 'id' in self.provider_data:
            self.update_source_resource({
                'identifier': self.provider_data.get('id',{}).get('text')
            })
        if 'invno' in self.provider_data:
            self.update_source_resource({
                'identifier': self.provider_data.get('invno',{}).get('text')
            })

    def map_relation(self):
        if 'collectionTitle' in self.provider_data:
            self.update_source_resource({
                'relation': self.provider_data.get('collectionTitle',{}).get('text')
            })

    def map_type(self):
        if 'mediaType' in self.provider_data:
            self.update_source_resource({
                'type': self.provider_data.get('mediaType',{}).get('text')
            })
