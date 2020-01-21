# -*- coding: utf-8 -*-
from dplaingestion.mappers.omeka_mapper import Omeka_OAIMapper
from dplaingestion.selector import getprop
import requests


class Omeka_NoThumb_Mapper(Omeka_OAIMapper):
    '''Mapper for Omeka collections w/ thumbnail-less objects,
    does not map through to SOLR/Calisphere front end'''

    def get_thumb(self):
        '''Grab only the first image URL from identifier values'''
        thumb = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in filter(None, idents):
            if 's3.amazonaws.com/omeka-net' in i:
                thumb = i
                break
            elif '/files/thumbnails/' in i:
                thumb = i
                break
            # Build thumbnail url from original file url, if present
            elif '/files/original/' in i:
                if i.rsplit('.', 1)[1] == 'jpg':
                    thumb = i
                else:
                    thumb_url = i.replace("/original/", "/thumbnails/")
                    thumb_url = thumb_url.rsplit('.', 1)[0] + '.jpg'
                    request = requests.get(thumb_url)
                    if request.status_code == 200:
                        thumb = thumb_url
                    else:
                        thumb = i
                break
        return thumb

    def map_source_resource(self):
        thumb = self.get_thumb()
        if thumb:
            super(Omeka_NoThumb_Mapper, self).map_source_resource()

    def map_is_shown_at(self):
        thumb = self.get_thumb()
        if thumb:
            isShownAt = None
            idents = getprop(self.provider_data_source, 'identifier')
            for i in filter(None, idents):
                if 'items/show' in i:
                    isShownAt = i
            if isShownAt:
                self.mapped_data.update({'isShownAt': isShownAt})

    def map_is_shown_by(self):
        thumb = self.get_thumb()
        if thumb:
            self.mapped_data.update({'isShownBy': thumb})

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
