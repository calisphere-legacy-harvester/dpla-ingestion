import requests
from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from dplaingestion.selector import exists, getprop

class CONTENTdm_OAI_Mapper(OAIDublinCoreMapper):
    '''A base mapper for CONTENTdm OAI feeds. Should work for most OAI
    feeds from CONTENTdm data sources.
    
    isShownAt & isShownBy are in standard locations relative to the 
    base URL for the feed.
    
    Values are split on semicolons (";") and each one put in new list
    item for a given field.'''

    def __init__(self, provider_data):
        super(CONTENTdm_OAI_Mapper, self).__init__(provider_data)

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

        As it turns out, for "image" type objects, larger images are 
        available.
        The creation of the URL to grab the image needs to check the image
        object information before setting the URL. ContentDM has an image
        server that will resize the image on demand. We want images whose max
        dimension in height or width is 1024. Need to first get image info at
        the base URL then request an appropriately scaled image.
        This needs to be done after the sourceResouce/type is mapped, so it
        happens in update_mapped_fields
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
        '''TOOD:Funky, but map_type comes after the is_shown_by, should change order
        '''
        self.to_source_resource_with_split('type', 'type')

    def get_url_image_info(self):
        image_info = {'height': 0, 'width': 0 }
        ident = self.get_identifier_match('cdm/ref')
        base_url, i, j, k, collid, l, objid = ident.rsplit('/', 6)
        #url_image_info give json data about image for record
        url_image_info = '/'.join((base_url, 'utils', 'ajaxhelper'))
        url_image_info = '{}?CISOROOT={}&CISOPTR={}'.format(
                url_image_info, collid, objid)
        return url_image_info

    def get_image_info(self):
        '''Return image info for the contentdm object'''
        image_info = {'height': 0, 'width': 0 }
        ident = self.get_identifier_match('cdm/ref')
        if ident:
            image_info = requests.get(self.get_url_image_info()).json()['imageinfo']
        return image_info

    def get_larger_preview_image(self):
        # Try to get a bigger image than the thumbnail.
        # Some "text" types have a large image
        image_info = self.get_image_info()
        if image_info['height'] > 0: #if 0 only thumb available
            #figure scaling
            max_dim = 1024.0
            scale = 100
            if image_info['height'] >= image_info['width']:
                scale = int((max_dim / image_info['height']) * 100)
            else:
                scale = int((max_dim / image_info['width']) * 100)
            scale = 100 if scale > 100 else scale
            thumbnail_url = '{}&action=2&DMHEIGHT=2000&DMWIDTH=2000&DMSCALE={}'.format(
                    self.get_url_image_info(), scale)
            self.mapped_data.update({'isShownBy': thumbnail_url})

    def update_mapped_fields(self):
        ''' To run post mapping. For this one, is_shown_by needs
        sourceResource/type'''
        rec_type = self.mapped_data['sourceResource']['type']
        is_sound_object = False
        if isinstance(rec_type, basestring):
            if 'sound' == rec_type.lower():
                is_sound_object = True
        else: #list type
            for val in rec_type:
                if 'sound' == val.lower():
                    is_sound_object = True
        if not is_sound_object:
            self.get_larger_preview_image()
        else:
            if 'isShownBy' in self.mapped_data:
                del self.mapped_data['isShownBy']
