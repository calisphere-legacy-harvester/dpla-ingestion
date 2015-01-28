# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "lapl-oai-isShown-26096"
    return H.request(url, "POST", body=body,
            )


def test_isShown():
    INPUT = {'originalRecord': { 'identifier': [
        'rescarta.lapl.org/jsp/RcWebImageViewer.jsp?doc_id=026bc4f2-52f9-4cbf-b1e4-12291b1cd6d0/LPU00000/LL000001/00000004' ]}
        }
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['isShownAt'], 
        'http://rescarta.lapl.org/ResCarta-Web/jsp/RcWebImageViewer.jsp?doc_id=026bc4f2-52f9-4cbf-b1e4-12291b1cd6d0/LPU00000/LL000001/00000004'
        )
    TC.assertEqual(content['isShownBy'], 
        'http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id=LPU00000/LL000001/00000004'
        )
