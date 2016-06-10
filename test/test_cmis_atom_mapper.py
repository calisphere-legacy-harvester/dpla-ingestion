# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json
from dplaingestion.akamod.select_cmis_atom_id import select_id

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=cmis_atom"
    return H.request(url, "POST", body=body)

def test_map_oac_dc_meta():
    '''Test that the DC meta values from OAC are pulled to sourceResource'''
    fixture = path.join(DIR_FIXTURES, 'preservica-cmis-atom-entry.json')
    with open(fixture) as f:
        INPUT = f.read()
    dobj=json.loads(INPUT)
    select_id('CNUMERICID', dobj)
    resp, content = _get_server_response(json.dumps(dobj))
    TC.assertEqual(resp.status, 200)
    content_obj = json.loads(content)
    srcRes = content_obj['sourceResource']
    TC.assertEqual(len(srcRes['title']), 1)
    TC.assertEqual(srcRes['title'],
            ['The Phyllis Wheatley Reporter vol. 1 no. 1'])
    TC.assertEqual(srcRes['creator'], [u'Phyllis Wheatley YWCA.'])
    TC.assertEqual(srcRes['subject'],  [
                {u'name': u'African American women--Societies and clubs.'},
                {u'name': u'Phyllis Wheatley YWCA--History.'},])
    TC.assertEqual(srcRes['description'], 
                ["The Phyllis Wheatley Reporter vol. 1 no. 1"])
    TC.assertEqual(srcRes['publisher'],
            [u'African American Museum & Library at Oakland (Oakland, Calif.)'])
    TC.assertNotIn('contributor', srcRes)
    TC.assertEqual(srcRes['date'], [u'1960-03'])
    TC.assertEqual(srcRes['type'], [u'text'])
    TC.assertEqual(srcRes['format'], [u'newsletters'])
    TC.assertEqual(srcRes['identifier'], [u'MS110_B01_F07_002'])
    TC.assertEqual(srcRes['source'],
            [u"Young Women's Christian Association Collection"])
    TC.assertEqual(srcRes['language'], [u'eng'])
    TC.assertEqual(srcRes['relation'],
            [u'http://www.oac.cdlib.org/findaid/ark:/13030/c84b3311/'])
    TC.assertEqual(srcRes['spatial'], [{'name': 'Coverage Test Value'}])
    TC.assertEqual(srcRes['rights'][0][:12], "Copyrighted.")
    TC.assertEqual(content_obj['isShownAt'],
            'https://oakland.access.preservica.com/file/sdb:digitalFile|sdb:digitalFile|ddf962b3-e763-4838-b149-f87eef10504b')

if __name__=="__main__":
    raise SystemExit("Use nosetests")


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

