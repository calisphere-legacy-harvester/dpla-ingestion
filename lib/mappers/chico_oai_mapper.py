from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper


class Chico_OAI_Mapper(CONTENTdm_OAI_Mapper):
    def map_date(self):
        # Suppress 'created' from sourceResource
        # to not confuse decade faceting, since it currently
        # represents date digitized
        self.source_resource_orig_to_prop("date", "date")
