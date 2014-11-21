from dplaingestion.selector import setprop
from dplaingestion.mappers.pymarc_mapper import PYMARCMapper

class LAPLMARCMapper(PYMARCMapper):                                                       
    def __init__(self, provider_data):
        super(LAPLMARCMapper, self).__init__(provider_data,
                datafield_tag='fields',
                controlfield_tag='fields')

    def map_data_provider(self):
        super(LAPLMARCMapper, self).map_data_provider(prop="collection")


    def update_is_shown_at(self):
        '''Cheat, use this to copy isShownAt to isShownBy for 
        grabbing images'''
        self.mapped_data['isShownBy'] = self.mapped_data['isShownAt']
