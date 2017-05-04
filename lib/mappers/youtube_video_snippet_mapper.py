from __future__ import print_function
from dplaingestion.mappers.mapper import Mapper
import re


class YouTubeVideoSnippetMapper(Mapper):
    '''This is the most basic mapping of the flickr photo api to dc metadata
    It is a very thin model, but you can get isShownAt, isShownBy, title & a
    description from it by just mapping elements.
    '''
    url_video_page = 'https://www.youtube.com/watch?v={id}'

    def map_is_shown_at(self):
        import sys
        print('KEYS:{}'.format(self.provider_data.keys()), file=sys.stderr)
        self.mapped_data['isShownAt'] = self.url_video_page.format(
            id=self.provider_data['id'])

    def map_is_shown_by(self):
        url_big_thumb = \
        self.provider_data['snippet']['thumbnails']['standard']['url']
        self.mapped_data['isShownBy'] = url_big_thumb

    def map_description(self):
        self.update_source_resource(
            {'description': self.provider_data['snippet']['description']})

    def map_subject(self):
        self.update_source_resource(
                {'subject': self.provider_data['snippet']['tags']})

    def map_title(self):
        self.update_source_resource(
            {'title': self.provider_data['snippet']['title']})
