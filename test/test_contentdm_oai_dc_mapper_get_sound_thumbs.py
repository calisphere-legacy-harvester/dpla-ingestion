import os.path as path
from unittest import TestCase
from nose.plugins.attrib import attr
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=contentdm_oai_dc_get_sound_thumbs"
    return H.request(url, "POST", body=body)



def test_get_sound_thumbs():
    '''The isShownBy should be present for this mapper.
    These are contentdm types that have thumbs
    '''
    fixture = path.join(DIR_FIXTURES, 'cavpp_contentdm_oai.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    TC.assertEqual(obj['sourceResource']['type'], ['Sound'])
    TC.assertIn('isShownBy', obj)
    TC.assertEqual(
            obj['isShownBy'],
            'http://digitalcollections.lmu.edu/utils/getthumbnail/'
            'collection/johndblack/id/262')
