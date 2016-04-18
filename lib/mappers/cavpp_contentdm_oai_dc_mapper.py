from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper

class CAVPP_CONTENTdm_OAI_Mapper(CONTENTdm_OAI_Mapper):
    def map_is_shown_at(self):
        '''Grab the identifier with "archive.org" in them
        '''
        isShownAt = self.get_identifier_match('archive.org')
        if isShownAt:
            if not isShownAt.startswith('http'):
                isShownAt = 'http://' + isShownAt
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

    def update_mapped_fields(self):
        super(CAVPP_CONTENTdm_OAI_Mapper, self).update_mapped_fields()
        rec_type = self.mapped_data['sourceResource']['type']
        is_moving_image = False
        if isinstance(rec_type, basestring):
            if 'moving image' == rec_type.lower():
                is_moving_image = True
        else: #list type
            for val in rec_type:
                if 'moving image' == val.lower():
                    is_moving_image = True
                    break
        if is_moving_image:
            self.map_is_shown_by()
