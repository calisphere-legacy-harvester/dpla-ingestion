# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dedup-sourceresource"
    return H.request(url, "POST", body=body,
            )

def test_lapl_creator():
    fixture = path.join(DIR_FIXTURES, 'couchdb_doc_with_dups.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('subject', INPUT)
        orig_doc = json.loads(INPUT)
        resp, content = _get_server_response(INPUT)
    assert str(resp.status).startswith("2"), str(resp) + "\n" + content
    new_doc = json.loads(content)
    # make sure other stuff didn't change
    TC.assertEqual(orig_doc['originalRecord'],
                new_doc['originalRecord'])

    TC.assertEqual(orig_doc['_id'],
                new_doc['_id'])
    TC.assertEqual(orig_doc['id'],
                new_doc['id'])
    TC.assertEqual(orig_doc['object'],
                new_doc['object'])
    TC.assertEqual(orig_doc['isShownAt'],
                new_doc['isShownAt'])
    TC.assertNotEqual(orig_doc['sourceResource'],
                new_doc['sourceResource'])
    TC.assertEqual(len(new_doc['sourceResource']['relation']), 6)
    TC.assertEqual(new_doc['sourceResource']['relation'], 
            [u'http://www.oac.cdlib.org/findaid/ark:/13030/ft6k4007pc',
                u'http://bancroft.berkeley.edu/collections/jarda.html',
                u'hb158005k9',
                u'BANC PIC 1986.059--PIC',
                u'http://calisphere.universityofcalifornia.edu/',
                u'http://bancroft.berkeley.edu/']
            )
