from dplaingestion.selector import setprop
from dplaingestion.mappers.marc_mapper import PyMARCMapper

class LAPLMARCMapper(PyMARCMapper):                                                       
    def __init__(self, provider_data):
        super(LAPLMARCMapper, self).__init__(provider_data)
        self.mapping_dict.update(
                {lambda t: t == "856": [(self.map_is_shown_by, "u")]})
        self.mapping_dict.update(
                {lambda t: t == "910":  [(self.map_is_shown_at, "a")]})

    def map_data_provider(self):
        super(LAPLMARCMapper, self).map_data_provider(prop="collection")


    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        values = self._get_values(_dict, codes)
        if tag == "910":
            self.extend_prop(prop, _dict, codes, values=values)
            if isinstance(self.mapped_data[prop], list):
                # EDM says this is a single URL, not a list
                self.mapped_data[prop] = self.mapped_data[prop][0]
            self.mapped_data[prop] = ''.join((
            'http://photos.lapl.org/carlweb/jsp/DoSearch?index=z&databaseID=968&terms=',
            self.mapped_data[prop][4:]
            ))

    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        self.extend_prop(prop, _dict, codes)
        if isinstance(self.mapped_data[prop], list):
            # EDM says this is a single URL, not a list
            self.mapped_data[prop] = self.mapped_data[prop][0]

    def map_description(self, _dict, tag, codes):
        '''Need to handle the special case of mapping the 530 field.
        Need to concatenate subfields a & d into one value
        '''
        if tag != "530":
            super(LAPLMARCMapper, self).map_description(_dict, tag, codes)
        else:
            prop = "sourceResource/description"
            values = [' '.join(self._get_values(_dict, 'ad'))]
            self.extend_prop(prop, _dict, codes, values=values)


