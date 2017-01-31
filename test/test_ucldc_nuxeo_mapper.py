# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json
from akara import logger

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=ucldc_nuxeo"
    return H.request(url, "POST", body=body)

def test_ucldc_nuxeo_mapping():
    fixture = path.join(DIR_FIXTURES, 'ucldc-nuxeo.json')
    with open(fixture) as f:
        INPUT = f.read()
        resp, content = _get_server_response(INPUT)
        assert resp.status == 200
        obj = json.loads(content)
        TC.assertIn('isShownAt', obj)
        TC.assertIn('isShownBy', obj)
        TC.assertEqual(obj['isShownBy'], "http://example.edu/this/is/image/URL")
        TC.assertEqual(obj['isShownAt'],
                "https://calisphere.org/item/40677ed1-f7c2-476f-886d-bf79c3fec8c4")
        TC.assertIn('sourceResource', obj)
        srcRes = obj['sourceResource']
        logger.error(srcRes)
        TC.assertIn('originalRecord', obj)
        origRec = obj['originalRecord']
        logger.error(origRec)
        TC.assertEqual(srcRes['alternativeTitle'], [])
        TC.assertEqual(srcRes['contributor'], [])
        TC.assertEqual(srcRes['creator'], ["Cochems, Edward W. (Edward William), 1874-1949"])
        TC.assertEqual(origRec['date'], ["1919 - 1949"])
        TC.assertEqual(srcRes['description'], ["First picture of Adeline Cochems (Mrs. Weston Walker) and one of the first pictures Cochems took while practicing with his daughter as model"])
        TC.assertNotIn('extent', srcRes)
        TC.assertEqual(srcRes['format'], "Photographic print")
        TC.assertEqual(srcRes['genre'], [])
        TC.assertEqual(srcRes['identifier'], ["testID", "633"])
        TC.assertEqual(srcRes['language'], [])
        TC.assertEqual(srcRes['spatial'],[{"text": "Santa Ana (Calif.)"}])
        TC.assertEqual(srcRes['publisher'], [])
        TC.assertNotIn('relation', srcRes)
        TC.assertEqual(srcRes['rights'], ["Copyrighted", "This material is provided for private study, scholarship, or research. Transmission or reproduction of any material protected by copyright beyond that allowed by fair use requires the written permission of the copyright owners. The creators of the material or their heirs may retain copyright to this material."])
        TC.assertEqual(srcRes['subject'], ["Photographers -- Photographs"])
        TC.assertEqual(srcRes['temporalCoverage'], [])
        TC.assertEqual(srcRes['title'],
                [u"Adeline Cochems having her portrait taken by her father Edward W, Cochems in Santa Ana, California: Photograph"])
        TC.assertEqual(srcRes['type'], "image")
        TC.assertNotIn('source', origRec)
        TC.assertEqual(origRec['provenance'], [])
        TC.assertEqual(origRec['location'], "Box 6 : Folder 3")
        TC.assertNotIn('rightsHolder', origRec)
        TC.assertNotIn('rightsNote', origRec)
        TC.assertNotIn('dateCopyrighted', origRec)
        TC.assertNotIn('transcription', origRec)

def test_ucldc_nuxeo_mapping_typed_descriptions():
    '''Test when the "typed" values of description from ucldc schema are
    in the metadata.
    Records of this type have  dc.des
    '''
    fixture = path.join(DIR_FIXTURES, 'ucldc-nuxeo_typed_description.json')
    INPUT = open(fixture).read()
    resp, content = _get_server_response(INPUT)
    assert resp.status == 200
    obj = json.loads(content)
    TC.assertIn('isShownAt', obj)
    TC.assertIn('sourceResource', obj)
    srcRes = obj['sourceResource']
    TC.assertIn('originalRecord', obj)
    TC.assertEqual(srcRes['description'],
        [u'Medium: Silk, plain weave, stencil-printed warp and weft threads (heiy\u0139\x8d-gasuri meisen)',
         u'Annotations/Markings: No signature, seals, or inscriptions.',
         u'Acquisition: Partial Gift/Partial Purchase from Natalie Fitz-Gerald',
         u'Exhibitions: Japan & Beyond: The Yoshida Family Legacy in Japanese Woodblock Prints',
         u'Biography/History: 20th century artist',
         ]
      )
