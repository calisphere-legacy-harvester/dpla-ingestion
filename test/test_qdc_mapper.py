# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=dublin_core"
    return H.request(url, "POST", body=body)


def test_basic_dublin_core():
    fixture = path.join(DIR_FIXTURES, 'contentdm_oai_dc_only.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(
        srcRes['subject'][1]['name'],
        "Metabolic Studio; Los Angeles Aqueduct; LA Aqueduct; Acquaduct ")
    TC.assertEqual(srcRes["format"], ["2 pages", "image/tiff"])
    TC.assertEqual(srcRes["type"], ["Letters", "Text"])
    TC.assertEqual(srcRes["rights"], [
        "http://library.lmu.edu/generalinformation/departments/digitallibraryprogram/copyrightandreproductionpolicy/"
    ])
    TC.assertEqual(srcRes["language"], ["eng"])
    TC.assertEqual(srcRes["description"], [
        "Letter from J. D. Black in Big Pine to H. R. Coffin",
        "J. D. Black (1893-1960), also known as Jack"
    ])
    TC.assertEqual(srcRes["date"], ["1924-07-24", "1920-1929"])
    TC.assertEqual(srcRes["relation"], [
        "J. D. Black Papers", "CSLA-15", "Series 1.; Box No. 8; Folder No. 4"
    ])
    TC.assertEqual(srcRes["spatial"],
                   ["Los Angeles (Calif.); Big Pine (Calif.)"])
    TC.assertEqual(srcRes["contributor"],
                   ["Support provided by the Metabolic Studio."])
    TC.assertEqual(srcRes["title"],
                   ["Letter from J. D. Black to H. R. Coffin"])
    TC.assertEqual(srcRes["identifier"], [
        "http://archive.org/details/cubanc_000177", "sc_jdbp001110001",
        "sc_jdbp00111",
        "http://digital-collections.csun.edu/cdm/ref/collection/GSAC/id/21",
        "http://cdm15972.contentdm.oclc.org/bogus"
    ])
    TC.assertEqual(srcRes["creator"], ["Coffin, H. R."])


def test_qualified_dublin_core():
    fixture = path.join(DIR_FIXTURES, 'oai-qdc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']

    TC.assertEqual(srcRes['contributor'], ['TEST contributor'])
    TC.assertEqual(srcRes['creator'], ['TEST creator'])
    TC.assertEqual(srcRes['date'], [
        "TEST available",
        "TEST created",
        "TEST date",
        "TEST dateAccepted",
        "TEST dateCopyrighted",
        "TEST dateSubmitted",
        "TEST issued",
        "TEST modified",
        "TEST valid",
    ])
    TC.assertEqual(srcRes['description'], [
        "TEST abstract",
        "TEST description",
        "TEST tableOfContents",
    ])
    TC.assertEqual(srcRes['extent'], ["TEST extent"])
    TC.assertEqual(srcRes['format'], [
        "TEST format",
        "TEST medium",
    ])
    TC.assertEqual(srcRes['identifier'], [
        "TEST bibliographicCitation",
        "TEST identifier",
    ])
    TC.assertEqual(srcRes['language'], ["TEST language"])
    TC.assertEqual(srcRes['publisher'], ["TEST publisher"])
    TC.assertEqual(srcRes['relation'], [
        "TEST conformsTo",
        "TEST hasFormat",
        "TEST hasPart",
        "TEST hasVersion",
        "TEST isFormatOf",
        "TEST isPartOf",
        "TEST isReferencedBy",
        "TEST isReplacedBy",
        "TEST isRequiredBy",
        "TEST isVersionOf",
        "TEST references",
        "TEST relation",
        "TEST replaces",
        "TEST requires",
    ])
    TC.assertEqual(srcRes['rights'], [
        "TEST accessRights",
        "TEST rights",
    ])
    TC.assertEqual(srcRes['subject'], [{"name": "TEST subject"}])
    TC.assertEqual(srcRes['title'], ["TEST title"])
    TC.assertEqual(srcRes['type'], ["TEST type"])
    TC.assertEqual(srcRes['alternativeTitle'], ["TEST alternative"])
    TC.assertEqual(srcRes['spatial'], ["TEST coverage", "TEST spatial"])
    TC.assertEqual(srcRes['temporal'], ["TEST temporal"])

def test_string_description_fields():
    '''Test what happens when one of a possible list of fields is a string, not
    list value
    '''
    fixture = path.join(DIR_FIXTURES, 'oai-qdc-string-fields.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['description'], [
        "TEST abstract",
        "TEST description",
        "TEST tableOfContents",
    ])

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
