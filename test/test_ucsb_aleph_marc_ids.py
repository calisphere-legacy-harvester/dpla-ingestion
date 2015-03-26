# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + 'ucsb-aleph-marc-id'
    return H.request(url, "POST", body=body,
            headers={'Source': '113'}
            )

def test_ucsb_aleph_marc_id_select():
    fixture = path.join(DIR_FIXTURES, 'ucsb-aleph-marc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('035', INPUT)
        resp, content = _get_server_response(INPUT)
        assert resp.status == 200
        obj = json.loads(content)
        TC.assertIn('_id', obj)
        TC.assertEqual(obj[u'_id'], '113--http://www.library.ucsb.edu/OBJID/Cylinder0002')

