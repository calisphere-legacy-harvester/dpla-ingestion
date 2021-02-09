import os
import re
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
from akara import module_config

URL_OAC_CONTENT_BASE = module_config().get(
    'url_oac_content',
    os.environ.get('URL_OAC_CONTENT_BASE', 'http://content.cdlib.org'))

# collection 25496 has coverage values like A0800 & A1000
# drop these
Anum_re = re.compile('A\d\d\d\d')


class OAC_DCMapper(object):
    '''Mapper for OAC xml feed objects'''
    def __init__(self, provider_data):
        self.provider_data = provider_data
        self.mapped_data = {"sourceResource": {}}

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
        self.map_source_resource() # pass

    def map_root(self):
        """Maps the mapped_data root fields."""

        # map_original_record and map_ids and map_ingest_data and map_is_shown_at
        self.mapped_data.update({
            "originalRecord": self.provider_data.get("originalRecord")
            "id": self.provider_data.get("id", ""), 
            "_id": self.provider_data.get("_id"), 
            "@id": "http://ucldc.cdlib.org/api/items/" + self.provider_data.get("id", ""),
            "ingestDate": self.provider_data.get("ingestDate"),
            "ingestType": self.provider_data.get("ingestType"),
            "ingestionSequence": self.provider_data.get("ingestionSequence"),
            "isShownAt": self.provider_data.get('isShownAt', None), # This is set in select-oac-id but must be added to mapped data
        })

        # map provider
        if exists(self.provider_data, "provider"):
            self.mapped_data.update({"provider":
                                     self.provider_data.get("provider")})

        # map_data_provider
        if 'originalRecord' in self.provider_data:  # guard weird input
            if 'collection' in self.provider_data.get('originalRecord'):
                self.mapped_data.update({
                    "dataProvider":
                    self.provider_data.get('originalRecord',{}).get('collection')
                })

        # map_is_shown_by - already set in select_oac_id to base of {{obj url}}/thumbnail
        if self.get_best_oac_image():
            self.mapped_data.update({"isShownBy": self.get_best_oac_image(), })

        # map_item_count
        '''Use reference-image-count value to determine compound objects.
        NOTE: value is not always accurate so only determines complex (-1)
        or not complex (no item_count value)
        '''
        image_count = 0
        if 'originalRecord' in self.provider_data:  # guard weird input
            ref_image_count = self.provider_data.get('originalRecord',{}).get(
                'reference-image-count', None)
            if ref_image_count:
                image_count = ref_image_count[0]['text']
            if image_count > "1":
                self.mapped_data.update({"item_count": "-1"})

    def map_source_resource(self):
        """Mapps the mapped_data sourceResource fields."""
        self.source_resource_prop_to_prop("contributor")
        self.source_resource_prop_to_prop("creator")
        self.source_resource_prop_to_prop("date", suppress_attribs={'q': 'dcterms:dateCopyrighted'})
        self.map_copyrightDate()
        self.source_resource_orig_list_to_prop(("abstract", "description", "tableOfContents"), 'description')
        self.source_resource_prop_to_prop("extent")
        self.source_resource_prop_to_prop("format", suppress_attribs={'q': 'x'})
        self.source_resource_orig_list_to_prop(("bibliographicCitation", "identifier"), 'identifier')
        self.source_resource_prop_to_prop("language")
        self.source_resource_prop_to_prop("publisher")
        self.source_resource_orig_list_to_prop(("accessRights", "rights"), 'rights')
        self.map_spatial()
        self.update_source_resource({"stateLocatedIn": [{"name": "California"}]})
        self.map_subject()
        self.map_temporal()
        self.source_resource_prop_to_prop("title", suppress_attribs={'q': 'alternative'})
        self.map_alternative_title()
        self.source_resource_prop_to_prop("type", suppress_attribs={'q': 'genreform'})
        self.map_genre()
        self.source_resource_prop_to_prop("provenance")

    def update_source_resource(self, _dict):
        """
        Updates the mapped_data sourceResource field with the given dictionary.
        """
        self.mapped_data["sourceResource"].update(_dict)

    def get_values_from_text_attrib(self, provider_prop, suppress_attribs={}):
        '''Return a list of string values take from the OAC type
        original record (each value is {'text':<val>, 'attrib':<val>} object)
        '''
        values = []
        if exists(self.provider_data, provider_prop):
            for x in self.provider_data[provider_prop]:
                try:
                    value = x['text']
                except KeyError:
                    # not an elementtree type data value
                    values.append(x)
                    continue
                if not x['attrib']:
                    values.append(x['text'])
                else:
                    suppress = False
                    for attrib, attval in x['attrib'].items():
                        if attval in suppress_attribs.get(attrib, []):
                            suppress = True
                            break
                    if not suppress:
                        values.append(x['text'])
        return values

    def source_resource_orig_list_to_prop(self, original_fields, srcRes_prop, suppress_attribs={}):
        '''for a list of fields in the providers original data, append the
        values into a single sourceResource field

        Override to handle elements which are dictionaries of format
        {'attrib': {}, 'text':"string value of element"}
        suppress_attribs is a dictionary of attribute key:value pairs to
        omit from mapping.
        '''
        values = []
        for field in original_fields:
            if exists(self.provider_data, field):
                values.extend(
                    self.get_values_from_text_attrib(field, suppress_attribs))
        if values:
            self.update_source_resource({srcRes_prop: values})

    def source_resource_prop_to_prop(self, prop, suppress_attribs={}):
        '''Override to handle elements which are dictionaries of format
        {'attrib': {}, 'text':"string value of element"}

        prop - name of field in original data and in sourceResource to map to
        suppress_attribs is a dictionary of attribute key:value pairs to
            omit from mapping.

        '''
        values = self.get_values_from_text_attrib(prop, suppress_attribs)
        self.update_source_resource({prop: values})

        
    def get_best_oac_image(self):
        '''From the list of images, choose the largest one'''
        best_image = None
        if 'originalRecord' in self.provider_data:  # guard weird input
            x = 0
            thumb = self.provider_data.get('originalRecord',{}).get('thumbnail', None)
            if thumb:
                if 'src' in thumb:
                    x = thumb.get('X')
                    best_image = thumb.get('src')
            ref_images = self.provider_data.get('originalRecord',{}).get(
                'reference-image', [])
            if type(ref_images) == dict:
                ref_images = [ref_images]
            for obj in ref_images:
                if int(obj['X']) > x:
                    x = int(obj.get('X'))
                    best_image = obj.get('src')
            if best_image and not best_image.startswith('http'):
                best_image = '/'.join((URL_OAC_CONTENT_BASE, best_image))
        return best_image

    def map_copyrightDate(self):
        # suppress dateCopyrighted from main date field
        copydate_data = self.provider_data.get('date', None)
        if copydate_data:
            copyright_date = [
                d.get('text') for d in copydate_data
                if d.get('attrib') if d.get('attrib',{}).get('q') == 'dcterms:dateCopyrighted'
            ]
            self.update_source_resource({"copyrightDate": copyright_date})

    def map_subject(self):
        subject_values = self.get_values_from_text_attrib(
            "subject", suppress_attribs={'q': 'series'})
        subject_objs = [{'name': s} for s in subject_values]
        self.update_source_resource({"subject": subject_objs})

    def map_alternative_title(self):
        # separate out alternate title(s) from main title
        grab_titles = self.provider_data.get('title', None)
        if grab_titles:
            alt_titles = [
                t.get('text') for t in grab_titles
                if t.get('attrib') if t.get('attrib',{}).get('q') == 'alternative'
            ]
            self.update_source_resource({"alternativeTitle": alt_titles})

    def map_genre(self):
        # separate out q="genreform" values from type values
        genre_data = self.provider_data.get('type', None)
        if genre_data:
            genre_form = [
                g.get('text') for g in genre_data
                if g.get('attrib') if g.get('attrib',{}).get('q') == 'genreform'
            ]
            self.update_source_resource({"genre": genre_form})

    def map_spatial(self):
        if 'originalRecord' in self.provider_data:  # guard weird input
            if 'coverage' in self.provider_data.get('originalRecord'):
                coverage_data = iterify(
                    getprop(self.provider_data.get('originalRecord'), "coverage"))
                # remove arks from data
                # and move the "text" value to
                coverage = []
                for c in coverage_data:
                    if (not isinstance(c, basestring) and
                            not c.get('text').startswith('ark:')):
                        if 'q' in c.get('attrib', {}) and 'temporal' not in c.get('attrib',{}).get('q'):
                            coverage.append(c.get('text'))
                        if 'q' not in c.get('attrib', {}) and c.get('attrib', {}) is not None and not Anum_re.match(c.get('text')):
                            coverage.append(c.get('text'))
                self.update_source_resource({"spatial": coverage})

    def map_temporal(self):
        if 'originalRecord' in self.provider_data:  # guard weird input
            if 'coverage' in self.provider_data.get('originalRecord'):
                time_data = iterify(
                    getprop(self.provider_data.get('originalRecord'), "coverage"))
                temporal = []
                for t in time_data:
                    if 'q' in t.get('attrib', {}) and 'temporal' in t.get('attrib',{}).get('q'):
                        temporal.append(t.get('text'))
                    self.update_source_resource({"temporal": temporal})

    def map_state_located_in(self):
        

