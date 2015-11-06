import json
import os.path
import hashlib
from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
#select_id = __import__("dplaingestion.akamod.select-id")

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))

class UCSFSolrFeedMapper(Mapper):

    def map_ids(self):
        collection_id = self.provider_data['collection'][0]['resource_uri']
        collection_id = collection_id.rsplit('/')[-2]
        doc_id = self.provider_data['tid']
        _id = COUCH_ID_BUILDER(collection_id, doc_id)
        id  = hashlib.md5(_id).hexdigest()
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})
