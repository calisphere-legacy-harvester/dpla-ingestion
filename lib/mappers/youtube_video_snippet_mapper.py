from __future__ import print_function
from dplaingestion.mappers.mapper import Mapper


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
            id=self.provider_data.get('id'))

    def map_is_shown_by(self):
        thumbnails = self.provider_data.get('snippet',{}).get('thumbnails')
        try:
            url_thumb = thumbnails['standard']['url']
        except KeyError:
            try:
                url_thumb = thumbnails['high']['url']
            except KeyError:
                try:
                    url_thumb = thumbnails['medium']['url']
                except KeyError:
                    url_thumb = thumbnails['default']['url']

        self.mapped_data['isShownBy'] = url_thumb

    def map_description(self):
        self.update_source_resource(
            {'description': self.provider_data.get('snippet',{}).get('description')})

    def map_subject(self):
        if 'tags' in self.provider_data['snippet']:
            self.update_source_resource(
                {'subject': self.provider_data.get('snippet',{}).get('tags')})

    def map_title(self):
        self.update_source_resource(
            {'title': self.provider_data.get('snippet',{}).get('title')})
