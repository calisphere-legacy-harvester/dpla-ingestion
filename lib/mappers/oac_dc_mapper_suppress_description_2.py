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

class OAC_DCMapperSuppressDescription2(OAC_DCMapper):
    '''Mapper for OAC xml feed objects with copyrighted transcripts
    There are 2 collections which have copyrighted transcripts
    encoded in the 2nd description field. These need to be suppressed
    
    As of 20150224 the 2 collections are
    1) Nance (Afton) Dill Papers (collection ID #15486)
    2) Workman Family Papers (collection ID #25043)
    '''
    # sourceResource mapping
    def map_description(self):
        descs = self.provider_data.get('description', [])
        safe_descs = []
        for n, desc in enumerate(descs):
            if n == 1:
                continue
            safe_descs.append(desc['text'])
        self.update_source_resource({'description':safe_descs}) \
                if len(safe_descs) else None
