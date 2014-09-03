import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "ucla-solr-to-dpla"
    return H.request(url, "POST", body=body)

def test_ucla_mapping():
    fixture = path.join(DIR_FIXTURES, 'ucla-solr-bartlett-obj.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('PID', INPUT)
        resp, content = _get_server_response(INPUT)
        assert resp.status == 200
        obj = json.loads(content)
        TC.assertIn('isShownAt', obj)
        TC.assertEqual(obj['isShownAt'], 'http://digital.library.ucla.edu/collections/islandora/object/edu.ucla.library.specialCollections.bartlett:1747')
        TC.assertIn('isShownBy', obj)
        TC.assertEqual(obj['isShownBy']['src'], 'http://digital.library.ucla.edu/collections/islandora/object/edu.ucla.library.specialCollections.bartlett:1747/datastream/JPG/JPG.jpg')
        TC.assertIn('sourceResource', obj)
        srcRes = obj['sourceResource']
        TC.assertEqual(srcRes['subject'], [u'Postal service $z United States', u'Delivering $z United States', u'Drum Barracks (Los Angeles, Calif.)', u'Camels $z United States', u''])
        TC.assertEqual(srcRes['contributor'], [u'University of California, Los Angeles. $b Library. $b Dept. of Special Collections (repository)'])
        TC.assertEqual(srcRes['spatial'], [u"California--Los Angeles--Wilmington"])
        TC.assertEqual(srcRes['creator'], [u'Heathcote, Basil'])
        TC.assertEqual(len(srcRes['description']), 4)
        TC.assertEqual(srcRes['description'][0], "Text from nitrate negative sleeve: 1823 - 1824 253R1694 2 negs, 1929.  Photo by Adelbert Bartlett, 535 15th Street, Santa Monica, Calif.  Drum Barracks, 1862-68, offcers qtrs. U.S. Army, Wilmington (now in Los Angeles at L.A. Harbor) Calif. (see story attached)")
        TC.assertEqual(srcRes['format'], [u'1 p.',])
        TC.assertEqual(srcRes['identifier'], [u'edu.ucla.library.specialCollections.bartlett:1747', u'uclamss_1300_1775i', u'1775i'])
        TC.assertEqual(srcRes['language'], [u'eng'])
        TC.assertEqual(srcRes['relation'], [u'Adelbert Bartlett Papers. Department of Special Collections, Charles E. Young Research Library, UCLA.'])
        TC.assertEqual(srcRes['subject'], [u'Postal service $z United States', u'Delivering $z United States', u'Drum Barracks (Los Angeles, Calif.)', u'Camels $z United States', u''])
        TC.assertEqual(srcRes['title'], [u'Photograph of 3rd page of Los Angeles Times Sunday Magazine story about Drum Barracks, "When Camels Carried Mail to California," by Basil Heathcote, 1930'])
        TC.assertEqual(srcRes['type'], [ "clippings", "StillImage" ])

if __name__=="__main__":
    test_ucla_mapping()
    #raise SystemExit("Use nosetests")
