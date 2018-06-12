import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


class PastPerfect_XML_FeedTestCase(TestCase):
    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=pastperfect_xml"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'pastperfect_xml.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(obj['_id'],
                         '26935--000501E3-9133-4358-AE66-874944208261')
        self.assertEqual(obj['id'], 'ca1797b08177dc1fa18bb17d59be3ca9')
        self.assertEqual(
            obj['@id'],
            'http://ucldc.cdlib.org/api/items/ca1797b08177dc1fa18bb17d59be3ca9')
        self.assertEqual(
            obj['isShownAt'],
            'http://sacramento.pastperfectonline.com/photo/000501E3-9133-4358-AE66-874944208261'
        )
        self.assertEqual(
            obj['isShownBy'],
            'https://s3.amazonaws.com/pastperfectonline/images/museum_231/130/thumbs/1983001sbpmp02464.jpg'
        )
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['date'], '1966/09/28')
        self.assertEqual(srcRes['identifier'], ['000501E3-9133-4358-AE66-874944208261', '1994/007/013'])
        self.assertEqual(srcRes['subject'], [
            {
                'name': u'Memorabilia'
            },
            {
                'name': u'Interviews'
            },
            {
                'name': u'Military'
            },
            {
                'name': u'Lee, A.W.'
            },
        ])
        self.assertEqual(
            srcRes['title'],
            "Edwin A. Grebitus Sr. shown with his son Edwin A. Grebitus Jr. and Sacramento Mayor Walter Christensen (center)."
        )
        self.assertEqual(srcRes['creator'][0], "Denny Johnson")
        self.assertEqual(srcRes['format'][0], "Print")
