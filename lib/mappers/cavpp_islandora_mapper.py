from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from dplaingestion.selector import getprop

class CAVPP_Islandora_Mapper(OAIDublinCoreMapper):
    '''CAVPP mapper from Islandora'''

    def map_is_shown_at(self):
        '''Grab the identifier with "archive.org" in them
        '''
        ident = self.provider_data['identifier']
        for i in ident:
            if 'archive.org' in i:
                self.mapped_data.update({'isShownAt': i})

    def map_is_shown_by(self):

        if 'identifier.thumbnail' in self.provider_data:
            self.mapped_data.update({'isShownBy': self.provider_data['identifier.thumbnail']})

    def map_provenance(self):
        # Add boilerplate statement to any existing provenance info
        prov_list = []

        if 'provenance' in self.provider_data:
            provenance = self.provider_data['provenance']
            for prov in provenance:
                prov_list.append(prov)
        prov_list.append('The California Revealed Project is supported by the U.S. Institute of Museum and Library Services under the provisions of the Library Services and Technology Act, administered in California by the State Librarian.')
        self.update_source_resource({'provenance': prov_list})

    def map_type(self):
        # If type value = 'item', get type from medium
        if 'type' in self.provider_data:
            if self.provider_data['type'][0] == 'Item':
                try:
                    self.update_source_resource({'type': self.provider_data['medium']})
                except KeyError:
                    pass
            else:
                self.update_source_resource({'type': self.provider_data['type']})
