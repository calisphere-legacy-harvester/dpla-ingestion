from __future__ import print_function
from dplaingestion.mappers.mapper import Mapper
import re


class FlickrMapper(Mapper):
    '''This is the most basic mapping of the flickr photo api to dc metadata
    It is a very thin model, but you can get isShownAt, isShownBy, title & a
    description from it by just mapping elements.
    '''

    def __init__(self, provider_data, key_prefix=None):
        super(FlickrMapper, self).__init__(provider_data, key_prefix)

    def map_is_shown_at(self):
        urls = self.provider_data['urls']
        for url in urls:
            if url['type'] == 'photopage':
                self.mapped_data['isShownAt'] = url['text']

    @property
    def url_image(self):
        '''Return the url to the image
        This is the URL formula from:
        https://www.flickr.com/services/api/misc.urls.html

        https://farm{farm-id}.staticflickr.com/{server-id}/ \
                {id}_{secret}_[mstzb].jpg
        The z size is 640 on longest side
        The n size is 320 on longest side

        Going to use the 640 size as of 2017-05-01
        '''
        url_image_template = "https://farm{farm}.staticflickr.com/" \
            "{server}/{id}_{secret}_z.jpg"
        return url_image_template.format(
            farm=self.provider_data['farm'],
            server=self.provider_data['server'],
            id=self.provider_data['id'],
            secret=self.provider_data['secret'], )

    def map_is_shown_by(self):
        self.mapped_data['isShownBy'] = self.url_image

    def map_date(self):
        '''It appears that the "taken" date corresponds to the date uploaded
        if there is no EXIF data. For items with EXIF data, hopefully it is
        the date taken == created date.
        '''
        pass

    def map_description(self):
        self.update_source_resource(
            {'description': self.provider_data['description']['text']})

    def map_subject(self):
        tags = self.provider_data['tags']
        subjects = []
        for tag in tags:
            subjects.append(tag['raw'])
        self.update_source_resource({'subject': subjects})

    def map_title(self):
        self.update_source_resource(
            {'title': self.provider_data['title']['text']})

    def map_format(self):
        self.update_source_resource(
            {'format': self.provider_data['media']})

    def map_identifier(self):
        '''Parse out the values prefixed by "PictionID:" and "Catalog:" from
        the description field
        '''
        identifiers = set() # we don't want dups, catalog & filename often
        description = self.provider_data['description']['text']
        matches = re.search('PictionID:(\w+)', description)
        import sys
        if matches:
            identifiers.add(matches.group(1))
        matches = re.search('Catalog:([-.\w]+)', description)
        if matches:
            identifiers.add(matches.group(1))
        matches = re.search('Filename:([-.\w]+)', description)
        if matches:
            identifiers.add(matches.group(1))
        if len(identifiers):
            self.update_source_resource({'identifier': [i for i in identifiers]})

    def map_spatial(self):
        '''Some photos have spatial (location) data'''
        pass
