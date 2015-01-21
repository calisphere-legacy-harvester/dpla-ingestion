import os
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
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

    def map_is_shown_at(self, index=None):
        self.mapped_data.update( {"isShownAt" : self.select_isShownAt(),
            "isShownBy" :  self.get_best_oac_image(),
            })

    def map_data_provider(self):
        if self.provider_data.has_key('originalRecord'):
            if self.provider_data['originalRecord'].has_key('collection'):
                self.mapped_data.update({"dataProvider":
                    self.provider_data['originalRecord']['collection']})

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

    def map_spatial(self):
        print "PROVIDER KEYS:", self.provider_data.keys()
        if self.provider_data.has_key('originalRecord'):
            if self.provider_data['originalRecord'].has_key('coverage'):
                self.update_source_resource({"spatial":
                                         iterify(getprop(self.provider_data['originalRecord'],
                                                         "coverage"))})
