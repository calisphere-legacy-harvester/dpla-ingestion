from dplaingestion.selector import exists, setprop, getprop
from dplaingestion.mappers.marc_mapper import PyMARCMapper
from akara import logger

class UCSBAlephMarcMapper(PyMARCMapper):

    '''Need to be a bit tricky about 856 for this collection'''
    def _map_is_at_values(self, prop, _dict, tag, codes):
        self.extend_prop(prop, _dict, codes)
        usethis = ''
        for data in self.mapped_data.get(prop):
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

    def map_title(self, _dict, tag, index, codes):
        prop = "sourceResource/title"
        if not exists(self.mapped_data, prop):
            setprop(self.mapped_data, prop, [None, None, None])

        values = self._get_values(_dict, "!ch")
        if values:
            # removing trailing slash and leading/trailing whitespaces
            values = [x.rstrip('/') for x in values]
            values = [x.strip() for x in values]
            title = getprop(self.mapped_data, prop)
            title[index] = values
            setprop(self.mapped_data, prop, title)
