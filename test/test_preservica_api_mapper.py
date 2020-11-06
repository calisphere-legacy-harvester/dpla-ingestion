# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json


DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=preservica_api"
    return H.request(url, "POST", body=body)

def test_map_dc_meta():
    '''Test that the DC meta values are pulled to sourceResource'''
    fixture = path.join(DIR_FIXTURES, 'preservica-api.json')
    with open(fixture) as f:
        INPUT = f.read()
    dobj = json.loads(INPUT)

    #select_id('CNUMERICID', dobj)
    resp, content = _get_server_response(json.dumps(dobj))
    TC.assertEqual(resp.status, 200)

    content_obj = json.loads(content)
    srcRes = content_obj['sourceResource']
    
    TC.assertEqual(srcRes['stateLocatedIn'], 'California')
    TC.assertEqual(srcRes['title'],
            [u'Two Oakland firefighters standing in front of fire station'])
    
    TC.assertEqual(srcRes['subject'],  [
                {u'name': u'African Americans--California--Oakland--History--Pictorial works.'},
                {u'name': u'Oakland (Calif.). Fire Department--Pictorial works.'},
                {u'name': u'Oakland (Calif.)--History--Pictorial works.'}
                ]) 
    TC.assertEqual(srcRes['description'],
                [u"Two Oakland firefighters standing in front of fire station [2327a]"])
    TC.assertEqual(srcRes['publisher'],
            [u'African American Museum & Library at Oakland (Oakland, Calif.)'])
    TC.assertNotIn('contributor', srcRes)
    TC.assertEqual(srcRes['date'], [u'circa 1950s'])
    TC.assertEqual(srcRes['type'], [u'image'])
    TC.assertEqual(srcRes['format'], [u'negatives (photographs)'])
    TC.assertEqual(srcRes['identifier'], [u'MS126_2327A'])
    TC.assertEqual(srcRes['source'],
            [u"Joseph (E. F.) Photograph Collection"])
    TC.assertEqual(srcRes['language'], [u'eng'])
    TC.assertEqual(srcRes['relation'],
            [u'http://www.oac.cdlib.org/findaid/ark:/13030/c8930w8p/'])
    TC.assertNotIn('spatial', srcRes)
    TC.assertEqual(srcRes['rights'], 
        ["Copyrighted. Rights are owned by the African American Museum & Library at Oakland. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the copyright owner. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."])
    TC.assertEqual(content_obj['isShownAt'],
           'https://oakland.access.preservica.com/file/sdb:digitalFile%7C8c81f065-b6e4-457e-8b76-d18176f74bee/')
    TC.assertEqual(content_obj['isShownBy'],
            'https://oakland.access.preservica.com/download/thumbnail/sdb:digitalFile%7C8c81f065-b6e4-457e-8b76-d18176f74bee')


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

