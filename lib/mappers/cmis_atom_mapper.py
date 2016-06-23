# -*- coding: utf-8 -*-
from dplaingestion.mappers.mapper import Mapper
#from dplaingestion.selector import exists, getprop
#from dplaingestion.utilities import iterify
#from akara import module_config

    
URL_BASE_SHOWN_AT = 'https://oakland.access.preservica.com/file/sdb:digitalFile|'
URL_BASE_SHOWN_BY = 'https://us.preservica.com/Render/render/jpegImage?content=true&typeFile='

class CMISAtomDCMapper(Mapper):  
    def __init__(self, provider_data, key_prefix=None):
        super(CMISAtomDCMapper, self).__init__(provider_data, key_prefix)
        metadata_root = self.provider_data["{http://www.w3.org/2005/Atom}entry"]["{http://docs.oasis-open.org/ns/cmis/restatom/200908/}object"]["{http://www.tessella.com/sdb/cmis/metadata}metadata"]
        #now under the provider_data_source is a list of items corresponding to
        #the dublin core metadata. How to handle
        '''
              {
                "{http://www.tessella.com/sdb/cmis/metadata}name": {
                  "$": "title"
                },
                "{http://www.tessella.com/sdb/cmis/metadata}value": {
                  "$": "The Phyllis Wheatley Reporter vol. 1 no. 1"
                }
              },

        '''
        self.provider_data_source = metadata_root["{http://www.tessella.com/sdb/cmis/metadata}group"][0]["{http://www.tessella.com/sdb/cmis/metadata}item"]

    def map_is_shown_at(self):
        objid = self.mapped_data['_id'].split('--')[1]
        self.mapped_data.update(
                {'isShownAt': URL_BASE_SHOWN_AT + objid })

    def map_is_shown_by(self):
        objid = self.mapped_data['_id'].split('--')[1]
        self.mapped_data.update(
                {'isShownBy': URL_BASE_SHOWN_BY + objid })

    def map_source_resource(self):
        '''Because of the format of the data, it is going to be easier to loop
        through the values, match to given sourceResource field and update
        Need to handle non-existent fields & fields with data already in
        defaultdict with list values
        so I'm not overriding the various map_<field> methods.
        '''
        self.mapped_data['sourceResource'].update({'stateLocatedIn':'California'})
        DC_elements = [ 'contributor', 'coverage', 'creator', 'date',
                    'description', 'format', 'identifier', 'language',
                    'publisher', 'relation', 'rights', 'source', 'subject',
                    'title', 'type',]
        for item in self.provider_data_source:
            field = item["{http://www.tessella.com/sdb/cmis/metadata}name"]
            field = field.get('$', None)
            value = item["{http://www.tessella.com/sdb/cmis/metadata}value"]
            value = value.get('$', None)
            if not (field and value):
                continue
            value = unicode(value)
            if field in DC_elements:
                field_map_sr = field
                d = value
                if field == 'coverage':
                    d = {'name': value}
                    field_map_sr = 'spatial'
                elif field == 'subject':
                    d = {'name':value}
                vlist = self.mapped_data['sourceResource'].get(field_map_sr, None)
                if vlist:
                    vlist.append(d)
                else:
                    vlist = [d]
                self.mapped_data['sourceResource'][field_map_sr] = vlist

# Copyright © 2016, Regents of the University of California
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

