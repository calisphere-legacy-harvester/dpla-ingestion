import os
import re
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify
from akara import module_config

URL_OAC_CONTENT_BASE = module_config().get(
                        'url_oac_content',
                        os.environ.get('URL_OAC_CONTENT_BASE',
                                        'http://content.cdlib.org')
                        )

# collection 25496 has coverage values like A0800 & A1000
# drop these
Anum_re = re.compile('A\d\d\d\d')

class OAC_DCMapper(DublinCoreMapper):
    '''Mapper for OAC xml feed objects'''
    def get_values_from_text_attrib(self,
                                    provider_prop,
                                    suppress_attribs={}):
        '''Return a list of string values take from the OAC type
        original record (each value is {'text':<val>, 'attrib':<val>} object)
        '''
        values = []
        if exists(self.provider_data_source, provider_prop):
            for x in self.provider_data_source[provider_prop]:
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

    # sourceResource mapping
    def source_resource_orig_to_prop(self,
                                    provider_prop,
                                    srcRes_prop,
                                    suppress_attribs={}):
        '''Override to handle elements which are dictionaries of format
        {'attrib': {}, 'text':"string value of element"}
        Args:
            provider_prop - name of field in original data
            srcRes_prop - name of field in sourceResource to map to
            suppress_attribs is a dictionary of attribute key:value pairs to
                omit from mapping.
        '''
        values = self.get_values_from_text_attrib(provider_prop,
                                             suppress_attribs)
        self.update_source_resource({srcRes_prop: values})
            
    def source_resource_prop_to_prop(self, prop, suppress_attribs={}):
        '''Override to handle elements which are dictionaries of format
        {'attrib': {}, 'text':"string value of element"}
        suppress_attribs is a dictionary of attribute key:value pairs to
        omit from mapping.
        '''
        provider_prop = prop if not self.prefix else ''.join((self.prefix, prop))
        self.source_resource_orig_to_prop(provider_prop, prop, suppress_attribs)

    def get_best_oac_image(self):
        '''From the list of images, choose the largest one'''
        best_image = None
        if self.provider_data.has_key('originalRecord'): # guard weird input
            x = 0
            thumb = self.provider_data['originalRecord'].get('thumbnail', None)
            if thumb:
                if 'src' in thumb:
                    x = thumb['X']
                    best_image = thumb['src']
            ref_images = self.provider_data['originalRecord'].get('reference-image', [])
            if type(ref_images) == dict:
                ref_images = [ref_images]
            for obj in ref_images:
                if int(obj['X']) > x:
                    x = int(obj['X'])
                    best_image = obj['src']
            if best_image and not best_image.startswith('http'):
                best_image = '/'.join((URL_OAC_CONTENT_BASE, best_image))
        return best_image

    def map_is_shown_at(self, index=None):
        ''' This is set in select-oac-id but must be added to mapped data'''
        self.mapped_data.update({'isShownAt': self.provider_data.get('isShownAt', None)})

    def map_is_shown_by(self, index=None):
        #already set in select_oac_id to base of {{obj url}}/thumbnail
        best_image = self.get_best_oac_image()
        if best_image:
            self.mapped_data.update( { "isShownBy" :  self.get_best_oac_image(),
                })

    def map_data_provider(self):
        if self.provider_data.has_key('originalRecord'):
            if self.provider_data['originalRecord'].has_key('collection'):
                self.mapped_data.update({"dataProvider":
                    self.provider_data['originalRecord']['collection']})

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": [{"name": "California"}]})

    def map_spatial(self):
        if self.provider_data.has_key('originalRecord'):
            if self.provider_data['originalRecord'].has_key('coverage'):
                coverage_data = iterify(getprop(self.provider_data['originalRecord'],
                                                         "coverage"))
                #remove arks from data
                # and move the "text" value to 
                coverage_data = [ c['text'] for c in coverage_data if (not isinstance(c,basestring) and not c['text'].startswith('ark:'))]
                coverage_data = [ c for c in coverage_data if not Anum_re.match(c)]
                self.update_source_resource({"spatial":coverage_data})

    def map_format(self):
        self.source_resource_prop_to_prop("format",
                suppress_attribs={'q':'x'})

    def map_subject(self):
        subject_values = self.get_values_from_text_attrib("subject",
                suppress_attribs={'q':'series'})
        subject_objs = [{'name': s} for s in subject_values]
        self.update_source_resource({"subject": subject_objs})

    def map_relation(self):
        # drop relation items
        pass

