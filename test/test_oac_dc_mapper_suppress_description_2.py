import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=oac_dc_suppress_desc_2"
    return H.request(url, "POST", body=body)

def _check_isShownBy(INPUT, EXPECTED):
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content)['isShownBy'], EXPECTED)

def test_oac_isShownAt():
    '''Verify that the isShownAt set by select-oac-id is still in data.
    '''
    INPUT = {
            'identifier':[{'attrib':{}, 'text':'http://ark.cdlib.org/ark:/bogus'},
                {'attrib':{}, 'text':'localid'}]
    }
    url = server() + "select-oac-id"
    resp, content = H.request(url, "POST", body=json.dumps(INPUT),
            headers={'Source': 'an-oac-collection-slug'})
    resp, content = _get_server_response(content)
    content = json.loads(content)
    TC.assertEqual(content['isShownAt'], 'http://ark.cdlib.org/ark:/bogus')

def test_suppress_description_2():
    '''Test that the 2nd value in description is suppressed'''
    fixture = path.join(DIR_FIXTURES, 'oac-xml.json')
    with open(fixture) as f:
        INPUT = f.read()
    resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    content_obj = json.loads(content)
    srcRes = content_obj['sourceResource']
    TC.assertEqual(len(srcRes['description']), 2) 
    TC.assertEqual(srcRes['description'],
            ["description1 comes through for suppressed collections",
             "description3 comes through for suppressed collections",
            ])
