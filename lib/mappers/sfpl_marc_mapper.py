from dplaingestion.selector import setprop
from dplaingestion.mappers.marc_mapper import PyMARCMapper

class SFPLMARCMapper(PyMARCMapper):                                                       
    def __init__(self, provider_data):
        super(SFPLMARCMapper, self).__init__(provider_data)

    def map_is_shown_at(self, _dict, tag, codes):
        pass
###        prop = "isShownAt"
###        values = self._get_values(_dict, codes)
###        if tag == "910":
###            self.extend_prop(prop, _dict, codes, values=values)
###            if isinstance(self.mapped_data[prop], list):
###                # EDM says this is a single URL, not a list
###                self.mapped_data[prop] = self.mapped_data[prop][0]
###            self.mapped_data[prop] = ''.join((
###            'http://photos.lapl.org/carlweb/jsp/DoSearch?index=z&databaseID=968&terms=',
###            self.mapped_data[prop][4:]
###            ))

    def map_is_shown_by(self, _dict, tag, codes):
        pass
###        prop = "isShownBy"
###        self.extend_prop(prop, _dict, codes)
###        if isinstance(self.mapped_data[prop], list):
###            # EDM says this is a single URL, not a list
###            self.mapped_data[prop] = self.mapped_data[prop][0]
