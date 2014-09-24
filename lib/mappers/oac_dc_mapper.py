import os
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from akara import module_config

URL_OAC_CONTENT_BASE = module_config().get(
                        'url_oac_content',
                        os.environ.get('URL_OAC_CONTENT_BASE',
                                        'http://content.cdlib.org')
                        )

class OAC_DCMapper(DublinCoreMapper):
    '''Mapper for OAC xml feed objects'''

    def get_best_oac_image(self):
        '''From the list of images, choose the largest one'''
        best_image = None
        x = 0
        thumb = self.provider_data['originalRecord'].get('thumbnail', None)
        if thumb:
            x = thumb['X']
            best_image = thumb['src']
        ref_images = self.provider_data['originalRecord'].get('reference-image', [])
        if type(ref_images) == dict:
            ref_images = [ref_images]
        for obj in ref_images:
            if int(obj['X']) > x:
                x = int(obj['X'])
                best_image = obj['src']
        if best_image and not best_image.startswith('http'):
            best_image = '/'.join((URL_OAC_CONTENT_BASE, best_image))
        return best_image

    def select_isShownAt(self):
        '''The identifier that's a URL and has ark: is the location
        where the object lives in the current OAC'''
        isShownAt = None
        print('d:{} OR:{}'.format(self.provider_data.keys(), self.provider_data['originalRecord'].keys()))
        for u in self.provider_data['originalRecord']['identifier']:
            if u[:4] == 'http':
                isShownAt = u
        return isShownAt

    def map_is_shown_at(self, index=None):
        self.mapped_data.update( {"isShownAt" : self.select_isShownAt(),
            "isShownBy" :  self.get_best_oac_image(),
            })

    def map_data_provider(self):
        super(OAC_DCMapper, self).map_data_provider(prop="collection")

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

    def map_spatial(self):
        if exists(self.provider_data, "coverage"):
            self.update_source_resource({"spatial":
                                         iterify(getprop(self.provider_data,
                                                         "coverage"))})
