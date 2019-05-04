from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from dplaingestion.selector import exists, getprop
from akara import logger

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

    def map_description(self):
        #scrub CAVPP and California Revealed from description
        desc_list =[]

        if 'description' in self.provider_data:
            description = self.provider_data['description']
            for desc in description:
                if 'California Audiovisual Preservation Project (CAVPP)' in desc or 'California Revealed' in desc:
                    continue
                else:
                    desc_list.append(desc)
        self.update_source_resource({'description': desc_list})

    def map_date(self):
        self.source_resource_orig_to_prop("created", "date")

    def map_identifier(self):
        #scrub archive.org and cavpp values from identifier
        fields = ("bibliographicCitation", "identifier")

        values = []
        for field in fields:
            field = field if not self.prefix else ''.join(
                    (self.prefix, field))
            if exists(self.provider_data_source, field):
                # Need to check if string or not
                prop_val = getprop(self.provider_data_source, field)
                if isinstance(prop_val, basestring):
                    if 'archive.org' in prop_val or 'cavpp' in prop_val:
                        continue
                    else:
                        values.append(prop_val)
                else:
                    # should be list then
                    matches = ['archive.org', 'cavpp']
                    matching = [s for s in prop_val if any(xs in s for xs in matches)]
                    for prop in matching: prop_val.remove(prop)

                    values.extend(prop_val)
        if values:
            self.update_source_resource({'identifier': values})
