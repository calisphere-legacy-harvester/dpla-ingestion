# -*- coding: utf-8 -*-
from dplaingestion.mappers.islandora_oai_dc_mapper import Islandora_OAIMapper
import requests


class CalTech_Restricted_Mapper(Islandora_OAIMapper):
    '''A mapper for CalTech Islandora collections that does not map
    Finding Aid and certain item-level catalog records through to SOLR/
    Calisphere (see find_restricted below).
    '''

    def find_restricted(self):

        restrict_prefixes = ["Finding Aid", "PBM_", "DAG_", "DAGB_"]
        restricted = False
        if 'title' in self.provider_data:
            title = self.provider_data['title']
            if not isinstance(title, basestring):
                for r in title:
                    if r.startswith(tuple(restrict_prefixes)):
                        restricted = True
                        break  # breaks out of for loop, as we don't need to check more values
            else:
                if r.startswith(tuple(restrict_prefixes)):
                    restricted = True
        return restricted

    def map_source_resource(self):

        restricted = self.find_restricted()
        if not restricted:
            super(Islandora_OAIMapper, self).map_source_resource()

    def map_is_shown_at(self):
        ''' Pick out record link from identifier values
            Don't create isShownAt for objects with "Finding Aid"
            or "PBM_" as first value in dc:title field
        '''
        restricted = self.find_restricted()
        if not restricted:
            ident = self.provider_data['identifier']
            for i in ident:
                if i:
                    if 'library.caltech.edu' in i:
                        self.mapped_data.update({'isShownAt': i})

    def map_is_shown_by(self):

        restricted = self.find_restricted()
        if not restricted:
            # Change URL from 'TN' to 'JPG' for larger versions of image objects & test to make sure the link resolves
            try:
                thumb_url = self.provider_data['identifier.thumbnail'][0]
                if 'type' in self.provider_data and any(s in self.provider_data['type'] for s in ('StillImage','image')):
                    jpg_url = thumb_url.replace("/TN/", "/JPG/")
                    request = requests.get(jpg_url)
                    if request.status_code == 200:
                        thumb_url = jpg_url
                self.mapped_data.update({'isShownBy': thumb_url})
            except KeyError:  # no identifier.thumbnail
                pass

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
