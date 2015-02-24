import json
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify

class UCSDBlacklightDCMapper(DublinCoreMapper):                                                       
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

###    def source_resource_prop_from_provider_prop_json(self, provider_prop, prop):
###        '''Map the UCSD _json_tesim fields to sourceResource properties.
###        The _json_tesim seems to be a list of one json object, load it 
###        and assigng to prop. Need to know which field in the json we want
###        '''
###        if exists(self.provider_data, provider_prop):
###            objlist = []
###            for o in self.provider_data[provider_prop]:
###                objlist.append(json.loads(o))
###            self.update_source_resource({prop: objlist})
###
    def source_resource_prop_from_provider_json_tesim(self, prop, srcRes_prop=None, sub_key=None):
        '''Get data from a json_tesim.
        Provider prop will be the <prop>_json_tesim
        If sourceResource property has different name, pass in as srcRes_prop.
        sub_key will cause this to only pull forward that key's value from
        the json object in the UCSD field
        '''
        provider_prop = ''.join((prop, '_json_tesim'))
        if not srcRes_prop:
            srcRes_prop = prop
        if not sub_key:
            self.source_resource_orig_to_prop(provider_prop, srcRes_prop)
        else:
            #all stored as list
            values = []
            for obj in self.provider_data.get(provider_prop):
                if obj.get(sub_key):
                    values.append(obj.get(sub_key))
            self.update_source_resource({srcRes_prop: values})

    def map_relationship(self, relationship_type):
        relationships = self.provider_data_source.get('relationship_json_tesim')[0]
        relation = relationships.get(relationship_type, None)
        if relation:
            self.update_source_resource({relationship_type.lower(): relation})

    def map_contributor(self):
        self.map_relationship('Contributor')

    def map_creator(self):
        self.map_relationship('Creator')

    def map_date(self):
        # make DPLA style date object
        # how to handle array of different type date objects, for now just
        # use creation for now, or first if creation not available
        date_list = self.provider_data_source.get('date_json_tesim')
        for date_obj in date_list:
            if date_obj['type'] == 'creation':
                break
        else: # no creation date, use first date
            date_obj = date_list[0]
        date_mapped = dict(end=date_obj['endDate'],
                           begin=date_obj['beginDate'],
                           displayDate=date_obj['value'])
        self.update_source_resource({'date': date_mapped})

    def parse_otherNotes(self, note_type, display_label=None):
        '''Pull out values for the note_type from the otherNote_json_tesim.
        If display_label is specified, only take values when the 
        displayLabel equals the given display_label
        return the values for the note type
        '''
        values = []
        otherNotes = self.provider_data_source.get('otherNote_json_tesim')
        for note in otherNotes:
            if note['type'] == note_type:
                if display_label and display_label == note['displayLabel']:
                    values.append(note['value'])
                else:
                    values.append(note['value'])
        return values if len(values) else None

    def get_otherNotes_field(self, field, display_label=None):
        '''Get a field from that is in the otherNotes.
        '''
        values = self.parse_otherNotes(field)
        if values:
            self.update_source_resource({field: values})

    def map_description(self):
        self.get_otherNotes_field('description')

    def map_extent(self):
        self.source_resource_prop_from_provider_json_tesim('extent')

    def map_format(self):
        values = self.parse_otherNotes('general physical description')
        if values:
            self.update_source_resource({'format': values})

    def map_identifier(self):
        self.get_otherNotes_field('identifier')

###    def map_is_part_of(self):
###        pass

    def map_language(self):
        field = 'language'
        self.source_resource_prop_from_provider_json_tesim(field)
        #fix to match dpla spec
        values = []
        for lang in self.mapped_data["sourceResource"][field]:
            lang['iso639'] = lang['code']
            del lang['code']
            del lang['externalAuthority']
            values.append(lang)
        self.update_source_resource({field:values})

    def map_publisher(self):
        self.source_resource_prop_from_provider_json_tesim('publisher')

    def map_relation(self):
        self.source_resource_prop_from_provider_json_tesim('relation')

    def map_rights(self):
        values = []
        for obj in self.provider_data.get('copyright_tesim', []):
            values.append(obj.get('status')) if obj.get('status') else None
            values.append(obj.get('note')) if obj.get('note') else None
            values.append(obj.get('purposeNote')) if obj.get('purposeNote') else None
        self.update_source_resource({'rights':values})

    def map_subject(self):
        self.source_resource_prop_from_provider_json_tesim('subject')

### TODO:    def map_temporal(self):
###        pass

    def map_title(self):
        self.source_resource_orig_to_prop('title_tesim', 'title')

    def map_type(self):
        self.source_resource_prop_from_provider_json_tesim('type')

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

### TODO:    def map_spatial(self):
###        pass

### TODO:   def map_spec_type(self):
###        pass

