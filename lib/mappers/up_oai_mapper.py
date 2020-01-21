from dplaingestion.mappers.oai_dublin_core_mapper import OAIDublinCoreMapper
from dplaingestion.selector import getprop


class UP_OAI_Mapper(OAIDublinCoreMapper):
    '''Mapper for University of the Pacific bepress hosted collections from their OAI feed

    '''

    def map_is_shown_by(self):
        '''Can only reliably get a small thumbnail from the metadata in the OAI feed--
        Can parse the OAI id to get info we need.

        As it turns out, for "image" type objects, larger images are
        available.
        The creation of the URL to grab the image needs to check the image
        object information before setting the URL. ContentDM has an image
        server that will resize the image on demand. We want images whose max
        dimension in height or width is 1024. Need to first get image info at
        the base URL then request an appropriately scaled image.
        This needs to be done after the sourceResouce/type is mapped, so it
        happens in update_mapped_fields
        '''
        descs = getprop(self.provider_data_source, 'description')
        for d in filter(None, descs):
            if '/thumbnail.jpg' in d:
                url_preview = d.replace('thumbnail', 'preview')
                self.mapped_data.update({'isShownBy': url_preview})
                break

    def map_is_shown_at(self):
        '''The identifier that points to the OAI server & has cdm/ref in the
        path is the path to object.
        Can get harvest base URL from the "collection" object
        '''
        isShownAt = None
        idents = getprop(self.provider_data_source, 'identifier')
        for i in filter(None, idents):
            if 'scholarlycommons.pacific.edu' in i:
                if 'viewcontent' not in i:
                    isShownAt = i
        if isShownAt:
            self.mapped_data.update({'isShownAt': isShownAt})

    def map_description(self):
        '''drop thumbnail URL from description field'''
        values = []
        descs = getprop(self.provider_data_source, 'description')
        for d in filter(None, descs):
            if 'thumbnail.jpg' not in d:
                values.append(d)
        if values:
            self.update_source_resource({'description': values})

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
