# -*- coding: utf-8 -*-
from dplaingestion.mappers.omeka_mapper import Omeka_OAIMapper
from dplaingestion.selector import getprop
import requests

class Omeka_OAI_SantaClara_mapper(Omeka_OAIMapper):

    def map_is_shown_at(self):
        isShownAt = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in filter(None, idents):
            if i.startswith('https://sccbosarchive.org/api/items/'):
                omeka_id = i.split('/')[-1]
                isShownAt = 'https://sccbosarchive.org/s/home/item/{}'.format(omeka_id)
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})