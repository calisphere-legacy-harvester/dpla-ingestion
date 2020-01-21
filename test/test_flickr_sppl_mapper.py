# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-
# python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class FlickrSDASMMapperTestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=flickr_sppl"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'flickr-sppl.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(
            obj['isShownAt'],
            'https://www.flickr.com/photos/sopaslibrary/8720603651/')
        self.assertEqual(
            obj['isShownBy'],
            'https://farm8.staticflickr.com/7360/8720603651_65705ed155_z.jpg')
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['title'], 'South Pasadena High School')
        self.assertEqual(srcRes['date'], '1908')
        self.assertEqual(srcRes['subject'], [
            'south pasadena', 'south pasadena public library', 'sppl',
            'schools'
        ])
        self.assertEqual(srcRes['format'], "photo")
        self.assertEqual(
            srcRes['identifier'],
            ['<a href=\"http://ark.cdlib.org/ark:/13030/kt2199q7mk\" rel=\"noreferrer nofollow\">ark.cdlib.org/ark:/13030/kt2199q7mk</a>', 'csp_138', 'LP1399'])


# Copyright © 2017, Regents of the University of California
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
