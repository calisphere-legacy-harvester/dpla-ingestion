from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from dplaingestion.selector import exists, getprop
from akara import logger
import sys

class CAVPP_Islandora_Mapper(OAIDublinCoreMapper):
    '''CAVPP mapper from Islandora'''

    def map_is_shown_at(self):
        '''truncate identifier.thumbnail value past object ID
        '''
        nodeId = self.provider_data.get('identifier')[0] 
        if 'identifier.thumbnail' in self.provider_data:
            if isinstance(self.provider_data.get('identifier.thumbnail'), str):
                thumbnail = self.provider_data.get('identifier.thumbnail')
            else:
                thumbnail = self.provider_data.get('identifier.thumbnail')[0]

        if '/datastream/TN' in thumbnail:
            isShownAt = thumbnail.split('/datastream/TN')[0]
        elif 'node' in nodeId:
            isShownAt = nodeId

        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    def map_is_shown_by(self):
        if 'identifier.thumbnail' in self.provider_data:
            self.mapped_data.update({'isShownBy': self.provider_data.get('identifier.thumbnail')})

    def map_provenance(self):
        # Add boilerplate statement to any existing provenance info
        prov_list = []

        if 'provenance' in self.provider_data:
            provenance = self.provider_data.get('provenance')
            for prov in provenance:
                prov_list.append(prov)
        prov_list.append('California Revealed is supported by the U.S. Institute of Museum and Library Services under the provisions of the Library Services and Technology Act, administered in California by the State Librarian.')
        self.update_source_resource({'provenance': prov_list})

    def map_type(self):
        # If type value = 'item', get type from medium
        if 'type' in self.provider_data:
            if self.provider_data.get('type')[0] == 'Item':
                try:
                    self.update_source_resource({'type': self.provider_data.get('medium')})
                except KeyError:
                    pass
            else:
                self.update_source_resource({'type': self.provider_data.get('type')})

    def map_extent(self):
        self.source_resource_orig_to_prop('extent', 'extent')

    def map_genre(self):
        self.source_resource_orig_to_prop('genre', 'genre')

    def map_description(self):
        #scrub CAVPP and California Revealed from description
        desc_list =[]

        if 'description' in self.provider_data:
            description = self.provider_data.get('description')
            for desc in description:
                if 'California Audiovisual Preservation Project (CAVPP)' in desc or 'California Revealed' in desc:
                    continue
                else:
                    desc_list.append(desc)
        self.update_source_resource({'description': desc_list})

    def map_contributor(self):
        #scrub 'Unknown' from contributor values

        values = []
        field = "contributor"
        if exists(self.provider_data_source, field):
            # Need to check if string or not
            prop_val = getprop(self.provider_data_source, field)
            if isinstance(prop_val, basestring):
                if 'unknown' in prop_val.lower():
                    pass
                else:
                    values.append(prop_val)
            else:
                # should be list then
                matching = [s for s in prop_val if 'unknown' in s.lower()]
                for prop in matching: prop_val.remove(prop)
                values.extend(prop_val)
            if values:
                self.update_source_resource({'contributor': values})

    def map_creator(self):
        #scrub 'Unknown' from creator values

        values = []
        field = "creator"
        if exists(self.provider_data_source, field):
            # Need to check if string or not
            prop_val = getprop(self.provider_data_source, field)
            if isinstance(prop_val, basestring):
                if 'unknown' in prop_val.lower():
                    pass
                else:
                    values.append(prop_val)
            else:
                # should be list then
                matching = [s for s in prop_val if 'unknown' in s.lower()]
                for prop in matching: prop_val.remove(prop)
                values.extend(prop_val)
            if values:
                self.update_source_resource({'creator': values})

    def map_format(self):
        #scrub 'Unknown' from format values
        fields = ("format", "medium")

        values = []
        for field in fields:
            field = field if not self.prefix else ''.join(
                    (self.prefix, field))
            if exists(self.provider_data_source, field):
                # Need to check if string or not
                prop_val = getprop(self.provider_data_source, field)
                if isinstance(prop_val, basestring):
                    if 'unknown' in prop_val.lower():
                        continue
                    else:
                        values.append(prop_val)
                else:
                    # should be list then
                    matching = [s for s in prop_val if 'unknown' in s.lower()]
                    for prop in matching: prop_val.remove(prop)
                    values.extend(prop_val)
        if values:
            self.update_source_resource({'format': values})

    def map_date(self):
        #scrub 'Unknown' from date values
        fields = ("created", "issued")

        values = []
        for field in fields:
            field = field if not self.prefix else ''.join(
                    (self.prefix, field))
            if exists(self.provider_data_source, field):
                # Need to check if string or not
                prop_val = getprop(self.provider_data_source, field)
                if isinstance(prop_val, basestring):
                    if 'unknown' in prop_val.lower():
                        continue
                    else:
                        values.append(prop_val)
                else:
                    # should be list then
                    matching = [s for s in prop_val if 'unknown' in s.lower()]
                    for prop in matching: prop_val.remove(prop)
                    values.extend(prop_val)
        if values:
            self.update_source_resource({'date': values})

    def map_identifier(self):
        #scrub archive.org and cavpp values from identifier
        fields = ("bibliographicCitation", "identifier", "identifier.ark")

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

    def map_rights(self):
        self.source_resource_prop_to_prop("rights")

    def map_relation(self):
        # subclassed to remove "isPartOf" from fields
        fields = ("conformsTo", "hasFormat", "hasPart", "hasVersion",
                  "isFormatOf", "isReferencedBy", "isReplacedBy",
                  "isRequiredBy", "isVersionOf", "references", "relation",
                  "replaces", "requires")
        self.source_resource_orig_list_to_prop(fields, 'relation')
