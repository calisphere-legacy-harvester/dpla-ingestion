from dplaingestion.mappers.csu_dspace_mapper import CSU_DSpace_Mapper
from dplaingestion.selector import getprop
import urllib


class CSUCI_Mapper(CSU_DSpace_Mapper):
    def map_type(self):
        # Take type from first file MIME type since descriptive
        # type/genre values don't fit DCMI type vocab

        types = getprop(self.provider_data_source, 'formatName')
        for t in types:
            # Don't accept DSpace-generated txt files
            if 'text/plain' not in t:
                self.update_source_resource({'type': t})
                break
