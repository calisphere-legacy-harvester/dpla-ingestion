from dplaingestion.mappers.mapper import Mapper

class UCB_BAMPFA_Mapper(Mapper):
    def __init__(self, provider_data, key_prefix=None):
        super(UCB_BAMPFA_Mapper, self).__init__(provider_data, key_prefix)
        self.metadata = self.provider_data

    def map_is_shown_at(self):
        id_local = str(self.metadata['idnumber_s'])
        is_shown_at = ''.join((
            'https://webapps.cspace.berkeley.edu/bampfa/search/search/?idnumber=',
            id_local, '&displayType=full&maxresults=1&start=1'))

        self.mapped_data.update({"isShownAt": is_shown_at})

    def map_is_shown_by(self):

        blobArray = self.metadata['blob_ss']
        blob = str(blobArray[0])
        is_shown_by = ''.join(
            ('https://webapps.cspace.berkeley.edu/bampfa/imageserver/blobs/',
             blob, '/derivatives/Medium/content'))

        self.mapped_data.update({"isShownBy": is_shown_by})

    def map_creator(self):
        self.update_source_resource({
            'creator': self.metadata.get('artistcalc_s')
        })

    def map_title(self):
        self.update_source_resource({
            'title': self.metadata.get('title_s', None)
        })

    def map_date(self):
        self.update_source_resource({
            'date': self.metadata.get('datemade_s', None)
        })

    def map_extent(self):
        self.update_source_resource({
            'extent': self.metadata.get('measurement_s')
        })

    def map_identifier(self):
        self.update_source_resource({
            'identifier': self.metadata.get('idnumber_s')
        })

    def map_genre(self):
        self.update_source_resource({
            'genre': self.metadata.get('itemclass_s')
        })

    def map_format(self):
        self.update_source_resource({
            'format': self.metadata.get('materials_s')
        })

    def map_provenance(self):
        self.update_source_resource({
            'provenance': self.metadata.get('creditline_s')
        })

    def map_subject(self):
        '''Subject fieldnames are iterative.
        Add all the values from fields beginning with "subject"
        and ending with "_s"'''
        subjects = []
        for mdfield in self.metadata:
            if mdfield.startswith("subject"):
                if mdfield.endswith("_s"):
                    subjects.append(self.metadata[mdfield])
        if subjects:
            self.update_source_resource({'subject': subjects})
