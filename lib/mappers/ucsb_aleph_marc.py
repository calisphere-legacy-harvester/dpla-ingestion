from dplaingestion.mappers.marc_mapper import PyMARCMapper

class UCSBAlephMarcMapper(PyMARCMapper):
    '''Need to be a bit tricky about 856 for this collection'''
    def _map_is_at_values(self, prop, _dict, tag, codes):
        self.extend_prop(prop, _dict, codes)
        usethis = ''
        for data in self.mapped_data[prop]:
            if 'http://www.library.ucsb.edu/OBJID/' in data:
                usethis = data
                break
        self.mapped_data[prop] = usethis

    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        self._map_is_at_values(prop, _dict, tag, codes)

    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        self._map_is_at_values(prop, _dict, tag, codes)

