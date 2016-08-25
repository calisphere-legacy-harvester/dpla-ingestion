# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/ \
# is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=ucb_blacklight"
    return H.request(url, "POST", body=body)


def test_ucb_blacklight_mapping():
    fixture = path.join(DIR_FIXTURES,
                        'ucb-blacklight.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['format'], 'still image')
    TC.assertEqual(srcRes['rights'][:16],  "[\n  All requests")
    TC.assertEqual(srcRes['title'],
                   "Looking east.  Coulter pine-canyon live oak type.")
    TC.assertEqual(
        obj['isShownBy'],
        "http://digitalassets.lib.berkeley.edu/vtm/ucb/images/"
        "VTM00008024a_j.jpg")
    TC.assertEqual(
        obj['isShownAt'],
        "http://dc.lib.berkeley.edu/catalog/VTM_vtm1_3024_photo")
    TC.assertEqual(srcRes['creator'], "Wieslander, Albert Everett")
    # TC.assertEqual(obj['isShownAt'],
    #               'https://library.ucsd.edu/dc/object/bb0922726p')
    TC.assertEqual(srcRes['type'], 'still image')


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
