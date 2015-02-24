import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=ucsd_blacklight_dc"
    return H.request(url, "POST", body=body)

def test_ucsd_dc_mapping():
    #fixture = path.join(DIR_FIXTURES, 'ucsd-blacklight-missions-alta-california-obj.json')
    # at this point, the ucsd feed should be "jsonfied"
    # need to map from the jsonfied obj to sourceResource
    fixture = path.join(DIR_FIXTURES, 'ucsd-blacklight-camp-matthews-obj-jsonfied.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'], ['Camp Matthews, Rifle range, shed, storage'])
    TC.assertEqual(srcRes['collection'],  [{u'@id': u'https://registry-dev.cdlib.org/api/v1/collection/25563', u'name': u'Camp Matthews Photographs and Plans'}])
    TC.assertEqual(srcRes['date'],  { "displayDate": "1964",
                                      "end": "1964-12-31",
                                      "begin": "1964-01-01",
                                      })
    TC.assertEqual(srcRes['description'],  "a test description (added for testing)")
    TC.assertEqual(srcRes['creator'],  ['Mark Redar test creator'])
    TC.assertEqual(srcRes['contributor'],  [ "Mark Redar test contrib",
        "Mark Redar test2 contrib" ] )
    #TC.assertEqual(srcRes['language'],  '')
