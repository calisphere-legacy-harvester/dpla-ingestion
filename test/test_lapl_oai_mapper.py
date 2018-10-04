# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=lapl_oai"
    return H.request(
        url,
        "POST",
        body=body, )


def test_lapl_oai_mapping():
    fixture = path.join(DIR_FIXTURES, 'lapl-oai.json')
    with open(fixture) as f:
        INPUT = f.read()
        resp, content = _get_server_response(INPUT)
    assert str(resp.status).startswith("2"), str(resp) + "\n" + content
    doc = json.loads(content)
    TC.assertIn(u'sourceResource', doc)
    TC.assertIn(u'title', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['title'][0],
                   u'Olvera Street shop')
    TC.assertIn(u'description', doc[u'sourceResource'])
    TC.assertEqual(len(doc['sourceResource']['description']), 2)
    TC.assertEqual(
        doc['sourceResource']['description'][1],
        u'A man and two boys sit in front of an Olvera Street shop. A large sign on the right reads, "For Your Fortune Consult Princess Lorena - The Morning Star." Another sign posted above the doorway reads, "Chief Kut - Mescalero." It is not clear if the man sitting on the right is Chief Kut.'
    )
    TC.assertIn(u'format', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['format'][0],
                   u'1 photographic print :b&amp;w ;15 x 11 cm.')
    TC.assertIn(u'identifier', doc[u'sourceResource'])
    TC.assertEqual(len(doc['sourceResource']['identifier']), 5)
    TC.assertEqual(doc['sourceResource']['identifier'][2], u'N-011-201 8x10')
    TC.assertIn(u'isShownAt', doc)
    TC.assertEqual(
        doc['isShownAt'],
        u'https://tessa.lapl.org/cdm/ref/collection/photos/id/36479'
    )
    TC.assertIn(u'isShownBy', doc)
    TC.assertEqual(doc['isShownBy'],
                   u'http://173.196.26.125/utils/ajaxhelper?CISOROOT=photos&CISOPTR=36479&action=2&DMHEIGHT=2000&DMWIDTH=2000&DMSCALE=100')
    TC.assertEqual(len(doc['sourceResource']['subject']), 8)
    TC.assertEqual(doc['sourceResource']['subject'][0],
                   {'name': 'Signs and signboards--California--Los Angeles.'})
    TC.assertEqual(doc['sourceResource']['contributor'],
                   ['Made accessible through a grant from the John Randolph Haynes and Dora Haynes Foundation.'])
    TC.assertEqual(doc['sourceResource']['creator'], ['Schultheis, Herman.'])


if __name__ == "__main__":
    raise SystemExit("Use nosetests")
