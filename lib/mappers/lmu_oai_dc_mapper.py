from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper

class LMU_OAI_Mapper(DublinCoreMapper):
    def __init__(self, provider_data, path_parent=None, prefix='dc:'):
        super(LMU_OAI_Mapper).__init__(self, provider_data, path_parent,
                prefix)
