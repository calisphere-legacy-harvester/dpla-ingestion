import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body, prop=None):
    url = server() + "jsonfy-prop" # with no prop, does root of data
    if prop:
        url = url + '?prop=' + str(prop)
    return H.request(url, "POST", body=body)


def get_fixture(fixture):
    fixture = path.join(DIR_FIXTURES, fixture)
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
    return INPUT

def test_jsonfy_data():

    INPUT = get_fixture('ucsd-blacklight-missions-alta-california-obj.json')
    resp, content = _get_server_response(INPUT)
    assert resp.status == 200
    obj = json.loads(content)
    TC.assertEqual(obj['relationship_json_tesim'][0]['Creator'],
            [u'Jackson, William Henry, 1843-1942'])
    TC.assertEqual(obj['relationship_json_tesim'][0]['Collector'],
            [u'Hill, Dorothy V.', u'Hill, Kenneth E.'])
    TC.assertEqual(len(obj['otherNote_json_tesim']), 2)
    TC.assertEqual(obj['otherNote_json_tesim'][1]['value'], '6302')

    TC.assertEqual(obj['date_json_tesim'][0]['endDate'], '1890')
    TC.assertEqual(obj['title_json_tesim'][0]['name'], 'Mission San Carlos')


    #DIFFERENT DATA
    INPUT = get_fixture('ucsd-blacklight-camp-matthews-obj.json')
    resp, content = _get_server_response(INPUT)
    assert resp.status == 200
    obj = json.loads(content)
    TC.assertEqual(obj['language_json_tesim'][0]['code'], 'zxx')
    TC.assertEqual(obj['preferredCitationNote_json_tesim'][0]['value'][:43],
            u'"Camp Matthews, Rifle range, shed, storage"')

def test_jsonfy_originalRecord():
    data = get_fixture('ucsd-blacklight-missions-alta-california-obj.json')
    prop = 'originalRecord'
    obj = {prop:json.loads(data)} 
    resp, content = _get_server_response(json.dumps(obj), prop=prop)
    assert resp.status == 200
    obj = json.loads(content)
    TC.assertEqual(obj[prop]['title_json_tesim'][0]['name'],
            'Mission San Carlos')
    
