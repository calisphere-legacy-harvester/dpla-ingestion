from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists
from jsonpath import jsonpath

#TODO: get from akara.ini?
url_nuxeo_base = 'https://nuxeo.cdlib.org/Nuxeo/nxpicsfile/default/'

url_nuxeo_pic_template_med_sz = ''.join((url_nuxeo_base, '{}/Medium:content/'))

class UCLDCNuxeoMapper(Mapper):

    def __init__(self, provider_data):
        super(UCLDCNuxeoMapper, self).__init__(provider_data)
        self.provider_data_source = jsonpath(self.provider_data, '$.properties')[0]

    # root mapping
    def map_is_shown_at(self):
        self.mapped_data.update({"isShownAt": 'http://example.edu'})
        self.mapped_data.update({"isShownBy": 
                url_nuxeo_pic_template_med_sz.format(self.provider_data['uid'])})

    def map_contributor(self):
        if exists(self.provider_data_source, 'ucldc_schema:contributor'):
            contributors = [contrib['name'] for contrib in self.provider_data_source.get('ucldc_schema:contributor')]
            self.update_source_resource({'contributor': contributors})

    def map_creator(self):
        if exists(self.provider_data_source, 'ucldc_schema:creator'):
            names = [creator['name'] for creator in self.provider_data_source.get('ucldc_schema:creator')]
            self.update_source_resource({'creator': names})


    def map_date(self):
        if exists(self.provider_data_source, 'ucldc_schema:date'):
            dates = [date['date'] for date in self.provider_data_source.get('ucldc_schema:date')]
            self.update_source_resource({'date': [{'date': d} for d in dates]})

    def map_description(self):
        if exists(self.provider_data_source, 'ucldc_schema:description'):
            self.update_source_resource({'description':self.provider_data_source.get('ucldc_schema:description')})

    def map_extent(self):
        if exists(self.provider_data_source, 'ucldc_schema:extent'):
            self.update_source_resource({'extent':self.provider_data_source.get('ucldc_schema:extent')})

    def map_format(self):
        # format
        if exists(self.provider_data_source, 'ucldc_schema:physdesc'):
            self.update_source_resource({'format':self.provider_data_source.get('ucldc_schema:physdesc')})
        # genre 
        if exists(self.provider_data_source, 'ucldc_schema:formgenre'):
            genres = [fg['heading'] for fg in self.provider_data_source.get('ucldc_schema:formgenre')]
            self.update_source_resource({'genre': genres})

    def map_identifier(self):
        if exists(self.provider_data_source, 'ucldc_schema:localidentifier'):
            self.update_source_resource({'identifier': self.provider_data_source.get('ucldc_schema:localidentifier')})

    def map_language(self):
        if exists(self.provider_data_source, 'ucldc_schema:language'):
            # map language and languagecode?            
            languages = [lang['language'] for lang in self.provider_data_source.get('ucldc_schema:language')]
            languages.extend([lang['languagecode'] for lang in self.provider_data_source.get('ucldc_schema:language')])
            self.update_source_resource({'language': [{'iso639_3': l} for l in languages]})

    def map_title(self):
        # title
        if exists(self.provider_data_source, 'dc:title'):
            self.update_source_resource({'title': self.provider_data_source.get('dc:title')})    
        # alt title
        if exists(self.provider_data_source, 'ucldc_schema:alternativetitle'):
            alt_titles = [at for at in self.provider_data_source.get('ucldc_schema:alternativetitle')]
            self.update_source_resource({'alternativeTitle': alt_titles})

    def map_rights(self):
        if exists(self.provider_data_source, 'ucldc_schema:rightsstatus'):
            self.update_source_resource({'rights':self.provider_data_source.get('ucldc_schema:rightsstatus')})
