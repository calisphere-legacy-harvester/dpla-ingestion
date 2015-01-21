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
    TC.assertEqual(json.loads(content)['isShownBy'], EXPECTED)

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
    TC.assertEqual(content['sourceResource']['stateLocatedIn'], 'California')

def test_map_spatial():
    INPUT = {'originalRecord':{'coverage':'Oakland'}}
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['spatial'], ['Oakland'])


if __name__=="__main__":
    raise SystemExit("Use nosetests")

