from dplaingestion.mappers.flickr_api_mapper import FlickrMapper
import re


class FlickrSDASMMapper(FlickrMapper):

    def map_description(self):
        pass

    def map_title(self):
        pass

    def map_identifier(self):
        '''Parse out identifier values prefixed by "PictionID:" and "Catalog:"
        remove from description field and save to identifier field
        '''
        identifiers = set() # we don't want dups, catalog & filename often
        description = self.provider_data.get('description',{}).get('text')
        if description:
            matches = re.search('PictionID:([-.\w]+)', description, re.IGNORECASE)
            import sys
            if matches:
                description = description.replace(matches.group(0), '')
                identifiers.add(matches.group(1))
            matches = re.search('Catalog:([-.\w]+)', description, re.IGNORECASE)
            if matches:
                description = description.replace(matches.group(0), '')
                identifiers.add(matches.group(1))
            matches = re.search('Filename:([-.\w]+)', description, re.IGNORECASE)
            if matches:
                description = description.replace(matches.group(0), '')
                identifiers.add(matches.group(1))

            '''Parse out date and title'''
            matches = re.search('Date on Neg:.[\d/]+', description, re.IGNORECASE)
            if matches:
                description = description.replace(matches.group(0), '')
                date = matches.group(0).replace('Date on Neg:', '')
                self.update_source_resource({
                    'date': date.strip()
                })
            matches = re.search('Date:.[\d/]+', description, re.IGNORECASE)
            if matches:
                description = description.replace(matches.group(0), '')
                date = matches.group(0).replace('Date:', '')
                self.update_source_resource({
                    'date': date.strip()
                })
            matches = re.search('Title:.+?(?= -)', description, re.IGNORECASE)
            if matches:
                description = description.replace(matches.group(0), '')
                title = matches.group(0).replace('Title:', '')
                self.update_source_resource({
                    'title': title.strip()
                })
            else:
                self.update_source_resource({
                    'title': self.provider_data.get('title',{}).get('text')
                })

            #cleaning up description a bit
            description = description.replace(' - ', '')
            if len(identifiers):
                self.update_source_resource({'identifier': [i for i in identifiers]})
            self.update_source_resource({'description': description})
