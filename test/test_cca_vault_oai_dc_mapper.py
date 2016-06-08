# -*- coding: utf-8 -*-

import os.path as path
from unittest import TestCase
from nose.plugins.attrib import attr
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=cca_vault_oai_dc"
    return H.request(url, "POST", body=body)

def test_cca_vault_oai_dc_mapping():
    fixture = path.join(DIR_FIXTURES,
            'cca_vault.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    TC.assertEqual(obj['isShownAt'],
    'https://vault.cca.edu/items/52167916-597c-4bbd-8af2-ce33bf6e4659/0/')
    TC.assertEqual(obj['isShownBy'],
    'https://vault.cca.edu/thumbs/52167916-597c-4bbd-8af2-ce33bf6e4659/0/?gallery=preview')
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'],
            ["Reading Room",])
    TC.assertEqual(srcRes['description'],[
        "Mural and scroll installation involving poetry by Chinese-American immigrants held at the Chinese Affirmative Action Community Room, Kuo Building. In same file as Resident Alien."])

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

