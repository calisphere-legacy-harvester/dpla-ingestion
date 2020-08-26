from dplaingestion.selector import exists
from jsonpath import jsonpath
from akara import logger


#TODO: get from akara.ini?
# url_nuxeo_base = 'https://nuxeo.cdlib.org/Nuxeo/nxpicsfile/default/'
# url_nuxeo_pic_template_med_sz = ''.join((url_nuxeo_base, '{}/Medium:content/'))

url_calisphere_item_base = 'https://calisphere.org/item/'

class UCLDCNuxeoMapper(object):

    def __init__(self, provider_data):
        self.provider_data = provider_data
        self.mapped_data = {"sourceResource": {}}
        self.provider_data_source = jsonpath(self.provider_data, '$.properties')[0]

        # type of mapping - helper functions
   def array_wrap_map(source, dest, dest_field):
        if exists(self.provider_data_source, source):
            arr = [self.provider_data_source.get(source)]
            self.mapped_data[dest].update({dest_field: arr})

    def straight_map_provider_data(source, dest_field):
        if exists(self.provider_data, source):
            self.mapped_data.update({dest_field: self.provider_data.get(source)})

    def straight_map(source, dest, dest_field):
        if exists(self.provider_data_source, source):
            self.mapped_data[dest].update({dest_field: self.provider_data_source.get(source)})

    def aggregate_subfield_map(source, src_subfield, dest, dest_field):
        if exists(self.provider_data_source, source):
            aggregate = [a[src_subfield] for a in self.provider_data_source.get(source)]
            self.mapped_data[dest].update({dest_field: aggregate})
    
    def force_array_map(source, dest, dest_field):
        if exists(self.provider_data_source, source):
            arr = [a for a in self.provider_data_source.get(source)]
            self.mapped_data[dest].update({dest_field: arr})


    def map(self):
        """
        Maps fields from provider_data to fields in mapped_data by:

        1. Mapping, one-to-one, provider_data fields to mapped_data root fields
           via map_root
        2. Mapping, one-to-one, provider_data fields to mapped_data
           sourceResource fields via map_source_resource
        3. Mapping, one-to-many or many-to-one, provider_data fields to
           mapped_data fields
        4. Running any post-mapping logic via update_mapped_fields
        """
        self.map_root()
        self.map_source_resource()
        self.update_mapped_fields()

    """Maps the mapped_data root fields."""
    def map_root(self):
        """Maps base fields shared by all Mappers"""
        self.mapped_data["originalRecord"] = self.provider_data.get("originalRecord", {})
        self.straight_map('ucldc_schema:source', 'originalRecord', 'source')
        self.straight_map('ucldc_schema:physlocation', 'originalRecord', 'location')
        self.map_rights_holder()
        self.map_rights_note()
        self.straight_map('ucldc_schema:rightsstartdate', 'originalRecord', 'dateCopyrighted')
        self.straight_map('ucldc_schema:transcription', 'originalRecord', 'transcription')

        id = self.provider_data.get("id", "")
        _id = self.provider_data.get("_id")
        at_id = "http://ucldc.cdlib.org/api/items/" + id
        self.mapped_data.update({"id": id, "_id": _id, "@id": at_id})

        for prop in ("ingestDate", "ingestType", "ingestionSequence"):
            self.mapped_data.update({prop: self.provider_data.get(prop)})

        # map_provider
        self.straight_map_provider_data('provider', 'provider')
        # map_data_provider
        self.straight_map_provider_data('source', 'dataProvider')
        self.map_is_shown_at()

    # originalRecord mapping
    def map_rights_holder(self):
        rightsholders = []
        if exists(self.provider_data_source, 'ucldc_schema:rightsholder'):
            rightsholders = [rh['name'] for rh in self.provider_data_source.get('ucldc_schema:rightsholder')]
        if exists(self.provider_data_source, 'ucldc_schema:rightscontact'):
            rightsholders.append(self.provider_data_source.get('ucldc_schema:rightscontact'))
        if rightsholders:
            self.mapped_data["originalRecord"].update({'rightsHolder': rightsholders})

    def map_rights_note(self):
        rightsnotes = []
        if exists(self.provider_data_source, 'ucldc_schema:rightsnotice'):
            rightsnotes.append(self.provider_data_source.get('ucldc_schema:rightsnotice'))
        if exists(self.provider_data_source, 'ucldc_schema:rightsnote'):
            rightsnotes.append(self.provider_data_source.get('ucldc_schema:rightsnote'))
        if rightsnotes:
            self.mapped_data["originalRecord"].update({'rightsNote': rightsnotes})

        # root mapping

    def map_is_shown_at(self):
        # these live on calisphere. so the isShownAt is:
        # https://calisphere.org/item/<ID>
        self.mapped_data.update({"isShownAt": url_calisphere_item_base +
            self.provider_data.get('uid', None)})
        logger.error("keys in PDS:{}".format(self.provider_data.keys()))
        self.mapped_data.update({"isShownBy":
                                  self.provider_data.get('isShownBy')})

    def map_source_resource(self):
        """Mapps the mapped_data sourceResource fields."""
        aggregate_subfield_map('ucldc_schema:contributor', 'name', 'sourceResource', 'contributor')
        aggregate_subfield_map('ucldc_schema:creator', 'name', 'sourceResource', 'creator')
        aggregate_subfield_map('ucldc_schema:date', 'date', 'sourceResource', 'date')
        self.map_description()          #pass
        straight_map('ucldc_schema:extent', 'sourceResource', 'extent')
        straight_map('ucldc_schema:physdesc', 'sourceResource', 'format')
        self.map_identifier()           #pass
        self.map_is_part_of()           #pass
        self.map_language()             #pass
        force_array_map('ucldc_schema:publisher', 'sourceResource', 'publisher')
        self.map_relation()             #pass
        self.map_rights()               #pass
        self.map_spatial()              #pass
        # self.map_spec_type()            #pass
        # self.map_state_located_in()     #pass
        self.map_subject()              #pass
        force_array_map('ucldc_schema:temporalcoverage', 'sourceResource', 'temporalCoverage')
        array_wrap_map('dc:title', 'sourceResource', 'title')
        straight_map('ucldc_schema:type', 'sourceResource', 'type')
        aggregate_subfield_map('ucldc_schema:formgenre', 'heading', 'sourceResource', 'genre')
        straight_map('ucldc_schema:provenance', 'sourceResource', 'provenance')
        force_array_map('ucldc_schema:alternativetitle', 'sourceResource', 'alternativeTitle')

    # sourceResource mapping
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
            'prodcredits': 'Production Credits',
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
            if self.type_labels.get(data_type, ''):
                data_type = self.type_labels.get(data_type, '')
                logger.error("Data Readable:{}".format(data_type))
            item = data.get('item', '')
            if item:
                unpacked = u'{}: {}'.format(data_type, item)
            else:
                unpacked = ''
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
            self.mapped_data["sourceResource"].update({'description':desc_data})

    def map_identifier(self):
        identifiers = []
        if exists(self.provider_data_source, 'ucldc_schema:identifier'):
            identifiers.append(self.provider_data_source.get('ucldc_schema:identifier'))
        if exists(self.provider_data_source, 'ucldc_schema:localidentifier'):
            localids = self.provider_data_source.get('ucldc_schema:localidentifier')
            identifiers.extend(localids)
        if identifiers:
            self.mapped_data["sourceResource"].update({'identifier': identifiers})

    def map_language(self):
        languages = []
        if exists(self.provider_data_source, 'ucldc_schema:language'):
            for lang in self.provider_data_source.get('ucldc_schema:language'):
                if lang['language']:
                    languages.append(lang['language'])
                if lang['languagecode']:
                    languages.append(lang['languagecode'])
        self.mapped_data["sourceResource"].update({'language': [{'iso639_3': l} for l in languages]})

    def map_relation(self):
        relations = []
        if exists(self.provider_data_source, 'ucldc_schema:relatedresource'):
            relations = [rr for rr in self.provider_data_source.get('ucldc_schema:relatedresource')]
        if relations:
            self.mapped_data["sourceResource"].update({'relation': relations})

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
        self.mapped_data["sourceResource"].update({'rights': rights})

    def map_spatial(self):
        spatial = []
        if exists(self.provider_data_source, 'ucldc_schema:place'):
            for place in self.provider_data_source.get('ucldc_schema:place'):
                if place['name']:
                    spatial.append(place['name'])
                if place['coordinates']:
                    spatial.append(place['coordinates'])
        if spatial:
            self.mapped_data["sourceResource"].update({'spatial': [{'text': s} for s in spatial]})

    def map_subject(self):
        if exists(self.provider_data_source, 'ucldc_schema:subjecttopic'):
            subjects = [st['heading'] for st in self.provider_data_source.get('ucldc_schema:subjecttopic')]
            subjects.extend([sn['name'] for sn in self.provider_data_source.get('ucldc_schema:subjectname')])
            self.mapped_data["sourceResource"].update({'subject': subjects})