import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=csudh_contentdm_oai_dc"
    return H.request(url, "POST", body=body)

def test_csudh_contentdm_title_with_local_id():
    # at this point, the ucsd feed should be "jsonfied"
    # need to map from the jsonfied obj to sourceResource
    fixture = path.join(DIR_FIXTURES,
            'csudh_contentdm_oai_1.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'],
            ["Young Masaichi Ishibashi"]
            )
    TC.assertEqual(srcRes['identifier'], [ 
       "ISH_033",
       "http://cdm16855.contentdm.oclc.org/cdm/ref/collection/p16855coll4/id/2504",
       "csudh_ish_0032"
    ])

def test_csudh_contentdm_title_with_ARK():
    fixture = path.join(DIR_FIXTURES,
            'csudh_contentdm_oai_2.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'],
            ["World Friendship Group "]
            )
    TC.assertEqual(srcRes['identifier'], [ 
       "2490_P16",
       "http://cdm16855.contentdm.oclc.org/cdm/ref/collection/p16855coll4/id/610"
    ])
