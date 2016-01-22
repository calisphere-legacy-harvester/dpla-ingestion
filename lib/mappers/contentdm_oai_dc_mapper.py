from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop

class CONTENTdm_OAI_Mapper(DublinCoreMapper):
    '''A base mapper for CONTENTdm OAI feeds. Should work for most OAI
    feeds from CONTENTdm data sources.
    
    isShownAt & isShownBy are in standard locations relative to the 
    base URL for the feed.
    
    Values are split on semicolons (";") and each one put in new list
    item for a given field.'''

    def __init__(self, provider_data):
        super(CONTENTdm_OAI_Mapper, self).__init__(provider_data)

    def split_values(self, prop):
        new_values = []
        if exists(self.provider_data_source, prop):
            for value in getprop(self.provider_data_source, prop):
                new_values.extend([ s.strip() for s in value.split(';')])
        return new_values

    def to_source_resource_with_split(self, provider_prop, srcRes_prop):
        '''Copy the provider_prop to the srcRes_prop & split on ; in
        data values'''
        values = self.split_values(provider_prop)
        self.update_source_resource({srcRes_prop: values})


    def get_identifier_match(self, string_in):
        '''Return the identifier that has the given string in it'''
        idents = getprop(self.provider_data_source, 'identifier')
        for i in idents:
            if string_in in i:
                return i
        return None

    def map_is_shown_by(self):
        '''Can only reliably get a small tumbnail from the CONTENTdm
        with the metadata in the OAI feed
        Can parse the OAI id to get infor we need.
        '''
        ident = self.get_identifier_match('cdm/ref')
        if ident:
            base_url, i, j, k, collid, l, objid = ident.rsplit('/', 6)
            thumbnail_url = '/'.join((base_url, 'utils', 'getthumbnail',
                'collection', collid, 'id', objid))
            self.mapped_data.update({'isShownBy': thumbnail_url})

    def map_is_shown_at(self):
        '''The identifier that points to the OAI server & has cdm/ref in the
        path is the path to object.
        Can get harvest base URL from the "collection" object
        '''
        isShownAt = self.get_identifier_match('cdm/ref')
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    def map_contributor(self):
        self.to_source_resource_with_split('contributor', 'contributor')

    def map_creator(self):
        self.to_source_resource_with_split('creator', 'creator')

    def map_subject(self):
        values = self.split_values('subject')
        subject_objs = [ {'name': v } for v in values]
        self.update_source_resource({'subject': subject_objs})

    def map_spatial(self):
        self.to_source_resource_with_split('coverage', 'spatial')

    def map_type(self):
        self.to_source_resource_with_split('type', 'type')
