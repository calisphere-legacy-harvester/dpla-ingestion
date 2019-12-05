# -*- coding: utf-8 -*-
from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.selector import getprop

class USC_OAIMapper(CONTENTdm_OAI_Mapper):
    '''A base mapper for University of Southern California OAI feed'''

    def strip_brackets(self, value):
        if '[Legacy record ID]' in value:
            return value
        if isinstance(value, basestring):
            newVal = value.split('[')
            return newVal[0].strip()
        if isinstance(value, list):
            newlist = []
            for v in value:
                newlist.append(self.strip_brackets(v))
            return newlist
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = self.strip_brackets(v)
            return value
        return None

    def map_is_shown_at(self):
        isShownAt = None
        if 'identifier' in self.provider_data_source:
            idents = getprop(self.provider_data_source, 'identifier')
            for i in idents:
                if 'doi.org' in i:
                    isShownAt = i
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    def map_is_shown_by(self):
        isShownBy = None
        if 'identifier' in self.provider_data_source:
            idents = getprop(self.provider_data_source, 'identifier')
            for i in idents:
                if 'thumbnails.digitallibrary.usc.edu' in i:
                    isShownBy = i
        if isShownBy:
            self.mapped_data.update({'isShownBy': isShownBy})

    def map_identifier(self):
        self.to_source_resource_with_split('identifier', 'identifier')

    def map_format(self):
        self.to_source_resource_with_split('format', 'format')

    def map_description(self):
        self.to_source_resource_with_split('description', 'description')

    def map_date(self):
        date = []
        if 'date' in self.provider_data_source:
            dates = getprop(self.provider_data_source, 'date')
            for d in dates:
                if '[digitize date]' not in d.lower():
                    date.append(d)
        if date:
            self.update_source_resource({'date': date})

    def update_mapped_fields(self):
        '''strip out info in brackets from end of sourceResource
        values using regex. Don't strip out [Legacy record ID]
        so that DPLA can key on it for record-matching
        or description'''
        for b in self.mapped_data.get('sourceResource'):
            if b == 'description':
                continue
            fieldValue = self.mapped_data.get('sourceResource',{}).get(b)
            stripValue = self.strip_brackets(fieldValue)
            self.update_source_resource({b: stripValue})


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
