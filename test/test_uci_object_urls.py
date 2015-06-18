import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "uci-object-urls"
    return H.request(url, "POST", body=body)

def test_uci_object_urls():
    fixture = path.join(DIR_FIXTURES, 'uci-oai-enriched-once.json')
    with open(fixture) as f:
        INPUT = f.read()
        resp, content = _get_server_response(INPUT)
        print resp.status
        assert resp.status == 200
        obj = json.loads(content)
        TC.assertEqual(obj['isShownAt'], "http://hdl.handle.net/10575/11971")
        TC.assertEqual(obj['isShownBy'],
                "http://ucispace-prod.lib.uci.edu/xmlui/bitstream/10575/11971/3/VAOHP0138_F01_Viet.pdf")
