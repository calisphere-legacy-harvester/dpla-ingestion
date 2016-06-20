from dplaingestion.mappers.mapper import Mapper
from dplaingestion.selector import exists
from jsonpath import jsonpath
from akara import logger


#TODO: get from akara.ini?
url_nuxeo_base = 'https://nuxeo.cdlib.org/Nuxeo/nxpicsfile/default/'

url_nuxeo_pic_template_med_sz = ''.join((url_nuxeo_base, '{}/Medium:content/'))

url_calisphere_item_base = 'https://calisphere.org/item/'

class UCLDCNuxeoMapper(Mapper):

    def __init__(self, provider_data):
        super(UCLDCNuxeoMapper, self).__init__(provider_data)
        self.provider_data_source = jsonpath(self.provider_data, '$.properties')[0]

    def map_source_resource(self):
        super(UCLDCNuxeoMapper, self).map_source_resource()
        self.map_alt_title()
        self.map_genre()

    def map_original_record(self):
        super(UCLDCNuxeoMapper, self).map_original_record()
        if not self.mapped_data['originalRecord']: #during testing, this is None
            self.mapped_data['originalRecord'] = {}
        self.map_source()
        self.map_provenance()
        self.map_location()
        self.map_rights_holder()
        self.map_rights_note()
        self.map_copyrighted()
        self.map_transcription()

    def update_original_record(self, _dict):
        """
        Updates the mapped_data originalRecord field with the given dictionary.
        """
        self.mapped_data["originalRecord"].update(_dict)

    # root mapping
    def map_is_shown_at(self):
        # these live on calisphere. so the isShownAt is:
        # https://calisphere.org/item/<ID>
        self.mapped_data.update({"isShownAt": url_calisphere_item_base +
            self.provider_data.get('uid', None)})
        logger.error("keys in PDS:{}".format(self.provider_data.keys())) 
        self.mapped_data.update({"isShownBy":
                                  self.provider_data.get('isShownBy')})

    # sourceResource mapping
    def map_contributor(self):
        if exists(self.provider_data_source, 'ucldc_schema:contributor'):
            contributors = [contrib['name'] for contrib in self.provider_data_source.get('ucldc_schema:contributor')]
            self.update_source_resource({'contributor': contributors})

    def map_alt_title(self):
        if exists(self.provider_data_source, 'ucldc_schema:alternativetitle'):
            alt_titles = [at for at in self.provider_data_source.get('ucldc_schema:alternativetitle')]
            self.update_source_resource({'alternativeTitle': alt_titles})

    def map_creator(self):
        if exists(self.provider_data_source, 'ucldc_schema:creator'):
            names = [creator['name'] for creator in self.provider_data_source.get('ucldc_schema:creator')]
            self.update_source_resource({'creator': names})


    def map_date(self):
        if exists(self.provider_data_source, 'ucldc_schema:date'):
            dates = [date['date'] for date in self.provider_data_source.get('ucldc_schema:date')]
            self.update_source_resource({'date': [{'displayDate': d} for d in dates]})
    
    type_labels = {
            'scopecontent': 'Scope/Content',
            'acquisition': 'Acquisition',
            'bibliography': 'Bibliography',
            'bioghist': 'Biography/History',
            'biography': 'Biography/History',
            'biographical': 'Biography/History',
            'citereference': 'Citation/Reference',
            'conservation': 'Conservation History',
            'creationprod': 'Creation/Production Credits',
            'date': 'Date Note',
            'exhibitions': 'Exhibitions',
            'funding': 'Funding',	
            'marks': 'Annotations/Markings',
            'language': 'Language',
            'performers': 'Performers',
            'prefercite': 'Preferred Citation',
            'venue': 'Venue',
            'condition': 'Condition',
            'medium': 'Medium',
            'technique': 'Technique'
    }

    def unpack_description_data(self, data):
        '''See if dict or basestring and unpack value'''
        unpacked = None
        if isinstance(data, dict):
            #make robust to not break
            data_type = data.get('type', '').strip()
            logger.error("Data CODE:{}".format(data_type))
            if data_type:
                data_type = self.type_labels.get(data_type, '')
                logger.error("Data Readable:{}".format(data_type))
            item = data.get('item', '')
            unpacked = u'{}: {}'.format(data_type, item)
        else:
            unpacked = data
        return unpacked

    def map_description(self):
        desc_data = []
        if exists(self.provider_data_source, 'ucldc_schema:description'):
            raw_data = self.provider_data_source.get('ucldc_schema:description')
            if isinstance(raw_data, list):
                for d in raw_data:
                    desc_data.append(self.unpack_description_data(d))
            else:
                desc_data.append(self.unpack_description_data(raw_data))
            self.update_source_resource({'description':desc_data})

    def map_extent(self):
        if exists(self.provider_data_source, 'ucldc_schema:extent'):
            self.update_source_resource({'extent':self.provider_data_source.get('ucldc_schema:extent')})

    def map_format(self):
        if exists(self.provider_data_source, 'ucldc_schema:physdesc'):
            self.update_source_resource({'format':self.provider_data_source.get('ucldc_schema:physdesc')})

    def map_genre(self):
        if exists(self.provider_data_source, 'ucldc_schema:formgenre'):
            genres = [fg['heading'] for fg in self.provider_data_source.get('ucldc_schema:formgenre')]
            self.update_source_resource({'genre': genres})

    def map_identifier(self):
        identifiers = []
        if exists(self.provider_data_source, 'ucldc_schema:identifier'):
            identifiers.append(self.provider_data_source.get('ucldc_schema:identifier'))
        if exists(self.provider_data_source, 'ucldc_schema:localidentifier'):
            localids = self.provider_data_source.get('ucldc_schema:localidentifier')
            identifiers.extend(localids)
        if identifiers:
            self.update_source_resource({'identifier': identifiers})

    def map_language(self):
        languages = []
        if exists(self.provider_data_source, 'ucldc_schema:language'):
            for lang in self.provider_data_source.get('ucldc_schema:language'):
                if lang['language']:
                    languages.append(lang['language'])
                if lang['languagecode']:
                    languages.append(lang['languagecode'])
        self.update_source_resource({'language': [{'iso639_3': l} for l in languages]})

    def map_publisher(self):
        if exists(self.provider_data_source, 'ucldc_schema:publisher'):
            publishers = [pub for pub in self.provider_data_source.get('ucldc_schema:publisher')]
            self.update_source_resource({'publisher': publishers})

    def map_relation(self):
        relations = []
        if exists(self.provider_data_source, 'ucldc_schema:relatedresource'):
            relations = [rr for rr in self.provider_data_source.get('ucldc_schema:relatedresource')]
        if relations:
            self.update_source_resource({'relation': relations})

    def map_rights_codes(self, rights_str):
        '''Map the "coded" values of the rights status to a nice one for 
        display
        '''
        decoded = rights_str
        if rights_str == 'copyrighted':
            decoded = 'Copyrighted'
        elif rights_str == 'publicdomain':
            decoded = 'Public Domain'
        elif rights_str == 'unknown':
            decoded = 'Copyright Unknown'
        return decoded

    def map_rights(self):
        rights = []
        if exists(self.provider_data_source, 'ucldc_schema:rightsstatus'):
            rights_status = self.provider_data_source.get('ucldc_schema:rightsstatus') 
            rights.append(self.map_rights_codes(rights_status))
        if exists(self.provider_data_source, 'ucldc_schema:rightsstatement'):
            rights.append(self.provider_data_source.get('ucldc_schema:rightsstatement'))
        self.update_source_resource({'rights': rights}) 

    def map_spatial(self):
        spatial = []
        if exists(self.provider_data_source, 'ucldc_schema:place'):
            for place in self.provider_data_source.get('ucldc_schema:place'):
                if place['name']:
                    spatial.append(place['name'])
                if place['coordinates']:
                    spatial.append(place['coordinates'])
        if spatial:
            self.update_source_resource({'spatial': [{'text': s} for s in spatial]})

    def map_subject(self):
        if exists(self.provider_data_source, 'ucldc_schema:subjecttopic'):
            subjects = [st['heading'] for st in self.provider_data_source.get('ucldc_schema:subjecttopic')]
            subjects.extend([sn['name'] for sn in self.provider_data_source.get('ucldc_schema:subjectname')])
            self.update_source_resource({'subject': subjects}) 

    def map_temporal(self):
        if exists(self.provider_data_source, 'ucldc_schema:temporalcoverage'):
            self.update_source_resource({'temporalCoverage': [tc for tc in self.provider_data_source.get('ucldc_schema:temporalcoverage')]}) 

    def map_title(self):
        if exists(self.provider_data_source, 'dc:title'):
            titles = [self.provider_data_source.get('dc:title')]
            self.update_source_resource({'title': titles})

    def map_type(self):
        if exists(self.provider_data_source, 'ucldc_schema:type'):
            self.update_source_resource({'type': self.provider_data_source.get('ucldc_schema:type')})

    # originalRecord mapping
    def map_source(self):
        if exists(self.provider_data_source, 'ucldc_schema:source'):
            self.update_original_record({'source': self.provider_data_source.get('ucldc_schema:source')})

    def map_provenance(self):
        if exists(self.provider_data_source, 'ucldc_schema:provenance'):
            self.update_original_record({'provenance': self.provider_data_source.get('ucldc_schema:provenance')})

    def map_location(self):
        if exists(self.provider_data_source, 'ucldc_schema:physlocation'):
            self.update_original_record({'location': self.provider_data_source.get('ucldc_schema:physlocation')})

    def map_rights_holder(self):
        rightsholders = []
        if exists(self.provider_data_source, 'ucldc_schema:rightsholder'):
            rightsholders = [rh['name'] for rh in self.provider_data_source.get('ucldc_schema:rightsholder')]
        if exists(self.provider_data_source, 'ucldc_schema:rightscontact'):
            rightsholders.append(self.provider_data_source.get('ucldc_schema:rightscontact')) 
        if rightsholders:
            self.update_original_record({'rightsHolder': rightsholders})

    def map_rights_note(self):
        rightsnotes = []
        if exists(self.provider_data_source, 'ucldc_schema:rightsnotice'):        
            rightsnotes.append(self.provider_data_source.get('ucldc_schema:rightsnotice'))
        if exists(self.provider_data_source, 'ucldc_schema:rightsnote'):
            rightsnotes.append(self.provider_data_source.get('ucldc_schema:rightsnote'))
        if rightsnotes:
            self.update_original_record({'rightsNote': rightsnotes})

    def map_copyrighted(self):
        if exists(self.provider_data_source, 'ucldc_schema:rightsstartdate'):
           self.update_original_record({'dateCopyrighted': self.provider_data_source.get('ucldc_schema:rightsstartdate')}) 

    def map_transcription(self):
        if exists(self.provider_data_source, 'ucldc_schema:transcription'):
          self.update_original_record({'transcription': self.provider_data_source.get('ucldc_schema:transcription')})
