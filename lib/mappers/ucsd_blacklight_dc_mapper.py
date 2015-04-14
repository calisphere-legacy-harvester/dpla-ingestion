import json
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify

class UCSDBlacklightDCMapper(DublinCoreMapper):                                                       
    def __init__(self, provider_data): 
        super(UCSDBlacklightDCMapper, self).__init__(provider_data)

    # root mapping
    def map_is_shown_at(self, index=None):
        is_shown_at = ''.join(('https://library.ucsd.edu/dc/object/',
            self.provider_data['id_t']))
        self.mapped_data.update({"isShownAt": is_shown_at})

    def map_is_shown_by(self):
        '''bit complicated. need the files_tesim sub-object with
        key "use"=="image-service". Get the "id" field from this.
        Then construct URL as http://library.ucsd.edu/dc/object/ + id (ARK) +
        /_ + id from  above

        TODO: handle complex objects
        '''
        for obj in self.provider_data['files_tesim']:
            if obj['use'] == 'image-service':
                fid = obj['id']
                break
        else:
            return None
        obj_id =  self.provider_data['id_t']
        is_shown_by = ''.join(('https://library.ucsd.edu/dc/object/',
                obj_id, '/_', fid))
        self.mapped_data.update({"isShownBy": is_shown_by})


    def map_data_provider(self):
        super(UCSDBlacklightDCMapper, self).map_data_provider(prop="collection_json_tesim")

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

    def map_has_view(self):
        pass

    def map_object(self):
        pass

    # sourceResource mapping functions
    def map_collection(self):
        prop = "collection"
        if exists(self.provider_data, prop):
            self.update_source_resource({"collection":
                                         self.provider_data.get(prop)})

###    def source_resource_prop_from_provider_prop_json(self, provider_prop, prop):
###        '''Map the UCSD _json_tesim fields to sourceResource properties.
###        The _json_tesim seems to be a list of one json object, load it 
###        and assigng to prop. Need to know which field in the json we want
###        '''
###        if exists(self.provider_data, provider_prop):
###            objlist = []
###            for o in self.provider_data[provider_prop]:
###                objlist.append(json.loads(o))
###            self.update_source_resource({prop: objlist})
###
    def source_resource_prop_from_provider_json_tesim(self, prop, srcRes_prop=None, sub_key=None):
        '''Get data from a json_tesim.
        Provider prop will be the <prop>_json_tesim
        If sourceResource property has different name, pass in as srcRes_prop.
        sub_key will cause this to only pull forward that key's value from
        the json object in the UCSD field
        '''
        provider_prop = ''.join((prop, '_json_tesim'))
        if not srcRes_prop:
            srcRes_prop = prop
        if not sub_key:
            self.source_resource_orig_to_prop(provider_prop, srcRes_prop)
        else:
            #all stored as list
            values = []
            for obj in self.provider_data.get(provider_prop):
                if obj.get(sub_key):
                    values.append(obj.get(sub_key))
            self.update_source_resource({srcRes_prop: values})

    def map_relationship(self, relation_role_list, field):
        relationships = self.provider_data_source.get('relationship_json_tesim')[0]
        values = []
        for relation, value in relationships.items(): 
            if relation in relation_role_list:
                values.extend(value)
        if len(values):
            self.update_source_resource({field: values})

    def map_contributor(self):
        self.map_relationship(contributor_role_list, 'contributor')

    def map_creator(self):
        relationships = self.provider_data_source.get('relationship_json_tesim',None)
        if relationships:
             if len(relationships[0]) == 1:
                 role, value = relationships[0].items()[0]
                 self.update_source_resource({'creator': value})
             else:
                 self.map_relationship(creator_role_list, 'creator')

    def map_date(self):
        # make DPLA style date object
        # how to handle array of different type date objects, for now just
        # use creation for now, or first if creation not available
        date_list = self.provider_data_source.get('date_json_tesim')
        for date_obj in date_list:
            if date_obj['type'] == 'creation':
                break
        else: # no creation date, use first date
            date_obj = date_list[0]
        date_mapped = dict(end=date_obj['endDate'],
                           begin=date_obj['beginDate'],
                           displayDate=date_obj['value'])
        self.update_source_resource({'date': date_mapped})

    def parse_otherNotes(self, note_type, display_label=None):
        '''Pull out values for the note_type from the otherNote_json_tesim.
        If display_label is specified, only take values when the 
        displayLabel equals the given display_label
        return the values for the note type
        '''
        values = []
        otherNotes = self.provider_data_source.get('otherNote_json_tesim')
        for note in otherNotes:
            if note['type'] == note_type:
                if display_label and display_label == note['displayLabel']:
                    values.append(note['value'])
                else:
                    values.append(note['value'])
        return values if len(values) else None

    def get_otherNotes_field(self, field, display_label=None):
        '''Get a field from that is in the otherNotes.
        '''
        values = self.parse_otherNotes(field)
        if values:
            self.update_source_resource({field: values})

    def map_description(self):
        self.get_otherNotes_field('description')

    def map_extent(self):
        self.source_resource_prop_from_provider_json_tesim('extent')

    def map_format(self):
        values = self.parse_otherNotes('general physical description')
        if values:
            self.update_source_resource({'format': values})

    def map_identifier(self):
        self.get_otherNotes_field('identifier')

###    def map_is_part_of(self):
###        pass

    def map_language(self):
        field = 'language'
        self.source_resource_prop_from_provider_json_tesim(field)
        #fix to match dpla spec
        values = []
        for lang in self.mapped_data["sourceResource"].get(field, []):
            lang['iso639'] = lang['code']
            del lang['code']
            del lang['externalAuthority']
            values.append(lang)
        self.update_source_resource({field:values}) if len(values) else None

    def map_publisher(self):
        self.source_resource_prop_from_provider_json_tesim('publisher')

    def map_relation(self):
        self.source_resource_prop_from_provider_json_tesim('relation')

    def map_rights(self):
        values = []
        for obj in self.provider_data.get('copyright_tesim', []):
            values.append(obj.get('status')) if obj.get('status') else None
            values.append(obj.get('note')) if obj.get('note') else None
            values.append(obj.get('purposeNote')) if obj.get('purposeNote') else None
        self.update_source_resource({'rights':values}) if len(values) else None

    def map_subject(self):
        self.source_resource_orig_to_prop('subject_tesim', 'subject')

### TODO:    def map_temporal(self):
###        pass

    def map_title(self):
        title = self.provider_data_source['title_json_tesim'][0]['name']
        self.update_source_resource({'title': [title]})

    def map_type(self):
        field = 'type'
        self.source_resource_orig_to_prop('resource_type_tesim', field)
        if field in self.mapped_data["sourceResource"]:
            self.mapped_data["sourceResource"][field] = self.mapped_data["sourceResource"][field][0]

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": "California"})

### TODO:    def map_spatial(self):
###        pass

### TODO:   def map_spec_type(self):
###        pass
creator_role_list = [
'Creator',
'Artist',
'Author',
'Composer',
'Creator',
'Filmmaker',
'Photographer',
'Principal investigator',
]

contributor_role_list = [
'Contributor',
'Abridger',
'Actor',
'Adapter',
'Addressee',
'Analyst',
'Animator',
'Annotator',
'Applicant',
'Architect',
'Arranger',
'Art copyist',
'Art director',
'Artistic director',
'Assignee',
'Associated name',
'Attributed name',
'Auctioneer',
'Author in quotations or text abstracts',
'Author of afterword, colophon, etc.',
'Author of dialog',
'Author of introduction, etc.',
'Autographer',
'Bibliographic antecedent',
'Binder',
'Binding designer',
'Blurb writer',
'Book designer',
'Book producer',
'Bookjacket designer',
'Bookplate designer',
'Bookseller',
'Braille embosser',
'Broadcaster',
'Calligrapher',
'Cartographer',
'Caster',
'Censor',
'Choreographer',
'Cinematographer',
'Client',
'Collection registrar',
'Collector',
'Collotyper',
'Colorist',
'Commentator',
'Commentator for written text',
'Compiler',
'Complainant',
'Complainant-appellant',
'Compositor',
'Conceptor',
'Conductor',
'Conservator',
'Consultant',
'Consultant to a project',
'Contestant',
'Contestant-appellant',
'Contestant-appellee',
'Contestee',
'Contestee-appellant',
'Contestee-appellee',
'Contractor',
'Contributor',
'Co-principal investigator',
'Copyright claimant',
'Copyright holder',
'Corrector',
'Correspondent',
'Costume designer',
'Court governed',
'Court reporter',
'Cover designer',
'Cruise',
'Curator',
'Dancer',
'Data contributor',
'Data manager',
'Dedicatee',
'Dedicator',
'Degree granting institution',
'Degree supervisor',
'Delineator',
'Depicted',
'Depositor',
'Designer',
'Director',
'Dissertant',
'Distribution place',
'Distributor',
'Donor',
'Draftsman',
'Dubious author',
'Editor',
'Editor of compilation',
'Editor of moving image work',
'Electrician',
'Electrotyper',
'Enacting jurisdiction',
'Engineer',
'Engraver',
'Etcher',
'Event place',
'Expert',
'Facsimilist',
'Field assistant',
'Field director',
'Film director',
'Film distributor',
'Film editor',
'Film producer',
'First party',
'Forger',
'Former owner',
'Funder',
'Geographic information specialist',
'Honoree',
'Host',
'Host institution',
'Illuminator',
'Illustrator',
'Inscriber',
'Instrumentalist',
'Interviewee',
'Interviewer',
'Inventor',
'Issuing body',
'Jurisdiction governed',
'Laboratory',
'Laboratory assistant',
'Laboratory director',
'Landscape architect',
'Lead',
'Lender',
'Libelant',
'Libelant-appellant',
'Libelant-appellee',
'Libelee',
'Libelee-appellant',
'Libelee-appellee',
'Librettist',
'Licensee',
'Licensor',
'Lighting designer',
'Lithographer',
'Lyricist',
'Manufacture place',
'Manufacturer',
'Marbler',
'Markup editor',
'Medium',
'Metadata contact',
'Metal-engraver',
'Minute taker',
'Moderator',
'Monitor',
'Music copyist',
'Musical director',
'Musician',
'Narrator',
'Onscreen presenter',
'Opponent',
'Organizer',
'Originator',
'Other',
'Owner',
'Panelist',
'Papermaker',
'Patent applicant',
'Patent holder',
'Patron',
'Performer',
'Permitting agency',
'Plaintiff',
'Plaintiff-appellant',
'Plaintiff-appellee',
'Platemaker',
'Praeses',
'Presenter',
'Printer',
'Printer of plates',
'Printmaker',
'Process contact',
'Producer',
'Production company',
'Production designer',
'Production manager',
'Production personnel',
'Production place',
'Programmer',
'Project director',
'Proofreader',
'Provider',
'Publication place',
'Publisher',
'Publishing director',
'Puppeteer',
'Radio director',
'Radio producer',
'Recording engineer',
'Recordist',
'Redaktor',
'Renderer',
'Reporter',
'Repository',
'Research team head',
'Research team member',
'Researcher',
'Respondent',
'Responsible party',
'Restager',
'Restorationist',
'Reviewer',
'Rubricator',
'Scenarist',
'Scientific advisor',
'Screenwriter',
'Scribe',
'Sculptor',
'Second party',
'Secretary',
'Seller',
'Set designer',
'Setting',
'Signer',
'Singer',
'Sound designer',
'Speaker',
'Sponsor',
'Stage director',
'Stage manager',
'Standards body',
'Stereotyper',
'Storyteller',
'Supporting host',
'Surveyor',
'Teacher',
'Technical director',
'Television director',
'Television producer',
'Thesis advisor',
'Transcriber',
'Translator',
'Type designer',
'Typographer',
'University place',
'Vessel',
'Videographer',
'Voice actor',
'Witness',
'Wood engraver',
'Woodcutter',
'Writer of accompanying material',
'Writer of added commentary',
'Writer of added lyrics',
'Writer of added text',
'Writer of introduction',
'Writer of preface',
'Writer of supplementary textual content',
]
