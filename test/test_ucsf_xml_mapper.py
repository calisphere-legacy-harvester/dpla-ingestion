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
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['creator'],
                ['Mark Redar', u'Whent, Peter', u'Namelex Holdings Limited'])
        self.assertEqual(srcRes['date'],
                ['20030410 (April 10, 2003)'])
        self.assertEqual(srcRes['description'],
                [u'Gallaher v Tlais 2005 Folio 185'])
        self.assertEqual(srcRes['extent'],
                "1 page")
        self.assertEqual(srcRes['language'],
                [{'name':'English', 'iso639_9': 'eng'}])
        self.assertEqual(srcRes['spatial'],
                ["Jordan", "Syria", "UK", "Ukraine"])
        self.assertEqual(srcRes['subject'],
                    [u'Gallaher International Limited',
                     u'Gallaher Ltd',
                     u'Tlais Enterprises Limited',
                     u'Gallaher International Limited',
                     u'Farah, Simon',
                     u'Simon'])
        self.assertEqual(srcRes['title'],
            ["[Memo from Peter Whent to Simon Faith regarding reimbursing instructions]"])
        self.assertEqual(srcRes['format'],
                ['memo', 'notes'])


    def testLanguageMapping(self):
        '''Test the various combos found'''
        pass
        '''
"Arabic"
"Arabic; Chinese"
"Arabic; French"
"Arabic; German"
"Arabic; Hindu"
"Arabic; Russian"
"Chinese"
"French"
"French; German"
"French; Italian"
"German"
"Greek"
"Hindu"
"Italian"
"Russian"
"Russian; Greek"
"Spanish"
"Spanish; Arabic"
"Spanish; French"
"Spanish; Italian"
"Spanish; Italian; German"
'''
