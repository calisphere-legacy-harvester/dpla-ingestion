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


    def _chk_lang(self, INPUT, expected):
        resp, content = self._get_server_response(json.dumps(INPUT))
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(obj['sourceResource']['language'],
                expected)

    def testLanguageMapping(self):
        '''Test the various combos found'''
        INPUT = dict(collection = [{'resource_uri':'api/v1/123/'}],
                tid = 'bogus-id',
                uri = 'bogus-uri',
                metadata = {'ti':'bogus-title',
                    'lg': ["Arabic"]}
                )
        self._chk_lang(INPUT, 
                [{'name': 'Arabic', 'iso639_9': 'ara'}])
        INPUT['metadata']['lg'] = [ "Arabic; Chinese"]
        self._chk_lang(INPUT, 
                [{'name': 'Arabic', 'iso639_9': 'ara'},
                {'name': 'Chinese', 'iso639_9': 'chi'}])
        INPUT['metadata']['lg'] = [ "Arabic; French" ]
        self._chk_lang(INPUT, 
                [{'name': 'Arabic', 'iso639_9': 'ara'},
                {'name': 'French', 'iso639_9': 'fre'}])
        INPUT['metadata']['lg'] = [ "German" ]
        self._chk_lang(INPUT, 
                [{'name': 'German', 'iso639_9': 'ger'}])
        INPUT['metadata']['lg'] = [ "Greek" ]
        self._chk_lang(INPUT, 
                [{'name': 'Greek', 'iso639_9': 'gre'}])
        INPUT['metadata']['lg'] = [ "Hindu" ]
        self._chk_lang(INPUT, 
                [{'name': 'Hindu', 'iso639_9': 'hin'}])
        INPUT['metadata']['lg'] = [ "Italian" ]
        self._chk_lang(INPUT, 
                [{'name': 'Italian', 'iso639_9': 'ita'}])
        INPUT['metadata']['lg'] = [ "Russian" ]
        self._chk_lang(INPUT, 
                [{'name': 'Russian', 'iso639_9': 'rus'}])
        INPUT['metadata']['lg'] = [ "Spanish; Italian; German"]
        self._chk_lang(INPUT, 
                [{'name': 'Spanish', 'iso639_9': 'spa'},
                {'name': 'Italian', 'iso639_9': 'ita'},
                {'name': 'German', 'iso639_9': 'ger'}])
