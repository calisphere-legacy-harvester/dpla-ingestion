# -*- coding: utf-8 -*-
from dplaingestion.mappers.islandora_oai_dc_mapper import Islandora_OAIMapper
import requests


class SJSU_Islandora_Mapper(Islandora_OAIMapper):
    '''A mapper for SJSU Islandora OAI-PMH feed
    '''

    def map_is_shown_at(self):

        # Get digital collection URL from OAI-PMH slug
        harvest_url = self.provider_data.get('originalRecord', {}).get(
            'collection', {})[0].get('url_harvest')
        coll_url = harvest_url.replace('/oai2', '')

        # Get & format record ID
        ident = self.provider_data.get('originalRecord', {}).get('id')
        if ':' in ident:
            collID, recID = ident.rsplit(':', 1)
            newID = recID.replace('islandora_', 'islandora%3A')

            # Build record link
            self.mapped_data["isShownAt"] = ''.join(
                (coll_url, '/islandora/object/', newID))

    def map_is_shown_by(self):

        # Get digital collection URL from OAI-PMH slug
        harvest_url = self.provider_data.get('originalRecord', {}).get(
            'collection', {})[0].get('url_harvest')
        coll_url = harvest_url.replace('/oai2', '')

        # Get & format record ID
        ident = self.provider_data.get('originalRecord', {}).get('id')
        if ':' in ident:
            collID, recID = ident.rsplit(':', 1)
            newID = recID.replace('islandora_', 'islandora%3A')

            # Build image link
            thumb_url = ''.join((coll_url, '/islandora/object/', newID,
                                 '/datastream/TN/view'))

            # Change URL from 'TN' to 'JPG' for larger versions of image objects & test to make sure the link resolves
            if 'image' or 'StillImage' in self.provider_data.get('type'):
                jpg_url = thumb_url.replace("/TN/", "/JPG/")
                request = requests.get(jpg_url)
                if request.status_code == 200:
                    thumb_url = jpg_url
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
