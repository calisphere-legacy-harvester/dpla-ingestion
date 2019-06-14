from dplaingestion.mappers.flickr_api_mapper import FlickrMapper
import re
from akara import logger


class FlickrSDASMMapper(FlickrMapper):

    def map_description(self):
        pass

    def map_identifier(self):
        '''Parse out identifier values prefixed by "PictionID:" and "Catalog:"
        remove from description field and save to identifier field
        '''
        identifiers = set() # we don't want dups, catalog & filename often
        description = self.provider_data['description']['text']
        matches = re.search('PictionID:(\w+)', description)
        import sys
        if matches:
            description = description.replace(matches.group(0), '')
            identifiers.add(matches.group(1))
        matches = re.search('Catalog:([-.\w]+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            identifiers.add(matches.group(1))
        matches = re.search('Filename:([-.\w]+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            identifiers.add(matches.group(1))
        #cleaning up description a bit
        description = description.replace(' - ', '')
        if len(identifiers):
            self.update_source_resource({'description': description})
            self.update_source_resource({'identifier': [i for i in identifiers]})
