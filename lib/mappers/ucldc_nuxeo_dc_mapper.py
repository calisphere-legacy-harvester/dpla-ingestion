from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists

#TODO: get from akara.ini?
url_nuxeo_base = 'https://nuxeo.cdlib.org/Nuxeo/nxpicsfile/default/'

url_nuxeo_pic_template_med_sz = ''.join((url_nuxeo_base, '{}/Medium:content/'))

class UCLDCNuxeoMapper(DublinCoreMapper):
    def __init__(self, provider_data):
        super(UCLDCNuxeoMapper, self).__init__(provider_data,
                path_parent='$.properties',
                prefix='dc:'
        )

    # root mapping
    def map_is_shown_at(self):
        self.mapped_data.update({"isShownAt": 'http://example.edu'})
        self.mapped_data.update({"isShownBy": 
                url_nuxeo_pic_template_med_sz.format(self.provider_data['uid'])})

    def map_subject(self):
        if exists(self.provider_data_source, 'dc:subjects'):
            self.update_source_resource({'subject': [{'name': s} for s in self.provider_data_source.get('dc:subjects')]})
