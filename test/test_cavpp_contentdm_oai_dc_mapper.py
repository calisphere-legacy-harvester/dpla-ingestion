import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=cavpp_contentdm_oai_dc"
    return H.request(url, "POST", body=body)

def test_cavpp_overrides():
    fixture = path.join(DIR_FIXTURES,
            'contentdm_oai.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(obj['isShownAt'], 'http://archive.org/details/cubanc_000177')
    TC.assertEqual(obj['isShownBy'], 
      "http://digitalcollections.lmu.edu/utils/getthumbnail/collection/johndblack/id/262")
    srcRes = obj['sourceResource']
    TC.assertNotIn('http://cdm15972.contentdm.oclc.org/bogus',
            srcRes['identifier'])
    TC.assertEqual(srcRes['identifier'], 
                            [u'http://archive.org/details/cubanc_000177',
                             u'sc_jdbp001110001',
                             u'sc_jdbp00111',
u'http://digitalcollections.lmu.edu/cdm/ref/collection/johndblack/id/262'])
            
