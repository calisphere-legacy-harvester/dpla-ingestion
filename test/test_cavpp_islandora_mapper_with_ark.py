import os.path as path
from unittest import TestCase
from nose.plugins.attrib import attr
from server_support import server, H
from amara.thirdparty import json
from akara import logger

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=cavpp_islandora"
    return H.request(url, "POST", body=body)

@attr(uses_network='yes')
def test_cavpp_overrides():
    fixture = path.join(DIR_FIXTURES,
            'cavpp_islandora_with_ark.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(obj['isShownAt'], 'https://californiarevealed.org/islandora/object/cavpp%3A225041')
    TC.assertEqual(obj['isShownBy'][0],
      "https://californiarevealed.org/islandora/object/cavpp%3A225041/datastream/TN/view/Aerial%20View%20of%20Jonestown%2C%20Guyana%2C%20Circa%201977.jpg")
    srcRes = obj['sourceResource']
    TC.assertNotIn('http://cdm15972.contentdm.oclc.org/bogus',
            srcRes['identifier'])
    TC.assertNotIn('creator', srcRes)
    TC.assertEqual(srcRes['contributor'], [u'California Historical Society'])
    TC.assertEqual(srcRes['identifier'], [u'chi_000218', u'PC 010.05.0536', u'http://ark.cdlib.org/ark:/13030/kt0c6032hh'])
    TC.assertEqual(srcRes['provenance'],
                            [u"California Historical Society",
                            u"California Revealed is supported by the U.S. Institute of Museum and Library Services under the provisions of the Library Services and Technology Act, administered in California by the State Librarian."])
    TC.assertEqual(srcRes['extent'],
                            [u"Unknown",
                            u'1 Page of 1'])
    TC.assertEqual(srcRes['type'],[u'Still Image'])
    # TC.assertEqual(srcRes['genre'],[u'Nonfiction films'])
    TC.assertEqual(srcRes['date'],[u'1977-03'])
    TC.assertEqual(srcRes['description'],[u"35mm color slide."])
    TC.assertEqual(srcRes['rights'],[u"Copyrighted. Rights are owned by California Historical Society. Copyright Holder has given Institution permission to provide access to the digitized work online. Transmission or reproduction of materials protected by copyright beyond that allowed by fair use requires the written permission of the Copyright Holder. In addition, the reproduction of some materials may be restricted by terms of gift or purchase agreements, donor restrictions, privacy and publicity rights, licensing and trademarks. Works not in the public domain cannot be commercially exploited without permission of the copyright owner. Responsibility for any use rests exclusively with the user."])
