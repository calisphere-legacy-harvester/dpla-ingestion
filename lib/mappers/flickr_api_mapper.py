from dplaingestion.mappers.mapper import Mapper


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

        https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}_[mstzb].jpg
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
        self.mapped_data['sourceResource']['date'] = \
            self.provider_data['dates']['taken']

    def map_description(self):
        self.mapped_data['sourceResource']['description'] = \
                self.provider_data['description']['text']

    def map_subject(self):
        tags = self.provider_data['tags']
        subjects = []
        for tag in tags:
            subjects.append(tag['text'])
        self.mapped_data['sourceResource']['subject'] = subjects

    def map_title(self):
        self.mapped_data['sourceResource']['title'] = self.provider_data[
            'title']['text']

    def map_format(self):
        self.mapped_data['sourceResource']['format'] = \
            self.provider_data['media']

    def map_spatial(self):
        '''Some photos have spatial (location) data'''
        pass
