from dplaingestion.selector import setprop
from dplaingestion.mappers.marc_mapper import MARCMapper

class LAPLMARCMapper(MARCMapper):                                                       
    def __init__(self, provider_data):
        super(LAPLMARCMapper, self).__init__(provider_data,
                datafield_tag='fields',
                controlfield_tag='fields')

    def map_data_provider(self):
        super(LAPLMARCMapper, self).map_data_provider(prop="collection")
