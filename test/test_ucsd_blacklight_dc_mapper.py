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
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'],
            ['Camp Matthews, Rifle range, shed, storage'])
    TC.assertEqual(srcRes['date'],  { "displayDate": "1964",
                                      "end": "1964-12-31",
                                      "begin": "1964-01-01",
                                      })
    TC.assertEqual(srcRes['description'],
            ["a test description (added for testing)"])
    TC.assertEqual(srcRes['creator'],  ['Mark Redar test creator'])
    TC.assertEqual(srcRes['contributor'],  ["Mark Redar test contrib",
                                            "Mark Redar test2 contrib",
                                            "Redar, Mark collector 1",
                                            "Redar, Mark collector 2.",])
    TC.assertEqual(srcRes['identifier'],  [ "039.tif",
                        "http://libraries.ucsd.edu/ark:/20775/bb0922726p",
                        "an3_r4025_39",
                        ])
    TC.assertEqual(srcRes['format'],
            ["1 2.25 inch black and white negative"])
    TC.assertEqual(srcRes['language'],  [{'iso639':'zxx',
                                          'name': 'No linguistic content', }])
    TC.assertEqual(srcRes['rights'][0],  "Under copyright")
    TC.assertEqual(srcRes['rights'][1][:21], "Constraint(s) on Use:")
    TC.assertEqual(srcRes['rights'][2][:27], "Use: This work is available")
    TC.assertEqual(srcRes['subject'], [
        {"name":"University of California, San Diego--Buildings, structures, etc"},
        {"name":"Camp Matthews (Calif.)--Buildings, structures, etc"},
        {"name":"University of California, San Diego--History"},
        {"name":"La Jolla (San Diego, Calif.)--Photographs"},
        {"name":"Camp Matthews (Calif.)--Photographs"},
        {"name":"Camp Matthews (Calif.)--History"}
        ])
    TC.assertEqual(srcRes['type'], 'image')
    TC.assertEqual(obj['isShownAt'],
            'https://library.ucsd.edu/dc/object/bb0922726p')
    TC.assertEqual(obj['isShownBy'],
            'https://library.ucsd.edu/dc/object/bb0922726p/_2.jpg')
    TC.assertEqual(srcRes['stateLocatedIn'][0]['name'], 'California')
    TC.assertEqual(srcRes['spatial'], [{'name': "Camp Matthews, San Diego"},
        {"name": "Test spatial"}])

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

