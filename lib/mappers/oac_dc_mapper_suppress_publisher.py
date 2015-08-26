import os
from dplaingestion.mappers.oac_dc_mapper import OAC_DCMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
from akara import module_config

URL_OAC_CONTENT_BASE = module_config().get(
                        'url_oac_content',
                        os.environ.get('URL_OAC_CONTENT_BASE',
                                        'http://content.cdlib.org')
                        )

class OAC_DCMapperSuppressPublisher(OAC_DCMapper):
    '''Mapper for OAC xml feed with bogus publisher fields'''
    # sourceResource mapping
    def map_publisher(self):
        pass
