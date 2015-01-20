from dplaingestion.selector import setprop
from dplaingestion.mappers.marc_mapper import MARCMapper

class LAPLMARCMapper(MARCMapper):                                                       
    def __init__(self, provider_data):
        super(LAPLMARCMapper, self).__init__(provider_data,
                datafield_tag='fields',
                controlfield_tag='fields',
                pymarc=True)

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
            print "VALUES:", str(values), ' TAG ', str(tag)
            self.extend_prop(prop, _dict, codes, values=values)
            if isinstance(self.mapped_data[prop], list):
                # EDM says this is a single URL, not a list
                self.mapped_data[prop] = self.mapped_data[prop][0]
            self.mapped_data[prop] = ''.join((
            'http://photos.lapl.org/carlweb/jsp/DoSearch?index=z&databaseID=968&count=10&initialsearch=true&terms=',
            self.mapped_data[prop][4:]
            ))

    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        print "ISSHOWNBY CALLLED VALUES:"
        self.extend_prop(prop, _dict, codes)
        if isinstance(self.mapped_data[prop], list):
            # EDM says this is a single URL, not a list
            self.mapped_data[prop] = self.mapped_data[prop][0]

