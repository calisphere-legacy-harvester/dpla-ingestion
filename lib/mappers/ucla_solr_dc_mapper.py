from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify

class UCLASolrDCMapper(DublinCoreMapper):
    URL_UCLA_OBJECT_ROOT = 'http://digital.library.ucla.edu/collections/islandora/object/'

    def __init__(self, provider_data): 
        super(UCLASolrDCMapper, self).__init__(provider_data, prefix='dc.')

    # root mapping
    def map_is_shown_at(self, index=None):
        self.mapped_data.update( {"isShownAt" :  ''.join((self.URL_UCLA_OBJECT_ROOT, self.provider_data['PID'])),
            "isShownBy" :  ''.join((self.URL_UCLA_OBJECT_ROOT, self.provider_data['PID'], '/datastream/JPG/JPG.jpg')),
            })

    def map_data_provider(self):
        super(UCLASolrDCMapper, self).map_data_provider(prop="collection")

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

    def map_spatial(self):
        if exists(self.provider_data, "dc.coverage"):
            self.update_source_resource({"spatial":
                                         iterify(getprop(self.provider_data,
                                                         "dc.coverage"))})
