from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper

class CAVPP_CONTENTdm_OAI_Mapper(CONTENTdm_OAI_Mapper):
    def map_is_shown_at(self):
        '''Grab the identifier starting with "http://archive.org"
        '''
        isShownAt = self.get_identifier_match('http://archive.org')
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})
        if not isShownAt:
            super(CAVPP_CONTENTdm_OAI_Mapper, self).map_is_shown_at()


