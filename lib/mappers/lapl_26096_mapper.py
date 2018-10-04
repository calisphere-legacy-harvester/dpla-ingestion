# -*- coding: utf-8 -*-
from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import getprop


class LAPL_26096Mapper(DublinCoreMapper):
    '''Map from the oai source records for LAPL collection 26096 (city
    directory) to the isShownAt & isShownBy properties.

    These are calculated from a portion of the identifier data per Adrian.
    The dc identifiers are of format:
    rescarta.lapl.org/jsp/RcWebImageViewer.jsp?doc_id=040428be-8b21-4de1-9b1e-3421068c0f1c/cl000000/20140507/00000002

    isShownAt:
    Use dc:identifier, but strip off "rescarta.lapl.org/jsp" and
    replace with "http://rescarta.lapl.org/ResCarta-Web/jsp"
    e.g.
    http://rescarta.lapl.org/ResCarta-Web/jsp/RcWebImageViewer.jsp?doc_id=040428be-8b21-4de1-9b1e-3421068c0f1c/cl000000/20140123/00000002

    isShownBy:
    Base URL is:
    http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id=
    after obj_id= use the charracters in the dc:identifier field that begin with    ""c1"" to the end of the identifier to get the specific identifier and
    append

    An example of the complete URL is:
    http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id=cl000000/20140507/00000027
    '''

    def get_object_view(self):
        identifier_url = getprop(self.provider_data_source, 'identifier')[0]
        # split off at /jsp
        object_view = identifier_url[identifier_url.index('jsp'):]
        return object_view

    def map_is_shown_at(self):
        object_view_path = self.get_object_view()
        self.mapped_data["isShownAt"] = ''.join(
            'http://rescarta.lapl.org/ResCarta-Web/' + object_view_path)

    def map_is_shown_by(self):
        object_view_path = self.get_object_view()
        obj_id = object_view_path[object_view_path.index('=') + 1:]
        obj_thumb_id = obj_id.split('/', 1)[1]
        self.mapped_data['isShownBy'] = ''.join(
            'http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id='
            + obj_thumb_id)

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
