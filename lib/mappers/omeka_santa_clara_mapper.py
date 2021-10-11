# -*- coding: utf-8 -*-
from dplaingestion.mappers.omeka_mapper import Omeka_OAIMapper
from dplaingestion.selector import getprop
import requests

class Omeka_OAI_SantaClara_mapper(Omeka_OAIMapper):

    def __init__(self, provider_data):
        super(Omeka_OAI_SantaClara_mapper, self).__init__(provider_data)

    def map_is_shown_at(self):
        isShownAt = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in filter(None, idents):
            if i.startswith('https://sccbosarchive.org/api/items/'):
                omeka_id = i.split('/')[-1]
                isShownAt = 'https://sccbosarchive.org/s/home/item/{}'.format(omeka_id)
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    '''
        rights value in fetched metadata is formatted like this:
        ["No Copyright: http://rightsstatements.org/vocab/NoC-US/1.0/"]
        strip out everything but the URI
    '''
    def map_rights(self):
        rights_list = []
        source_rights = getprop(self.provider_data_source, 'rights')
        for r in filter(None, source_rights):
            if 'rightsstatements.org' in r:
                rights = r.split(': ')[1]
                rights_list.append(rights)
            else:
                rights_list.append(r)
        if rights_list:
            self.update_source_resource({'rights': rights_list})