# -*- coding: utf-8 -*-
from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from akara import logger

class CalPoly_OAIMapper(OAIDublinCoreMapper):
    '''A mapper for CalPoly Islandora OAI-PMH feed'''

    def map_source_resource(self):
        '''Keep restricted records out of SOLR by not creating
           sourceResource entries for objects with "RESTRICT [...]"
           as first value in dc:rights field
        '''
        rights = self.provider_data['originalRecord']['rights']
        restricted = False
        if not isinstance(rights, basestring):
            for r in rights:
                if r and r.startswith("RESTRICT"):
                    restricted = True
                    break # breaks out of for loop, as we don't need to check more values
        else:
            if rights.startswith("RESTRICT"):
                restricted = True
        logger.error(restricted)
        if not restricted:
            super(CalPoly_OAIMapper, self).map_source_resource()

    def map_is_shown_at(self):

        #Pick out record link from identifier values
        ident = self.provider_data['originalRecord']['identifier']
        for i in ident:
            if i:
                if 'digital.lib.calpoly.edu' in i:
                    self.mapped_data.update({'isShownAt': i})

    def map_is_shown_by(self):

        # Change URL from 'TN' to 'JPG' for larger versions of image objects
        thumb_url = self.provider_data['originalRecord']['identifier.thumbnail']
        if 'type' in self.provider_data['sourceResource'] and thumb_url:
            if 'Image' in self.provider_data['sourceResource']['type']:
                thumb_url = thumb_url[0].replace("/TN/", "/JPG/")
                self.mapped_data.update({'isShownBy': thumb_url})
            self.mapped_data.update({'isShownBy': thumb_url})

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
