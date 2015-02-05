# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "oai-to-dpla"
    return H.request(url, "POST", body=body,
            )

def test_identifierToSrcRes():
    INPUT = { 'identifier': [
        'localid0', 'localid1' ]}
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['identifier'], 
        ['localid0', 'localid1' ])
