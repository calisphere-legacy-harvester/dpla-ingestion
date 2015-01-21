import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "select-oac-id"
    return H.request(url, "POST", body=body,
            headers={'Source': 'an-oac-collection-slug'}
            )

def test_id_selected():
    '''Test that the id is grabbed '''
    INPUT = {
        'identifier':['http://ark.cdlib.org/ark:/bogus', 'localid']
    }
    EXPECTED = 'an-oac-collection-slug--http://ark.cdlib.org/ark:/bogus'
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content)['_id'], EXPECTED)
    TC.assertEqual(json.loads(content)['isShownAt'],
            'http://ark.cdlib.org/ark:/bogus')

if __name__=="__main__":
    raise SystemExit("Use nosetests")
