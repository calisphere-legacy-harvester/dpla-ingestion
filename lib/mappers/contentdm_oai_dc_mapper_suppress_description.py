from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper

class CONTENTdm_OAI_Suppress_Description_Mapper(CONTENTdm_OAI_Mapper):
    '''Suppress description mapping.
    Needed for UOP Dave Brubeck oral history where description is just 
    a transcription
    '''
    def map_description(self):
        pass
