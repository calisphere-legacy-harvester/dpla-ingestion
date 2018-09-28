import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class UCD_JSON_TestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=ucd_json"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'ucd.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(obj['_id'], '27181--B-1160')
        self.assertEqual(obj['id'], 'e60b2fe59ab111ec9af42e7636bd682c')
        self.assertEqual(
            obj['@id'],
            'http://ucldc.cdlib.org/api/items/e60b2fe59ab111ec9af42e7636bd682c')
        self.assertEqual(
            obj['isShownAt'],
            'https://digital.ucdavis.edu/record/collection/eastman/B-1/B-1160')
        self.assertEqual(
            obj['isShownBy'],
            'https://digital.ucdavis.edu/fcrepo/rest/collection/eastman/B-1/B-1160/media/web'
        )
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['date'], '1940')
        self.assertEqual(srcRes['subject'], [
            {
                'name': u'Animals'
            },
            {
                'name': u'Fish'
            },
        ])
        self.assertEqual(srcRes['title'],
                         "\"Lakeview High School\" Lakeview, Ore")
        self.assertEqual(srcRes['creator'][0], "Eastman, Jervie Henry")
        self.assertEqual(srcRes['format'],
                         "1 photographic negative : b&w : 5 x 7 in.")
        self.assertEqual(srcRes['type'], "Photograph")
        self.assertEqual(srcRes['rightsURI'], "http://rightsstatements.org/vocab/InC-NC/1.0/")
