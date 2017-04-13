# -*- coding: utf-8 -*-
from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper


class CalPoly_OAIMapper(OAIDublinCoreMapper):
    '''A mapper for CalPoly Islandora OAI-PMH feed'''

    def remove_null_values(self, fieldValue):
        '''Remove null values from the originalRecord'''
        hasValue = []
        for f in fieldValue:
            if f is not None and f != '()':
                hasValue.append(f)
        return hasValue

    def map_source_resource(self):
        '''Keep restricted records out of SOLR by not creating
           sourceResource entries for objects with "RESTRICT [...]"
           as first value in dc:rights field
        '''
        rights = self.provider_data['rights']
        restricted = False
        if not isinstance(rights, basestring):
            for r in rights:
                if r and r.startswith("RESTRICT"):
                    restricted = True
                    break  # breaks out of for loop, as we don't need to check more values
        else:
            if rights.startswith("RESTRICT"):
                restricted = True
        if not restricted:
            super(CalPoly_OAIMapper, self).map_source_resource()

    def map_contributor(self):
        if 'contributor' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data[
                'contributor'])
            if notNull:
                self.update_source_resource({'contributor': notNull})

    def map_creator(self):
        if 'creator' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['creator'])
            if notNull:
                self.update_source_resource({'creator': notNull})

    def map_date(self):
        if 'date' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['date'])
            if notNull:
                self.update_source_resource({'date': notNull})

    def map_description(self):
        if 'description' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data[
                'description'])
            if notNull:
                self.update_source_resource({'description': notNull})

    def map_extent(self):
        if 'extent' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['extent'])
            if notNull:
                self.update_source_resource({'extent': notNull})

    def map_format(self):
        if 'format' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['format'])
            if notNull:
                self.update_source_resource({'format': notNull})

    def map_language(self):
        if 'language' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['language'])
            if notNull:
                self.update_source_resource({'language': notNull})

    def map_spatial(self):
        if 'spatial' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['spatial'])
            if notNull:
                self.update_source_resource({'spatial': notNull})

    def map_rights(self):
        if 'rights' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['rights'])
            if notNull:
                self.update_source_resource({'rights': notNull})

    def map_subject(self):
        if 'subject' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['subject'])
            if notNull:
                self.update_source_resource({'subject': notNull})

    def map_temporal(self):
        if 'temporal' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['temporal'])
            if notNull:
                self.update_source_resource({'temporal': notNull})

    def map_title(self):
        if 'title' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['title'])
            if notNull:
                self.update_source_resource({'title': notNull})

    def map_type(self):
        if 'type' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['type'])
            if notNull:
                self.update_source_resource({'type': notNull})

    def map_identifier(self):
        if 'identifier' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['identifier'])
            if notNull:
                self.update_source_resource({'identifier': notNull})

    def map_publisher(self):
        if 'publisher' in self.provider_data:
            notNull = self.remove_null_values(self.provider_data['publisher'])
            if notNull:
                self.update_source_resource({'publisher': notNull})

    def map_is_shown_at(self):
        # Pick out record link from identifier values
        ident = self.provider_data['identifier']
        for i in ident:
            if i:
                if 'digital.lib.calpoly.edu' in i:
                    self.mapped_data.update({'isShownAt': i})

    def map_is_shown_by(self):

        # Change URL from 'TN' to 'JPG' for larger versions of image objects
        thumb_url = self.provider_data['identifier.thumbnail']
        if thumb_url:
            if 'StillImage' in self.provider_data['type']:
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
