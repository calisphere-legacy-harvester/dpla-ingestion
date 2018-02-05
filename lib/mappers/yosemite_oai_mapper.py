# -*- coding: utf-8 -*-
from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from dplaingestion.selector import getprop


class Yosemite_OAIMapper(OAIDublinCoreMapper):
    '''A base mapper for Yosemite OAI feed.'''

    def map_is_shown_at(self):
        isShownAt = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in idents:
            if 'npgallery.nps.gov' in i:
                if 'AssetDetail' in i:
                    isShownAt = i
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    def map_is_shown_by(self):
        '''Grab the image URL from identifier values (but not the full size version) by looking for slash at end of string'''
        isShownBy = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in idents:
            if 'npgallery.nps.gov' in i:
                if i.endswith('/'):
                    isShownBy = i
        if isShownBy:
            self.mapped_data.update({'isShownBy': isShownBy})

    '''grab date value from dcterms:temporal and not dc:date which
    is date digitized'''
    def map_date(self):
        fields = ("available", "created", "dateAccepted",
                  "dateCopyrighted", "dateSubmitted", "issued",
                  "modified", "valid", "temporal")
        self.source_resource_orig_list_to_prop(fields, 'date')

    def map_temporal(self):
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
