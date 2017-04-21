import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class UCB_BAMPFA_Solr_FeedTestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=ucb_bampfa_solr"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'bampfa.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(
            obj['isShownAt'],
            'https://webapps.cspace.berkeley.edu/bampfa/search/search/?idnumber=1965.35&displayType=full&maxresults=1&start=1'
        )
        self.assertEqual(
            obj['isShownBy'],
            'https://webapps.cspace.berkeley.edu/bampfa/imageserver/blobs/7b52d372-524a-4de8-bbf2/derivatives/Medium/content'
        )
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['creator'], 'Savoldo, Giovanni')
        self.assertEqual(srcRes['title'], 'Pieta with Three Saints')
        self.assertEqual(srcRes['date'], '1529')
        self.assertEqual(srcRes['extent'], '43 5/8 x 60 3/8 in.')
        self.assertEqual(srcRes['identifier'], '1965.35')
        self.assertEqual(srcRes['genre'], 'Painting')
        self.assertEqual(srcRes['format'], 'oil on canvas')
        self.assertEqual(srcRes['provenance'], 'Museum Purchase')
        self.assertEqual(srcRes['subject'],
                         [u'History', u'Figure-Male', u'Figure-Portrait'])

    def testInt(self):
        fixture = path.join(DIR_FIXTURES, 'bampfa-int.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['title'], '981')
