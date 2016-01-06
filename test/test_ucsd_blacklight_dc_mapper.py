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
    # at this point, the ucsd feed should be "jsonfied"
    # need to map from the jsonfied obj to sourceResource
    fixture = path.join(DIR_FIXTURES,
            'ucsd-blacklight-camp-matthews-obj-jsonfied.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'],
            ['Camp Matthews, Rifle range, shed, storage'])
    TC.assertEqual(srcRes['date'],  [{ "displayDate": "1964",
                                      "end": "1964-12-31",
                                      "begin": "1964-01-01",
                                      }])
    TC.assertEqual(srcRes['description'],
           [ u'arrangement-val',
            u'A bibliography',
            u'bibliography-val',
            u'biography-val',
            u'credits-val',
            u'custodial history-val',
            u'a test description (added for testing)',
            u'description-val',
            u'digital origin',
            u'edition-val',
            u'funding-val',
            u'inscription-val',
            u'local attribution-val',
            u'location of originals-val',
            u'material details-val',
            u'performers-val',
            u'preferred citation-val',
            u'publication-val',
            u'related publications-val',
            u'scope and content-val',
            u'series-val',
            u'site-val',
            u'statement of responsibility-val',
            u'table of contents-val',
            u'technical requirements-val',
            u'A Thesis title',
            u'thesis-val',
            u'venue-val',
            u'This data represent a snapshot, or instant in time, from the cosmology simulation. This snapshot was taken at a redshift of 1.5, which is 4.2 billion years after the Big Bang. At this point, the simulation had created 207,076 grids and 374 galaxy clusters with masses of at least 10^14 solar masses. The primary contents are the parameter files, hierarchy file (description of grid sizes and spatial locations), and grid data. For a complete description of the contents, refer to the Scope and Contents note for the collection. In the Derived Data subcomponent, there are text, binary, and images files representing halo properties and the projections of various physical fields.'
            ]
    )
    TC.assertEqual(srcRes['creator'],  ['Mark Redar test creator'])
    TC.assertEqual(srcRes['contributor'],  ["Mark Redar test contrib",
                                            "Mark Redar test2 contrib",
                                            "Redar, Mark collector 1",
                                            "Redar, Mark collector 2.",])
    TC.assertNotIn('relation', srcRes)
    TC.assertNotIn('identifier', srcRes)
    TC.assertEqual(srcRes['format'],
            ["1 2.25 inch black and white negative",
             "black and white photograph"])
    TC.assertEqual(srcRes['genre'],
            ["Data tables",
             "Point cloud"])
    TC.assertEqual(srcRes['language'],  [{'iso639':'zxx',
                                          'name': 'No linguistic content', }])
    TC.assertEqual(srcRes['rights'][0],  "Under copyright")
    TC.assertEqual(srcRes['rights'][1][:21], "Constraint(s) on Use:")
    TC.assertEqual(srcRes['rights'][2][:27], "Use: This work is available")
    TC.assertEqual(srcRes['type'], 'image')
    TC.assertEqual(obj['isShownAt'],
            'https://library.ucsd.edu/dc/object/bb0922726p')
    TC.assertEqual(obj['isShownBy'],
            'https://library.ucsd.edu/dc/object/bb0922726p/_2.jpg')
    TC.assertEqual(srcRes['stateLocatedIn'][0]['name'], 'California')
    TC.assertEqual(srcRes['spatial'], [{'name': "Camp Matthews, San Diego"},
        {"name": "Test spatial"}])
    TC.assertEqual(obj['originalRecord']['rightsHolder'], [
            "DeWitt Higgs",
            "Kathryn M. Ringrose"
      ])
    print "SUBJ:{}".format(srcRes['subject'])
    TC.assertEqual(srcRes['subject'], 
        [
          {u'name': u'University of California, San Diego--Buildings, structures, etc'},
{u'name': u'Camp Matthews (Calif.)--Buildings, structures, etc'},
{u'name': u'University of California, San Diego--History'},
{u'name': u'La Jolla (San Diego, Calif.)--Photographs'},
{u'name': u'Camp Matthews (Calif.)--Photographs'},
{u'name': u'Camp Matthews (Calif.)--History'},
{u'name': u'test topic 1'},
{u'name': u'test topic 2'},
{u'name': u'Rappaport, Ann'},
{u'name': u'San Diego Supercomputer Center.'},
{u'name': u'University of California, San Diego. Center for Astrophysics and Space Sciences'},
{u'name': u'University of Colorado (System). Dept. of Astrophysics and Planetary Sciences. Center for Astrophysics and Space Astronomy'},
{u'name': u'Lawrence Livermore Laboratory'},
{u'name': u'University of California, San Diego--Buildings, structures, etc'},
{u'name': u'Camp Matthews (Calif.)--Buildings, structures, etc'},
{u'name': u'University of California, San Diego--History'},
{u'name': u'La Jolla (San Diego, Calif.)--Photographs'},
{u'name': u'Camp Matthews (Calif.)--Photographs'},
{u'name': u'Camp Matthews (Calif.)--History'}]
    )

def test_missing_language():
    fixture = path.join(DIR_FIXTURES,
              'ucsd-blacklight-missions-alta-california-obj-jsonfied.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertEqual(obj['isShownAt'],
            'https://library.ucsd.edu/dc/object/bb0308012n')
    TC.assertEqual(obj['isShownBy'],
            'https://library.ucsd.edu/dc/object/bb0308012n/_2.jpg')
    TC.assertNotIn('language', obj['sourceResource'])
    TC.assertEqual(obj['sourceResource']['type'], 'image')
    TC.assertEqual(obj['sourceResource']['rights'][0], 'Public Domain')
    TC.assertEqual(obj['sourceResource']['creator'],
                   [ "Jackson, William Henry, 1843-1942", ])

def test_missing_files_tesim():
    fixture = path.join(DIR_FIXTURES,
              'ucsd-blacklight-missions-alta-california-obj-jsonfied-files_tesim-removed.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    # was failing and deleting sourceResource
    TC.assertIn('sourceResource', obj)
