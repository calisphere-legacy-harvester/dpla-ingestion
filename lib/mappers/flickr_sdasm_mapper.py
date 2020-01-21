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
            matches = re.search('PictionID:([-.\w]+)', description)
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

            '''Parse out date and title'''
            matches = re.search('Date on Neg:.[\d/]+', description)
            if matches:
                description = description.replace(matches.group(0), '')
                date = matches.group(0).replace('Date on Neg:', '')
                self.update_source_resource({
                    'date': date.strip()
                })
            matches = re.search('Date:.[\d/]+', description)
            if matches:
                description = description.replace(matches.group(0), '')
                date = matches.group(0).replace('Date:', '')
                self.update_source_resource({
                    'date': date.strip()
                })
            matches = re.search('Title:(.+)(?=Details)', description)
            if matches:
                description = description.replace(matches.group(0), '')
                self.update_source_resource({
                    'title': matches.group(1).strip()
                })
            else:
                self.update_source_resource({
                    'title': self.provider_data.get('title',{}).get('text')
                })

            #cleaning up description a bit
            description = description.replace(' - ', '')
            if len(identifiers):
                self.update_source_resource({'description': description})
                self.update_source_resource({'identifier': [i for i in identifiers]})
