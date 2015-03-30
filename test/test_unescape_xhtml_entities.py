# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json
from dplaingestion.akamod.unescape_xhtml_entities import unescape_xhtml_string

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + 'unescape-xhtml-entities?field=sourceResource'
    return H.request(url, "POST", body=body,
            )

def test_unescape_xhmtl_entities():
    '''Test basic unescaping of strings'''
    x = 'NO ENTITIES'
    y = unescape_xhtml_string(x)
    TC.assertEqual(x, y)
    x = '&amp;, &reg;, &lt;, &gt;, &cent;, &pound;, &yen;, &euro;, &sect;, &copy; &nbsp;'
    y = unescape_xhtml_string(x)
    expected = u'&, \xae, <, >, \xa2, \xa3, \xa5, \u20ac, \xa7, \xa9 \xa0'
    TC.assertEqual(expected, y)

def test_unescape_xhtml_entities():
    '''Test unescaping of entities in an object'''
    testData = {'sourceResource': {
            'subject': [ {'name': 'Parks &amp; Rec'},
                         {'name': 'Dogs &amp; Cats'} ],
            'title': ['Ren &amp; Stimpy',
                      '0 &lt; 1',
                      7],
            'creator': '&lt;Hedlok&gt;',
            }}
    resp, content = _get_server_response(json.dumps(testData)) 
    assert resp.status == 200
    obj = json.loads(content)
    print "OBJ:{}".format(obj)
    TC.assertEqual(obj['sourceResource']['subject'][0], {'name':'Parks & Rec'})
    TC.assertEqual(obj['sourceResource']['subject'][1], {'name':'Dogs & Cats'})
    TC.assertEqual(obj['sourceResource']['title'][0], 'Ren & Stimpy')
    TC.assertEqual(obj['sourceResource']['title'][1], '0 < 1')
    TC.assertEqual(obj['sourceResource']['title'][2], 7)
    TC.assertEqual(obj['sourceResource']['creator'], '<Hedlok>')
