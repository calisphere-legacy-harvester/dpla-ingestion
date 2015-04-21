import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

class UCSF_XML_FeedTestCase(TestCase):

    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=ucsf_xml"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'ucsf-doc.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(obj['_id'], '26100--nga13j00')
        self.assertEqual(obj['isShownAt'],
                'http://legacy.library.ucsf.edu/tid/nga13j00')
        self.assertEqual(obj['isShownBy'],
                'http://legacy.library.ucsf.edu/tid/nga13j00/pdf')
        self.assertEqual(obj['sourceResource']['creator'],
                ['Mark Redar', u'Whent, Peter', u'Namelex Holdings Limited'])
        self.assertEqual(obj['sourceResource']['date'],
                ['20030410 (April 10, 2003) '])
        self.assertEqual(obj['sourceResource']['description'],
                [u'Gallaher v Tlais 2005 Folio 185'])
        self.assertEqual(obj['sourceResource']['extent'],
                "1 page")
