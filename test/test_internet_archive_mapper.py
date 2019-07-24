# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-
# python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class InternetArchiveMapperTestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=internet_archive"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'internet-archive-doc.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['title'],
                         "Edith Heath: Oral History presentation")
        self.assertEqual(
            srcRes['description'],
            "This oral history presentation interviews both Edith and Brian Heath, and includes information on 50 years of business in Sausalito. People discussed include Brian Heath, Edith Heath, Mary Ruiz, Nash Ruiz, Rosalie Ross, Leon Galleto, Daphne Ahlenius, and Bill Palmer. This is an unedited video."
        )
        self.assertEqual(srcRes['subject'],
                         ['Edith Heath', 'ceramics', 'art', 'Sausalito'])
        self.assertEqual(srcRes['type'], "texts")
        self.assertEqual(obj['isShownAt'],
                         'https://archive.org/details/VIDEOTS_20180308_1939')
        self.assertEqual(
            obj['isShownBy'],
            'https://archive.org/services/img/VIDEOTS_20180308_1939')


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
