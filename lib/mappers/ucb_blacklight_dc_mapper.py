# -*- coding: utf-8 -*-
from akara import logger
from dplaingestion.selector import exists, getprop
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper


class UCBBlacklightDCMapper(DublinCoreMapper):
    def map_is_shown_at(self, index=None):
        base_url = 'http://dc.lib.berkeley.edu/catalog/'
        self.mapped_data.update(
            {'isShownAt': base_url+self.provider_data['originalRecord']['id']})

    def map_is_shown_by(self):
        self.mapped_data.update({"isShownBy": self.provider_data["imageFile"]}
                                ) if self.provider_data.get("imageFile",
                                                            False) else None

    def map_title(self):
        self.source_resource_orig_to_prop('title_display', 'title')

    def map_creator(self):
        self.source_resource_orig_to_prop('name_Sphotographer_namePart',
                                          'creator')

    def map_type(self):
        self.source_resource_orig_to_prop('format', 'type')

    def map_date(self):
        self.source_resource_orig_to_prop('originInfo_dateCreated', 'date')

    def map_format(self):
        format_values = []
        if "relatedItem_Toriginal_typeOfResource" in self.provider_data_source:
            format_values.append(
                    self.provider_data_source[
                        "relatedItem_Toriginal_typeOfResource"])
        if "format" in self.provider_data_source:
            format_values.append(self.provider_data_source["format"])
        if format_values:
            self.update_source_resource({'format': format_values})

    def map_identifier(self):
        self.source_resource_orig_to_prop('identifier_TlocalId_SphotoNo',
                                          'identifier')

    def map_spatial(self):
        self.source_resource_orig_to_prop('relatedItem_titleInfo_Tid_SquadName',
                                          'spatial')

    def map_subject(self):
        self.source_resource_orig_to_prop('note_Tspecie',
                                          'subject')

    def map_rights(self):
        self.source_resource_prop_to_prop('rights')

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
