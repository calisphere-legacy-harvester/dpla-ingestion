from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.selector import getprop
import re

class LAPL_OAIMapper(CONTENTdm_OAI_Mapper):
    '''A base mapper for LAPL Tessa OAI feed.
    Based off CONTENTdm mapper since it seemed to map all MD correctly.'''

    def __init__(self, provider_data):
        super(LAPL_OAIMapper, self).__init__(provider_data)

    def map_is_shown_at(self):
        isShownAt = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in idents:
            if 'cdm/ref' in i:
                recordKey = i.split("cdm")[1]
                isShownAt = ''.join(
                ('https://tessa.lapl.org/cdm', recordKey))
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})
