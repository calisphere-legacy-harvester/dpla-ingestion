from dplaingestion.selector import setprop
from dplaingestion.mappers.marc_mapper import PyMARCMapper
from akara import logger

class SFPLMARCMapper(PyMARCMapper):                                                       
    def __init__(self, provider_data):
        super(SFPLMARCMapper, self).__init__(provider_data)
        self.mapping_dict.update({
            lambda t: t == "907":               [(self.map_is_shown_at, "a")],
            lambda t: t == "856":               [(self.map_is_shown_by, "u")],
            })

    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        if tag == '907':
            id_str = self._get_values(_dict, codes)[0]
            id = id_str[1:][:-1]
            self.mapped_data[prop] = ''.join((
                'http://sflib1.sfpl.org:82/record=',
                id
            ))

    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        # Take first one listed
#        logger.error('CURRENT IS SHOWNBY:{}'.format(self.mapped_data.get(prop, None)))
        if not self.mapped_data.get(prop, None) or ("webbie" not in self.mapped_data.get(prop, None)):
            # not yet set
            if tag == '856':
                url = self._get_values(_dict, codes)[0]
                logger.error('SETTING IS SHOWNBY:{}'.format(url))
                self.mapped_data[prop] = url
