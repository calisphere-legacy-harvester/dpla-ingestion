import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=ucsd_blacklight_dc"
    return H.request(url, "POST", body=body)

def test_ucsd_dc_mapping():
    fixture = path.join(DIR_FIXTURES, 'ucsd-blacklight-camp-matthews-obj.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
        assert resp.status == 200
        obj = json.loads(content)
        TC.assertIn('sourceResource', obj)
        srcRes = obj['sourceResource']
        TC.assertEqual(srcRes['collection'],  [{u'@id': u'https://registry-dev.cdlib.org/api/v1/collection/25563', u'name': u'Camp Matthews Photographs and Plans'}])
        TC.assertEqual(srcRes['language'],  [{"name":"No linguistic content","code":"zxx","externalAuthority":"http://id.loc.gov/vocabulary/iso639-2/zxx"}])
        TC.assertEqual(srcRes['date'],  [{"beginDate":"1964-01-01","endDate":"1964-12-31","value":"1964","type":"creation","encoding":"w3cdtf"}])
        TC.assertEqual(srcRes['title'],  [{"name":"Camp Matthews, Rifle range, shed, storage", "external":[], "value":"Camp Matthews, Rifle range, shed, storage", "nonSort":"","partName":"","partNumber":"", "subtitle":"","variant":"","translationVariant":"", "abbreviationVariant":"","acronymVariant":"","expansionVariant":""}])
        TC.assertEqual(srcRes['description'],  [{u'displayLabel': u'Physical description', u'type': u'general physical description', u'value': u'1 2.25 inch black and white negative'}, {u'displayLabel': u'fileName', u'type': u'identifier', u'value': u'039.tif'}, {u'displayLabel': u'ARK', u'type': u'identifier', u'value': u'http://libraries.ucsd.edu/ark:/20775/bb0922726p'}, {u'displayLabel': u'Digital source type', u'type': u'digitalOrigin', u'value': u'reformatted digital'}, {u'displayLabel': u'Digital object made available by', u'type': u'', u'value': u'Mandeville Special Collections Library, University of California, San Diego, La Jolla, 92093-0175 (http://libraries.ucsd.edu/locations/mscl/)'}, {u'displayLabel': u'negative', u'type': u'identifier', u'value': u'an3_r4025_39'}, {u'displayLabel': u'Location of Originals', u'type': u'existence and location of originals', u'value': u'This digital image is a surrogate of Neg. No. an3_r4025_39 from the Office of the Assistant Vice Chancellor. Facilities Design and Construction Camp Matthews Buildings Photographs (RSS 4025)'}])
