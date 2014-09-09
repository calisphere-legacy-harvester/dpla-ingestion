from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify

class UCLASolrMapper(Mapper):                                                       
    URL_UCLA_OBJECT_ROOT = 'http://digital.library.ucla.edu/collections/islandora/object/'
    # root mapping
    def map_is_shown_at(self, index=None):
        self.mapped_data.update( {"isShownAt" :  ''.join((self.URL_UCLA_OBJECT_ROOT, self.provider_data['PID'])),
            "isShownBy" :  {'src':''.join((self.URL_UCLA_OBJECT_ROOT, self.provider_data['PID'], '/datastream/JPG/JPG.jpg'))},
            })

    def map_data_provider(self):
        super(UCLASolrMapper, self).map_data_provider(prop="collection")

    # sourceResource mapping
    def source_resource_prop_to_prop(self, prop):
        #for ucla, the dc elements are prefixed by dc.
        #remove before sending to sourceResource
        if exists(self.provider_data, prop):
            self.update_source_resource({prop[3:]: self.provider_data.get(prop)})
            
    def map_collection(self):
        self.source_resource_prop_to_prop("dc.collection")

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

    def map_contributor(self):
        self.source_resource_prop_to_prop("dc.contributor")

    def map_creator(self):
        self.source_resource_prop_to_prop("dc.creator")

    def map_date(self):
        self.source_resource_prop_to_prop("dc.date")

    def map_description(self):
        self.source_resource_prop_to_prop("dc.description")

    def map_extent(self):
        self.source_resource_prop_to_prop("dc.extent")

    def map_format(self):
        self.source_resource_prop_to_prop("dc.format")

    def map_language(self):
        self.source_resource_prop_to_prop("dc.language")

    def map_spatial(self):
        if exists(self.provider_data, "dc.coverage"):
            self.update_source_resource({"spatial":
                                         iterify(getprop(self.provider_data,
                                                         "dc.coverage"))})

    def map_relation(self):
        self.source_resource_prop_to_prop("dc.relation")

    def map_rights(self):
        self.source_resource_prop_to_prop("dc.rights")

    def map_subject(self):
        self.source_resource_prop_to_prop("dc.subject")

    def map_temporal(self):
        self.source_resource_prop_to_prop("dc.temporal")

    def map_title(self):
        self.source_resource_prop_to_prop("dc.title")

    def map_type(self):
        self.source_resource_prop_to_prop("dc.type")

    def map_identifier(self):
        self.source_resource_prop_to_prop("dc.identifier")

    def map_publisher(self):
        self.source_resource_prop_to_prop("dc.publisher")
