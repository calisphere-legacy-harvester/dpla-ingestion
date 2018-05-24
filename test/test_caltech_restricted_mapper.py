# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=caltech_restrict"
    return H.request(url, "POST", body=body)


def test_calpoly_oai_dc_mapping():
    fixture = path.join(DIR_FIXTURES, 'caltech.json')
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
        obj['isShownAt'],
        "http://maccready.library.caltech.edu/islandora/object/pbm%3A631")
    TC.assertEqual(
        obj['isShownBy'],
        "http://maccready.library.caltech.edu/islandora/object/pbm%3A631/datastream/TN/view/Model%20airplanes%20and%20gliders%3A%20includes%20photographs%20of%20MacCready%20with%20award%20winning%20planes.%202%20Sheets.%20%2834%20items%29.jpg"
    )
    TC.assertEqual(srcRes['description'], [
        "ca.1937-1941,1945. Part of: Paul B. MacCready Papers ca. 1930-2002. Series 7: Audio-Visual material; Subseries 1: Photographic slides; Box 1, Folder 1"
    ])
    TC.assertEqual(srcRes['format'],
                   ["projected graphic", "Black and White 35mm slides"])


def test_title_exclusion():
    '''Verify that objects with "Finding Aid" or "PBM_"
    as first value in dc:title field are not passed on
    to sourceResource & no isShownAt or isShownBy assigned
    '''
    fixture = path.join(DIR_FIXTURES, 'caltech-restrict.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    assert resp.status == 200
    content = json.loads(content)
    TC.assertFalse(content['sourceResource'])
    TC.assertNotIn('isShownAt', content)
    TC.assertNotIn('isShownBy', content)

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
