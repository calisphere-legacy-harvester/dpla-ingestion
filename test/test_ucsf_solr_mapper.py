import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

class UCSF_Solr_FeedTestCase(TestCase):

    def _get_server_response(self, body):
        url = server() + "dpla_mapper?mapper_type=ucsf_solr"
        return H.request(url, "POST", body=body)

    def testMappings(self):
        fixture = path.join(DIR_FIXTURES, 'ucsf-solr-doc.json')
        with open(fixture) as f:
            INPUT = f.read()
            resp, content = self._get_server_response(INPUT)
        self.assertEqual(resp.status, 200)
        obj = json.loads(content)
        self.assertEqual(obj['_id'], '26100--ctg37j00')
        self.assertEqual(obj['id'], 'e78f57840bb57365ca30e57e1af2ae26')
        self.assertEqual(obj['isShownAt'],
            'https://industrydocuments.library.ucsf.edu/tobacco/docs/#id=kylw0221')
        self.assertEqual(obj['isShownBy'],
                'https://s3-us-west-2.amazonaws.com/edu.ucsf.library.iddl.artifacts/t/s/w/b/kylw0221/kylw0221_thumb.png')
        srcRes = obj['sourceResource']
        self.assertEqual(srcRes['title'], ['In Re: Engle Progeny Cases \
Tobacco Litigation. Pertains to Andy R. Allen, Sr., \
as Personal Representative for the Estate of Patricia \
L. Allen. Jury Trial'] )
        self.assertEqual(srcRes['extent'], '155 pages')
        self.assertEqual(srcRes['creator'], ["GANNON, SEAN L."])
        self.assertEqual(srcRes['date'], ["2014 November 25"])
        self.assertEqual(srcRes['description'],[
                "ATCH, ATTACHMENTS MISSING", "MARG, MARGINALIA"])
        self.assertEqual(srcRes['genre'], ["trial transcript"])
        self.assertEqual(srcRes['identifier'], [u'kylw0221', u'ctg37j00',
                u'figlarj20141125',
                u'Engle Progeny; Andy R. Allen, Sr. and Patricia L. Allen, \
Case No. 16-2007-CA-008311-BXXX-MA, Case No. 2008-CA-15000'])
        #NEED SAMPLE self.assertEqual(srcRes['language'], [])
        self.assertEqual(srcRes['subject'], [u'CAMEL', u'ABC TV', u'ABC',
            u'ACEP', u'AECA', u'AIR SUPPLY', u'AMERICA', u'BEST TALK IN TOWN'])
        self.assertEqual(srcRes['spatial'], [{'text':'South Africa'},
            {'text': 'Iran'}, {'text': 'Germany'}]),
        self.assertEqual(srcRes['relation'], ["Gallaher"])
