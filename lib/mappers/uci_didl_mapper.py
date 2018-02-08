from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.utilities import iterify
from akara import logger

class UCI_DIDL_Mapper(DublinCoreMapper):

    def map_date(self):
        ''' Remove "created" since it represents date retrieved '''
        fields = ("available", "date", "dateAccepted",
                  "dateCopyrighted", "dateSubmitted", "issued",
                  "modified", "valid")
        self.source_resource_orig_list_to_prop(fields, 'date')

    def map_is_shown_at(self):
        for h in iterify(self.provider_data_source.get('identifier')):
            if "handle.net" in h:
                self.mapped_data.update({"isShownAt": h})
                break

    def map_is_shown_by(self):
        resource = self.provider_data_source.get('Resource')
        isShownBy = resource.get('@ref', '')
        self.mapped_data.update({"isShownBy": isShownBy})
