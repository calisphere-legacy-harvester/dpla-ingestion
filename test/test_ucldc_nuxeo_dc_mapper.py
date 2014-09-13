import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=ucldc_nuxeo_dc"
    return H.request(url, "POST", body=body)

def test_ucla_mapping():
    fixture = path.join(DIR_FIXTURES, 'ucldc-nuxeo.json')
    with open(fixture) as f:
        INPUT = f.read()
        resp, content = _get_server_response(INPUT)
        assert resp.status == 200
        obj = json.loads(content)
        TC.assertIn('isShownAt', obj)
        TC.assertIn('sourceResource', obj)
        srcRes = obj['sourceResource']
        TC.assertEqual(srcRes['title'],  "Adeline Cochems having her portrait taken by her father Edward W, Cochems in Santa Ana, California: Photograph")
        TC.assertEqual(srcRes['creator'], 'system')
#        TC.assertEqual(srcRes['created'], "2014-01-23T08:26:49.59Z")
        TC.assertEqual(srcRes['subject'], [])

