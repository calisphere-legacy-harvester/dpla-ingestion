import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=chula_vista_pl_contentdm_oai_dc"
    return H.request(url, "POST", body=body)

def test_cvpl_contentdm_isShownValues():
    # at this point, the ucsd feed should be "jsonfied"
    # need to map from the jsonfied obj to sourceResource
    fixture = path.join(DIR_FIXTURES,
            'chula_vista_pl_contentdm_oai.json')
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
            ["The Sail"]
            )
    TC.assertEqual(srcRes['identifier'], [ 
        u'http://archives.chulavistalibrary.com:2009/u?/CVPublicArt,100'
    ])
    TC.assertEqual(obj['isShownAt'],  
        u'http://archives.chulavistalibrary.com:2009/u?/CVPublicArt,100'
    )
    TC.assertEqual(obj['isShownBy'],
        u'http://archives.chulavistalibrary.com:2009/cgi-bin/getimage.exe?DMSCALE=20&CISOROOT=/CVPublicArt&CISOPTR=100')
