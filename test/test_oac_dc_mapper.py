import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=oac_dc"
    return H.request(url, "POST", body=body)

def _check_isShownBy(INPUT, EXPECTED):
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content).get('isShownBy', None), EXPECTED)

def test_oac_isShownAt():
    '''Verify that the isShownAt set by select-oac-id is still in data.
    '''
    INPUT = {
            'identifier':[{'attrib':{}, 'text':'http://ark.cdlib.org/ark:/bogus'},
                {'attrib':{}, 'text':'localid'}]
    }
    url = server() + "select-oac-id"
    resp, content = H.request(url, "POST", body=json.dumps(INPUT),
            headers={'Source': 'an-oac-collection-slug'})
    resp, content = _get_server_response(content)
    content = json.loads(content)
    TC.assertEqual(content['isShownAt'], 'http://ark.cdlib.org/ark:/bogus')

def test_map_oac_dc_meta():
    '''Test that the DC meta values from OAC are pulled to sourceResource'''
    fixture = path.join(DIR_FIXTURES, 'oac-xml.json')
    with open(fixture) as f:
        INPUT = f.read()
    resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    content_obj = json.loads(content)
    srcRes = content_obj['sourceResource']
    TC.assertEqual(len(srcRes['format']), 1) # suppresses q="x"
    TC.assertEqual(srcRes['format'], ['painting'])
    TC.assertEqual(len(srcRes['relation']), 7)
    TC.assertEqual(len(srcRes['subject']), 2) # suppresses q="series"
    TC.assertEqual(srcRes['subject'],  [
        {'name': u'Japanese Americans'},
        {'name': u'Uchida'}])
    TC.assertEqual(srcRes['date'], ["7/21/42", "7/21/72"])

def test_oac_isShownBy():
    '''Test that the isShownBy is correctly grabbed from 
    OAC original records
    '''
    INPUT = {
        "_id": "yoshikawa-family-collection--http://ark.cdlib.org/ark:/13030/tf8779p3bw",
        "id": "bc46e3740d4ac92658be203231ffa87e",
        "originalRecord": {'identifier':['http://ark.cdlib.org/ark:/bogus',
            'localid']}
    }
    EXPECTED = None
    _check_isShownBy(INPUT, EXPECTED)
    INPUT['originalRecord']['thumbnail'] = {
                "Y": 105,
                "X": 125,
                "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/thumbnail"
    }
    EXPECTED = "http://content.cdlib.org/ark:/13030/tf8779p3bw/thumbnail"
    _check_isShownBy(INPUT, EXPECTED)
    INPUT['originalRecord']['reference-image'] = [{
                    "Y": 633,
                    "X": 750,
                    "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/med-res"
                    }
                ]
    EXPECTED = "http://content.cdlib.org/ark:/13030/tf8779p3bw/med-res"
    _check_isShownBy(INPUT, EXPECTED)
    INPUT['originalRecord']['reference-image'].append({
                    "Y": 1262,
                    "X": 1500,
                    "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/hi-res"
                    }
                )
    EXPECTED = "http://content.cdlib.org/ark:/13030/tf8779p3bw/hi-res"
    _check_isShownBy(INPUT, EXPECTED)
    INPUT['originalRecord']['reference-image'].append({
                    "Y": 2000,
                    "X": 3000,
                    "src": "ark:/13030/tf8779p3bw/hi-res-2"
                    }
                )
    EXPECTED = "http://content.cdlib.org/ark:/13030/tf8779p3bw/hi-res-2"
    _check_isShownBy(INPUT, EXPECTED)

def test_map_data_provider():
    '''Test that the "provider" is the collection'''
    INPUT = {
        #"_id": "yoshikawa-family-collection--http://ark.cdlib.org/ark:/13030/tf8779p3bw",
        #"id": "bc46e3740d4ac92658be203231ffa87e",
#        "originalRecord": {'identifier':['http://ark.cdlib.org/ark:/bogus', 'localid'],
        "originalRecord": {
            'collection': [
                   {
                       "description": "",
                       "title": "Historical Treasures of San Bernardino",
                       "ingestType": "collection",
                       "@id": "https://registry.cdlib.org/api/v1/collection/10046/",
                       "id": "10046",
                       "name": "Historical Treasures of San Bernardino"
                   }
               ]
            }
    }
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['dataProvider'],
            INPUT['originalRecord']['collection'])

def test_map_state_located_in():
    '''Should always return California'''
    INPUT = {'originalRecord':{}}
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['stateLocatedIn'][0]['name'], 'California')

def test_map_spatial():
    INPUT = {'originalRecord':{'coverage':[{'text':'Oakland', 'attrib':''}]}}
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['spatial'], ['Oakland'])
    INPUT = {'originalRecord':{'coverage':[{'text':'Oakland', 'attrib':''},
        {'text':'ark:/12345/bogusark', 'attrib':''},
        {'text':'Uptown', 'attrib':''}]}}
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['spatial'], ['Oakland', 'Uptown'])
    INPUT = {'originalRecord':{'coverage':[
        {'text':'Oakland', 'attrib':''},
        {'text':'ark:/12345/bogusark', 'attrib':''},
        {'text':'Uptown', 'attrib':''}]}}
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['spatial'], ['Oakland', 'Uptown'])


if __name__=="__main__":
    raise SystemExit("Use nosetests")

