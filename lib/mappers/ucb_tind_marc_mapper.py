# -*- coding: utf-8 -*-
from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.mappers.marc_mapper import PyMARCMapper
from dplaingestion.selector import getprop, setprop
import re

from akara import logger

class UCBTIND_MARCMapper(PyMARCMapper):
    '''A base mapper for UC Berkeley's new TIND OAI feed.
    Based off CONTENTdm mapper since it seemed to map all MD correctly.'''

    def __init__(self, provider_data):
        super(UCBTIND_MARCMapper, self).__init__(provider_data)
        self.mapping_dict.update({
            lambda t: t in ("024", "901"): [(self.map_identifier, 'a')],
            lambda t: t == "246": [(self.map_alt_title, '!6')],
            lambda t: t == "655": [(self.map_format, '!2')],
            lambda t: t == "336": [(self.map_type, None)],
            lambda t: t == "541": [(self.map_provenance, 'a')],
            lambda t: t == "001": [(self.map_is_shown_at, None),
                                   (self.map_is_shown_by, None)]
        })
        fields_880 = [d for d in self.provider_data['fields'] if '880' in d.keys()]
        self.fields_880 = {}
        for field_880 in fields_880:
            subfield = field_880['880']['subfields']
            field_880['subfield'] = subfield
            val_6 = self._get_values(field_880, '6')
            self.fields_880[val_6[0]] = field_880

    def _check_880(self, _dict):
        field_880 = self._get_one_subfield(_dict, '6')
        linked_fields = None
        if field_880:
            # get the tag
            tag = _dict.keys()
            tag.remove('subfield')
            tag = tag[0]
            # find the 880 field
            key_880 = tag + field_880[3:]
            if key_880 in self.fields_880:
                linked_fields = self.fields_880[key_880]
            # fail silently if 880 field not found
        return linked_fields

    def _get_values(self, _dict, codes):
        """
        Extracts the appropriate "#text" values from _dict given a string of
        codes. If codes is None, all "#text" values are extracted. If codes
        starts with "!", codes are excluded.
        For pymarc records, the #text if just the data value for the dictionary
        entry
        """
        values = []
        exclude = False
        codes = codes if codes != None else []

        if codes and codes.startswith("!"):
            exclude = True
            codes = codes[1:]

        for subfield in self._get_subfields(_dict):
            if self.pymarc:
                if not codes:
                    pass
                elif not exclude and (subfield.keys()[0] in codes):
                    pass
                elif exclude and len(subfield.keys()) == 1 and (
                        subfield.keys()[0] not in codes):
                    pass
                else:
                    continue
                code = subfield.keys()[0]
            else:
                if not codes:
                    pass
                elif not exclude and ("code" in subfield and
                                      subfield["code"] in codes):
                    pass
                elif exclude and ("code" in subfield and
                                  subfield["code"] not in codes):
                    pass
                else:
                    continue

            values.append(subfield[code]) if self.pymarc else values.append(
                subfield["#text"])
            val_880 = self._check_880(_dict)
            if val_880:
                values.append(self._get_one_subfield(val_880, code))

        if "subfield" not in _dict:
            values.append(self._get_mainfields(_dict))

        return values

    def _join_values(self, prop, values):
        """Joins the values on a prop-specific delimiter"""
        join_props = (["sourceResource/subject"], ". "), \
                     (["sourceResource/relation"], ". "), \
                     (["sourceResource/contributor",
                       "sourceResource/extent",
                       "sourceResource/identifier"], " ")

        for prop_list, delim in join_props:
            if prop in prop_list:
                if delim == ". ":
                    # Remove any existing periods at end of values, except for
                    # last value
                    values = [re.sub("\.$", "", v) for v in values]
                    values[-1] += "."
                if values:
                    values = [delim.join(values)]

        # Remove any double periods (excluding those in ellipsis)
        values = [re.sub("(?<!\.)\.{2}(?!\.)", ".", v) for v in values]

        return values


    # TIND doesn't use 1xx codes, only 7xx tags for creator
    # code 6 is a reference to marc field 880 and needs to be removed
    def map_contributor(self, _dict, tag, codes):
        prop = "sourceResource/creator"
        self.extend_prop(prop, _dict, "!6")

    # subclassed for excluding code 6 (reference to marc field 880)
    def map_publisher(self, _dict, tag, codes):
        prop = "sourceResource/publisher"
        self.extend_prop(prop, _dict, '!6c')

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

    def map_type(self, _dict, tag, codes):
        prop = "sourceResource/type"
        self.extend_prop(prop, _dict, codes)

    def map_description(self, _dict, tag, codes):
        if tag == '540':
            return
        prop = "sourceResource/description"
        self.extend_prop(prop, _dict, codes)

    def map_identifier(self, _dict, tag, codes):
        prop = "sourceResource/identifier"
        label = self.identifier_tag_labels.get(tag)

        # self.extend_prop(prop, _dict, codes, label, values=None)
        # rather than calling extend_prop here, we append (<tag>, <value>)
        # so update_identifier knows what to do
        values = self._get_values(_dict, codes)
        if values:
            if label:
                values.insert(0, label)
            prop_value = self._get_mapped_value(prop)

            # prop_value.extend((self._join_values(prop, values)))
            prop_value.extend([['tag'+tag, (self._join_values(prop, values))]])
            setprop(self.mapped_data, prop, prop_value)

    # there are two marc fields tagged 856, both with ind1='4'
    # one has ind2='1', the other has ind2=''
    # the one with ind2=1 has a link to oskicat that we don't care about
    def map_is_shown_by(self, _dict, tag, codes):
        prop = "isShownBy"
        if tag == '001':
            isShownBy = "http://digicoll.lib.berkeley.edu/nanna/thumbnail/v2/"
            isShownBy += self._get_values(_dict,codes)[0]
            isShownBy += "?redirect=1"
            self.mapped_data[prop] = isShownBy
        # fetch from the TIND image API via record ID
        # https://digicoll.lib.berkeley.edu/nanna/thumbnail/v2/53877?redirect=1
        # if tag == '856':
        #     if _dict['856']['ind2'] != '1':
        #         self.extend_prop(prop, _dict, codes)
        #         if isinstance(self.mapped_data[prop], list):
        #             # EDM says this is a single URL, not a list
        #             self.mapped_data[prop] = self.mapped_data[prop][0]

    # prepend marc field 001 with TIND url
    def map_is_shown_at(self, _dict, tag, codes):
        prop = "isShownAt"
        if tag == '001':
            self.mapped_data[prop] = "http://digicoll.lib.berkeley.edu/record/"
            self.mapped_data[prop] += self._get_values(_dict, codes)[0]

    def map_provenance(self, _dict, tag, codes):
        prop = 'sourceResource/provenance'
        self.extend_prop(prop, _dict, codes)

    def update_mapped_fields(self):
        self.update_identifier()
        self.update_title()
        self.update_format()
        self.update_is_shown_at()
        self.update_type_and_spec_type()


    def update_identifier(self):
        prop = "sourceResource/identifier"
        i_list = filter(None, getprop(self.mapped_data, prop))
        new_i_list = []
        tag024_flag = any('tag024' in identifier for identifier in i_list)
        tag035_flag = any('tag035' in identifier for identifier in i_list)

        for identifier in i_list:
            if tag024_flag and tag035_flag:
                if 'tag035' in identifier:
                    continue
            new_i_list = new_i_list + identifier[1]

        setprop(self.mapped_data, prop, new_i_list)


    def update_title(self):
        prop = "sourceResource/title"
        title_list = filter(None, getprop(self.mapped_data, prop))
        if title_list:
            title = [t for ts in title_list for t in ts]
            setprop(self.mapped_data, prop, title)
        else:
            delprop(self.mapped_data, prop)

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
