from dplaingestion.mappers.marc_mapper import PyMARCMapper
from akara import logger

class CSLMARCMapper(PyMARCMapper):
    def __init__(self, provider_data):
        super(CSLMARCMapper, self).__init__(provider_data)
        self.mapping_dict.update({
            lambda t: t == "001": [(self.map_is_shown_at, None),
                                   (self.map_is_shown_by, None)]
        })

    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        if tag == '001':
            id = self._get_values(_dict, codes)[0]
            self.mapped_data[prop] = ''.join(
                ('https://csl.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma', id,
                 '&context=L&vid=01CSL_INST:CSL'))

    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        if tag == '001':
            id = self._get_values(_dict, codes)[0]
            self.mapped_data[prop] = ''.join(
                ('https://na04.alma.exlibrisgroup.com/view/delivery/thumbnail/01CSL_INST/', id))
