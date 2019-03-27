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
        self.assertEqual(obj['_id'], '27181--ark:/13030/tf8g5007bs')
        self.assertEqual(obj['id'], 'e71ec10bbbd23338f92398f49b5e87d5')
        self.assertEqual(
            obj['@id'],
            'http://ucldc.cdlib.org/api/items/e71ec10bbbd23338f92398f49b5e87d5')
        self.assertEqual(
            obj['isShownAt'],
            'https://digital.ucdavis.edu/collection/eastman/B-1/B-1160')
        self.assertEqual(
            obj['isShownBy'],
            'https://digital.ucdavis.edu/fcrepo/rest/collection/amerine-wine-labels/labels/label_2955/media/label_2955/svc:iiif/full/500,333/0/default.jpg'
        )
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['date'], '1940')
        self.assertEqual(srcRes['publisher'], 'University of California, Davis. General Library. Dept. of Special Collections')
        self.assertEqual(srcRes['subject'], [
            {
                'name': u'Spain'
            },
            {
                'name': u'Sherry'
            },
        ])
        self.assertEqual(srcRes['title'],
                         "\"Lakeview High School\" Lakeview, Ore")
        self.assertEqual(srcRes['creator'], "Eastman, Jervie Henry")
        self.assertEqual(srcRes['format'],
                         "1 photographic negative : b&w : 5 x 7 in.")
        self.assertEqual(srcRes['type'], "Photograph")
        self.assertEqual(srcRes['rightsURI'], "http://rightsstatements.org/vocab/InC-NC/1.0/")
