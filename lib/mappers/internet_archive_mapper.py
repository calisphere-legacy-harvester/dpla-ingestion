from __future__ import print_function
from dplaingestion.mappers.mapper import Mapper


class InternetArchiveMapper(Mapper):
    def map_is_shown_at(self):
        # map 'isShownBy' too
        if 'identifier' in self.provider_data:
            identifier = self.provider_data['identifier']
            self.mapped_data['isShownAt'] = ''.join(
                ('https://archive.org/details/', identifier))
            self.mapped_data['isShownBy'] = ''.join(
                ('https://archive.org/services/img/', identifier))

    def map_relation(self):
        if 'collection' in self.provider_data:
            self.update_source_resource({
                'relation':
                self.provider_data['collection']
            })

    def map_date(self):
        if 'date' in self.provider_data:
            self.update_source_resource({'date': self.provider_data['date']})

    def map_description(self):
        if 'description' in self.provider_data:
            self.update_source_resource({
                'description':
                self.provider_data['description']
            })

    def map_format(self):
        if 'format' in self.provider_data:
            self.update_source_resource({
                'format': self.provider_data['format']
            })

    def map_identifier(self):
        if 'identifier' in self.provider_data:
            self.update_source_resource({
                'identifier':
                self.provider_data['identifier']
            })

    def map_language(self):
        if 'language' in self.provider_data:
            self.update_source_resource({
                'language':
                self.provider_data['language']
            })

    def map_type(self):
        if 'mediatype' in self.provider_data:
            self.update_source_resource({
                'type': self.provider_data['mediatype']
            })

    def map_rights(self):
        if 'licenseurl' in self.provider_data:
            self.update_source_resource({
                'rights':
                self.provider_data['licenseurl']
            })

    def map_publisher(self):
        if 'publisher' in self.provider_data:
            self.update_source_resource({
                'publisher':
                self.provider_data['publisher']
            })

    def map_subject(self):
        if 'subject' in self.provider_data:
            self.update_source_resource({
                'subject':
                self.provider_data['subject']
            })

    def map_title(self):
        if 'title' in self.provider_data:
            self.update_source_resource({'title': self.provider_data['title']})
