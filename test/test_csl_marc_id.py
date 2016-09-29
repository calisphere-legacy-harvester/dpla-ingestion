# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-
# test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + 'csl-marc-id'
    return H.request(url, "POST", body=body, headers={'Source': '26560'})


def test_csl_id_select():
    fixture = path.join(DIR_FIXTURES, 'csl-marc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('001', INPUT)
    resp, content = _get_server_response(INPUT)
    assert resp.status == 200
    obj = json.loads(content)
    TC.assertIn('_id', obj)
    TC.assertEqual(obj[u'_id'], '26560--001409080')
