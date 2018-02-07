from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper


class UCI_DIDL_Mapper(DublinCoreMapper):
    def map_date(self):
        ''' Remove "created" since it represents date retrieved '''
        fields = ("available", "date", "dateAccepted",
                  "dateCopyrighted", "dateSubmitted", "issued",
                  "modified", "valid")
        self.source_resource_orig_list_to_prop(fields, 'date')
