from dplaingestion.mappers.flickr_api_mapper import FlickrMapper
import re


class FlickrSPPLMapper(FlickrMapper):
    def map_subject(self):
        # subject mapping done in map_description()
        pass

    def map_description(self):
        '''Parse out metadata from description field,
        remove from description field and save to relevant fields
        '''
        description = self.provider_data['description']['text']
        matches = re.search('Date:(.+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            self.update_source_resource({'date': matches.group(1).strip()})

        tags = self.provider_data['tags']
        subjects = []
        for tag in tags:
            subjects.append(tag['raw'])
        matches = re.search('Category:( \S+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            subjects.append(matches.group(1).strip().lower())
        self.update_source_resource({'subject': subjects})

        matches = re.search('Previous Identifier:( +.+(.|\n)+/ (.|\n)\S+)', description)
        identifiers = []
        if matches:
            description = description.replace(matches.group(0), '')
            for x in matches.group(1).split(' /'):
                identifiers.append(x.strip())

        matches = re.search('Previous Identifier:( \S+/\S+)', description)
        if matches:
            # strip out 'N/A' values
            description = description.replace(matches.group(0), '')

        matches = re.search('Identifier:( \S+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            identifiers.append(matches.group(1).strip())
        self.update_source_resource({'identifier': identifiers})

        matches = re.search('Type:( \S+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            self.update_source_resource({
                'type':
                matches.group(1).strip().lower()
            })

        matches = re.search('Source:(.+)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            self.update_source_resource({
                'provenance': matches.group(1).strip()
            })

        matches = re.search('Owner:( .+</a>)', description)
        if matches:
            description = description.replace(matches.group(0), '')
            # don't need to map, same as Contributing Institution

        matches = re.search('Rights Information:(.|\n)+', description)
        if matches:
            description = description.replace(matches.group(0), '')
            rights = matches.group(0).replace('Rights Information:', '')
            self.update_source_resource({'rights': rights.strip()})

        # cleaning up description a bit
        self.update_source_resource({'description': description.strip()})
