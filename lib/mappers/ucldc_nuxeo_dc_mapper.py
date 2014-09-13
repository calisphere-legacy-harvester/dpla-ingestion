from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists

class UCLDCNuxeoMapper(DublinCoreMapper):
    def __init__(self, provider_data):
        super(UCLDCNuxeoMapper, self).__init__(provider_data,
                path_parent='$.properties',
                prefix='dc:'
        )

    # root mapping
    def map_is_shown_at(self):
        self.mapped_data.update({"isShownAt": 'http://example.edu'})

    def map_subject(self):
        if exists(self.provider_data, 'dc:subjects'):
            self.update_source_resource({'subject': self.provider_data.get('dc:subjects')})
