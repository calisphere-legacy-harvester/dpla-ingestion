# -*- coding: utf-8 -*-
from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.mappers.marc_mapper import PyMARCMapper
from dplaingestion.selector import getprop
from akara import logger

class UCBTIND_MARCMapper(PyMARCMapper):
    '''A base mapper for UC Berkeley's new TIND OAI feed.
    Based off CONTENTdm mapper since it seemed to map all MD correctly.'''

    def __init__(self, provider_data):
        super(UCBTIND_MARCMapper, self).__init__(provider_data)

    # def map_is_shown_at(self):
    #     isShownAt = None
    #     idents = getprop(self.provider_data_source, 'identifier')
    #     for i in filter(None, idents):
    #         if 'tind.io/record/' in i and '/files/' not in i:
    #             isShownAt = i
    #     if isShownAt:
    #         self.mapped_data.update({'isShownAt': isShownAt})

    # def map_is_shown_by(self):
    #     isShownBy = None
    #     idents = getprop(self.provider_data_source, 'identifier')
    #     for i in filter(None, idents):
    #         if 'tind.io/record/' in i and '/files/' in i:
    #             isShownBy = i
    #     if isShownBy:
    #         self.mapped_data.update({'isShownBy': isShownBy})

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
