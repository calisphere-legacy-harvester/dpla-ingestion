import json
from dplaingestion.mappers.dublin_core_mapper import Mapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify

class UCSDBlacklightDCMapper(Mapper):                                                       

    def __init__(self, provider_data): 
        super(UCSDBlacklightDCMapper, self).__init__(provider_data)

    # root mapping
    def map_is_shown_at(self, index=None):
        pass
###
    def map_data_provider(self):
        super(UCSDBlacklightDCMapper, self).map_data_provider(prop="collection_json_tesim")

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

    def map_is_shown_at(self):
        pass

    def map_has_view(self):
        pass

    def map_object(self):
        pass

    # sourceResource mapping functions
    def map_collection(self):
        prop = "collection"
        if exists(self.provider_data, prop):
            self.update_source_resource({"collection":
                                         self.provider_data.get(prop)})

    def source_resource_prop_from_provider_prop_json(self, provider_prop, prop):
        '''Map the UCSD _json_tesim fields to sourceResource properties.
        The _json_tesim seems to be a list of one json object, load it 
        and assigng to prop
        '''
        if exists(self.provider_data, provider_prop):
            objlist = []
            for o in self.provider_data[provider_prop]:
                objlist.append(json.loads(o))
            self.update_source_resource({prop: objlist})

    def source_resource_prop_from_provider_json_tesim(self, prop):
        provider_prop = ''.join((prop, '_json_tesim'))
        self.source_resource_prop_from_provider_prop_json(provider_prop, prop)

    def map_contributor(self):
        self.source_resource_prop_from_provider_json_tesim('contributor')

    def map_creator(self):
        self.source_resource_prop_from_provider_json_tesim('creator')

    def map_date(self):
        self.source_resource_prop_from_provider_json_tesim('date')

    def map_description(self):
        self.source_resource_prop_from_provider_json_tesim('description')
        self.source_resource_prop_from_provider_prop_json('otherNote_json_tesim', 'description')

    def map_extent(self):
        self.source_resource_prop_from_provider_json_tesim('extent')

    def map_format(self):
        self.source_resource_prop_from_provider_json_tesim('format')

    def map_identifier(self):
        self.source_resource_prop_from_provider_json_tesim('identifier')

###    def map_is_part_of(self):
###        pass

    def map_language(self):
        self.source_resource_prop_from_provider_json_tesim('language')

    def map_publisher(self):
        self.source_resource_prop_from_provider_json_tesim('publisher')

    def map_relation(self):
        self.source_resource_prop_from_provider_json_tesim('relation')

    def map_rights(self):
        self.source_resource_prop_from_provider_json_tesim('rights')

    def map_subject(self):
        self.source_resource_prop_from_provider_json_tesim('subject')

### TODO:    def map_temporal(self):
###        pass

    def map_title(self):
        self.source_resource_prop_from_provider_json_tesim('title')

    def map_type(self):
        self.source_resource_prop_from_provider_json_tesim('type')

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

### TODO:    def map_spatial(self):
###        pass

### TODO:   def map_spec_type(self):
###        pass

