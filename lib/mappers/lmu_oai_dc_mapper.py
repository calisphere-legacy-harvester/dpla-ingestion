from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper

class LMU_OAI_Mapper(DublinCoreMapper):
    def __init__(self, provider_data):
        super(LMU_OAI_Mapper, self).__init__(provider_data)
