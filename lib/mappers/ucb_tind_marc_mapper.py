# -*- coding: utf-8 -*-
from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.mappers.marc_mapper import PyMARCMapper
from dplaingestion.selector import getprop, setprop

from akara import logger

class UCBTIND_MARCMapper(PyMARCMapper):
    '''A base mapper for UC Berkeley's new TIND OAI feed.
    Based off CONTENTdm mapper since it seemed to map all MD correctly.'''

    def __init__(self, provider_data):
        super(UCBTIND_MARCMapper, self).__init__(provider_data)
        self.mapping_dict.update({
            lambda t: t == "246": [(self.map_alt_title, '!6')],
            lambda t: t == "336": [(self.map_format, "a")],
            lambda t: t == "001": [(self.map_is_shown_at, None)]
        })


    # subclassed for the `if code !=6` commented below
    # (code 6 is a reference to marc field 880)
    def _get_contributor_values(self, _dict, codes):
        """
        Extracts the appropriate "#text" values from _dict for the contributor
        field. If subfield "e" #text value is "aut" or "cre", the _dict is not
        used.
        """
        values = []
        for subfield in self._get_subfields(_dict):
            if self.pymarc:
                if "e" in subfield:
                    if subfield['e'] in ("aut", "cre"):
                        return []
                else:
                    for code in subfield.keys():
                        if not codes or code in codes:
                            if code != '6':             # ADDED FOR UCB TIND
                                values.append(subfield[code])
            else:
                if not codes or ("code" in subfield and
                                 subfield["code"] in codes):
                    if "#text" in subfield:
                        values.append(subfield["#text"])

        # Do not any _dict subfield values if the _dict contains #text of
        # "aut" or "cre" for code "e"
                if (subfield.get("code") == "e" and
                        subfield.get("#text") in ("aut", "cre")):
                    return []
        return values

    # subclassed for excluding code 6 (reference to marc field 880)
    def map_title(self, _dict, tag, index, codes):
        if tag == '245':
            if codes:
                codes = codes + '6'
            else:
                codes = "!6"
        super(UCBTIND_MARCMapper, self).map_title(_dict, tag, index, codes)

    # no alt title default mapping in the PyMarcMapper
    def map_alt_title(self, _dict, tag, codes):
        prop = "sourceResource/alternativeTitle"
        self.extend_prop(prop, _dict, codes)

    # there are two marc fields tagged 856, both with ind1='4'
    # one has ind2='1', the other has ind2=''
    # the one with ind2=1 has a link to oskicat that we don't care about
    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        if tag == '856':
            if _dict['856']['ind2'] != '1':
                self.extend_prop(prop, _dict, codes)
                if isinstance(self.mapped_data[prop], list):
                    # EDM says this is a single URL, not a list
                    self.mapped_data[prop] = self.mapped_data[prop][0]

    # prepend marc field 001 with TIND url
    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        if tag == '001':
            self.mapped_data[prop] = "http://digicoll.lib.berkeley.edu/record/"
            self.mapped_data[prop] += self._get_values(_dict, codes)[0]

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
