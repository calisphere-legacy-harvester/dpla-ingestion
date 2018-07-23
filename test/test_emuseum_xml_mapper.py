import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class eMuseum_XML_FeedTestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=emuseum_xml"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'eMuseum-xml.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(obj['_id'], '26251--11529')
        self.assertEqual(obj['id'], '748a227d50f2f9ea132f5748b8e89323')
        self.assertEqual(
            obj['@id'],
            'http://ucldc.cdlib.org/api/items/748a227d50f2f9ea132f5748b8e89323')
        self.assertEqual(obj['isShownAt'],
                         'http://digitalcollections.hoover.org/objects/11529')
        self.assertEqual(
            obj['isShownBy'],
            'https://img.youtube.com/vi/qxVJVE9oKg4/default.jpg'
        )
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['date'], '1914/1918?')
        self.assertEqual(
            srcRes['title'],
            "Money is power.  A war saving certificate in every Canadian home.  Get yours now at Post Offices or banks."
        )
        self.assertEqual(srcRes['type'], 'Image')
