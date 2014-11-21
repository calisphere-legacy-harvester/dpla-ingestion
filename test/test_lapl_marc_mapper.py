# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=lapl_marc"
    return H.request(url, "POST", body=body,
            )

def test_lapl_creator():
    fixture = path.join(DIR_FIXTURES, 'lapl-marc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('530', INPUT)
        resp, content = _get_server_response(INPUT)
    assert str(resp.status).startswith("2"), str(resp) + "\n" + content

    doc = json.loads(content)
    TC.assertIn(u'sourceResource', doc)
    TC.assertIn(u'title', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['title'], [u'Olvera Street shop [graphic] /']) 
    TC.assertIn(u'description', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['description'][2],
            u'A man and two boys sit in front of an Olvera Street shop. A large sign on the right reads, "For Your Fortune Consult Princess Lorena - The Morning Star." Another sign posted above the doorway reads, "Chief Kut - Mescalero." It is not clear if the man sitting on the right is Chief Kut.')
    TC.assertIn(u'extent', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['extent'], [u'1 photographic print : 15 x 11 cm.'])
    TC.assertIn(u'identifier', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['identifier'], [u'(OCoLC)838675849'])
    TC.assertIn(u'spatial', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['spatial'][0], u'California')
    TC.assertEqual(doc['sourceResource']['spatial'][1], u'Los Angeles')
    TC.assertIn(u'specType', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['specType'], [u'Photograph/Pictorial Works'])
    TC.assertIn(u'type', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['type'], u'Image')
    TC.assertIn(u'isShownAt', doc)
    TC.assertEqual(doc['isShownAt'], u'http://jpg1.lapl.org/00101/00101746.jpg')
    TC.assertIn(u'isShownBy', doc)
    TC.assertEqual(doc['isShownBy'], u'http://jpg1.lapl.org/00101/00101746.jpg')
    TC.assertEqual(doc['sourceResource']['language'], [u'eng'])
    TC.assertEqual(doc['sourceResource']['date']['displayDate'], u'[ca. 19--]')
    TC.assertEqual(doc['sourceResource']['date'], {'begin':'19uu',
                                                'end':'19uu',
                                                'displayDate':'[ca. 19--]'
                                                })
    TC.assertEqual(len(doc['sourceResource']['subject']), 8) 
    TC.assertEqual(doc['sourceResource']['subject'][0], 
            'Signs and signboards--California--Los Angeles.')
    TC.assertEqual(doc['sourceResource']['contributor'], ['Torrez, Eloy.',
                        'Walker & Eisen.'])

if __name__ == "__main__":
    raise SystemExit("Use nosetests")

