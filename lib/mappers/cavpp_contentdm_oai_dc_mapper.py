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

    def map_identifier(self):
        super(CAVPP_CONTENTdm_OAI_Mapper, self).map_identifier()
        # remove any ids that match start with http://cdm15972.contentdm.oclc.org/
        new_ids = []
        for ident in self.mapped_data['sourceResource']['identifier']:
            if not ident.startswith('http://cdm15972.contentdm.oclc.org'):
                new_ids.append(ident)
        self.mapped_data['sourceResource']['identifier'] = new_ids

