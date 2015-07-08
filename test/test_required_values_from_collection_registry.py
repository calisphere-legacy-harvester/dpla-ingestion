# coding: utf-8
from copy import deepcopy
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body, field, mode):
    url = server() + "required-values-from-collection-registry?field={}&mode={}".format(field, mode)
    return H.request(url, "POST", body=body,
            )

INPUT = { 'originalRecord': { "collection": [
               {
                   "description": "",
                   "title": "Historic Postcards Collection",
                   "ingestType": "collection",
                   "@id": "https://registry.cdlib.org//api/v1/collection/10028/",
                   "id": "10028",
                   "name": "Historic Postcards Collection",
                   "dcmi_type": "I",
                   "rights_statement": "rights-stmt",
                   "rights_status": "PD"
               }
           ]},
           'sourceResource': {}
           
       }

def test_noFilling():
    '''Test that the data values do not get replaced if existing'''
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'rights':'this has rights',
            'type': 'this has type',
            }
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'], 'this has rights')
    TC.assertEqual(content['sourceResource']['type'], 'this has type')

def test_no_dcmi_type():
    this_input = deepcopy(INPUT)
    this_input['originalRecord']['collection'][0]['dcmi_type'] = ''
    this_input['sourceResource'] = {}
    resp, content = _get_server_response(json.dumps(this_input), field='type',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertNotIn('type', content['sourceResource'])

def test_fill_dcmi_type():
    '''Is dcmi_type filled if no type in sourceResource'''
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'rights':'this has rights',
            }
    resp, content = _get_server_response(json.dumps(this_input), field='type',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'], 'this has rights')
    TC.assertEqual(content['sourceResource']['type'], 'Image')

def test_fill_rights():
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'type': 'this has type', }
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            [u'public domain', u'rights-stmt'])
    TC.assertEqual(content['sourceResource']['type'], 'this has type')

def test_fill_missing_rights():
    '''Test what happens if you need to fill rights but don't have any in collection
    '''
    this_input = dict(_id='testid',
        originalRecord={'collection':[{'rights_statement':'',
        'rights_status':'', 'dcmi_type':''}]},
        sourceResource={})
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='fill')
    # not sure if this is correct behavior
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            [u'Please contact the contributing institution for more information regarding the copyright status of this object.'])

def test_fill_rights_no_status():
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'type': 'this has type', }
    this_input['originalRecord']['collection'][0]['rights_status'] = 'XXXX'
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            u'rights-stmt')
    TC.assertEqual(content['sourceResource']['type'], 'this has type')

def test_fill_rights_no_stmt():
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'type': 'this has type', }
    this_input['originalRecord']['collection'][0]['rights_statement'] = ''
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            u'public domain')
    TC.assertEqual(content['sourceResource']['type'], 'this has type')

def test_append():
    '''Test the append mode, that the values are added to existing data'''
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'type': 'type0', 
            'rights': 'rights0'}
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='append')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            ['rights0', 'public domain', 'rights-stmt'])
    TC.assertEqual(content['sourceResource']['type'], 'type0')
    this_input['sourceResource'] = {'type': ['type0', 'type1'], 
            'rights': ['rights0', 'rights1']}
    resp, content = _get_server_response(json.dumps(this_input), field='type',
            mode='append')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            ['rights0', 'rights1'])
    TC.assertEqual(content['sourceResource']['type'],
            ['type0', 'type1', 'Image'])
            #['type0', 'Image'])

def test_overwrite():
    '''Test the overwrite mode. Values from collection registry overwrite the
    existing'''
    this_input = deepcopy(INPUT)
    this_input['sourceResource'] = {'type': 'type0', 
            'rights': 'rights0'}
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='overwrite')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'],
            ['public domain', 'rights-stmt'])
    TC.assertEqual(content['sourceResource']['type'], 'type0')
    resp, content = _get_server_response(json.dumps(this_input), field='type',
            mode='overwrite')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['rights'], 'rights0')
    TC.assertEqual(content['sourceResource']['type'], 'Image')
    this_input = dict(originalRecord={'collection':[
                {'rights_statement':'', 'rights_status':''}]})
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='overwrite')
    TC.assertEqual(resp.status, 500)
    this_input = dict(originalRecord={'collection':[
                {'rights_statement':'xxxx', 'rights_status':'I',
                    'dcmi_type':''}]})
    resp, content = _get_server_response(json.dumps(this_input), field='rights',
            mode='overwrite')
    TC.assertEqual(resp.status, 500)

def test_fill_title():
    this_input = deepcopy(INPUT)
    resp, content = _get_server_response(json.dumps(this_input), field='title',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['title'],
                    'Title unknown')
    this_input['sourceResource']['title'] = 'XX'
    resp, content = _get_server_response(json.dumps(this_input), field='title',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['title'],
                    'XX')
    this_input['sourceResource']['title'] = ''
    resp, content = _get_server_response(json.dumps(this_input), field='title',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['title'],
                    'Title unknown')
    this_input['sourceResource']['title'] = []
    resp, content = _get_server_response(json.dumps(this_input), field='title',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['title'],
                    'Title unknown')
    this_input['sourceResource']['title'] = {}
    resp, content = _get_server_response(json.dumps(this_input), field='title',
            mode='fill')
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['sourceResource']['title'],
                    'Title unknown')
