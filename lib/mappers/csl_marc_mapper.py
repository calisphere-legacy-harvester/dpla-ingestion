from dplaingestion.mappers.marc_mapper import PyMARCMapper


class CSLMARCMapper(PyMARCMapper):
    def __init__(self, provider_data):
        super(CSLMARCMapper, self).__init__(provider_data)
        self.mapping_dict.update(
            {lambda t: t == "856": [(self.map_is_shown_by, "t")]})
        self.mapping_dict.update(
            {lambda t: t == "001": [(self.map_is_shown_at, None)]})

# http://catalog.library.ca.gov/F/?func=find-b&request=001409080&find_code=SYS

    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        if tag == '001':
            self.mapped_data[prop] = ', '.join(self._get_values(_dict, codes))
            id = self._get_values(_dict, codes)
        self.mapped_data[prop] = ''.join(
            ('http://catalog.library.ca.gov/F/?func=find-b&request=', id,
             '&find_code=SYS'))

    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        self.extend_prop(prop, _dict, codes)
        if isinstance(self.mapped_data[prop], list):
            # EDM says this is a single URL, not a list
            self.mapped_data[prop] = self.mapped_data[prop][0]
