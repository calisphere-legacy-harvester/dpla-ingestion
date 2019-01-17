import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class SanJose_PastPerfect_TestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=sanjose_pastperfect"
        return H.request(url, "POST", body=body)

    def test_nowebobject(self):
        fixture = path.join(DIR_FIXTURES, 'pastperfect_xml.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertFalse(obj['sourceResource'])
        self.assertNotIn('isShownAt', obj)
        self.assertNotIn('isShownBy', obj)

    def test_nothumb(self):
        fixture = path.join(DIR_FIXTURES, 'pastperfect_xml_nothumb.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertFalse(obj['sourceResource'])
        self.assertNotIn('isShownAt', obj)
        self.assertNotIn('isShownBy', obj)
