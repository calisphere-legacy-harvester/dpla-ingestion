import sys
from unittest import TestCase
from server_support import server, print_error_log
from amara.thirdparty import httplib2
from amara.thirdparty import json

TC = TestCase('__init__')

CT_JSON = {"Content-Type": "application/json"}

H = httplib2.Http()

def _get_server_response_raw_query(url, body):
    return H.request(url, "POST", body=body, headers=CT_JSON)

def _get_server_response(body, prop=None, old=None, new=None):
    url = server() + "replace_substring"
    if prop:
        url = "%s?prop=%s" % (url, prop)
    if old:
        url = "%s&old=%s" % (url, old)
    if new:
        url = "%s&new=%s" % (url, new)
    return _get_server_response_raw_query(url, body)

def test_replace_string1():
    """Should do nothing since old/new is not set"""
    prop = "isShownAt"

    INPUT = {
        "isShownAt": "http://74.126.224.122/luna/servlet/detail/RUMSEY~8~1~107~10001"
    }

    resp,content = _get_server_response(json.dumps(INPUT), prop=prop)
    assert resp.status == 200
    assert json.loads(content) == INPUT

def test_replace_string2():
    """Should do nothing since old not in prop"""
    prop = "isShownAt"
    old = "bananas"
    new = "apples"

    INPUT = {
        "isShownAt": "http://74.126.224.122/luna/servlet/detail/RUMSEY~8~1~107~10001"
    }

    resp,content = _get_server_response(json.dumps(INPUT), prop=prop, old=old,
                                        new=new)
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), INPUT)

def test_replace_string3():
    """Should replace old with new"""
    prop = "isShownAt"
    old = "74%2E126%2E224%2E122"
    new = "www%2Edavidrumsey%2Ecom"

    INPUT = {
        "isShownAt": "http://74.126.224.122/luna/servlet/detail/RUMSEY~8~1~107~10001"
    }
    EXPECTED = {
        "isShownAt": "http://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~107~10001"
    }

    resp,content = _get_server_response(json.dumps(INPUT), prop=prop, old=old,
                                        new=new)
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), EXPECTED)

def test_replace_basestring_blank():
    INPUT = {
            'sourceResource': {'title': 'Bicyclist [graphic]'}
    }
    EXPECTED = {
            'sourceResource': {'title': 'Bicyclist'}
    }
    url = server() + "replace_substring"
    url = "{0}?prop=sourceResource%2Ftitle&old=[graphic]&new=".format(url)
    resp, content = _get_server_response_raw_query(url, json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), EXPECTED)

def test_replace_list():
    '''Test replacing substrings when field is a list
    '''
    INPUT = {
            'sourceResource': {'title': ['Bicyclist [graphic]',
                'Victorian [graphic] 1880s', 'no replace']}
    }
    EXPECTED = {
            'sourceResource': {'title': ['Bicyclist',
                'Victorian  1880s', 'no replace']}
    }
    url = server() + "replace_substring"
    url = "{0}?prop=sourceResource%2Ftitle&old=[graphic]&new=".format(url)
    resp, content = _get_server_response_raw_query(url, json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), EXPECTED)
    
def test_replace_list_subdicts():
    '''Test replacing substrings when field is a list of with dicts
    '''
    INPUT = {
            'sourceResource': {'subject': [{'name':'Bicyclist [graphic]'},
                {'name':'Victorian [graphic] 1880s'}, 
                {'name':'no replace'}]}
    }
    EXPECTED = {
            'sourceResource': {'subject': [{'name':'Bicyclist'},
                {'name':'Victorian  1880s'}, 
                {'name':'no replace'}]}
    }
    url = server() + "replace_substring"
    url = "{0}?prop=sourceResource%2Fsubject&old=[graphic]&new=".format(url)
    resp, content = _get_server_response_raw_query(url, json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), EXPECTED)

def test_replace_regex():
    '''Test replacing a regex'''
    INPUT = {
            'sourceResource': {'subject': [{'name':'Bicyclist $z'},
                {'name':'Victorian $x 1880s'}, 
                {'name':'no replace'}]}
    }
    EXPECTED = {
            'sourceResource': {'subject': [{'name':'Bicyclist --'},
                {'name':'Victorian -- 1880s'}, 
                {'name':'no replace'}]}
    }
    url = server() + "replace_regex"
    url = "{0}?prop=sourceResource%2Fsubject&regex=\$\S&new=--".format(url)
    resp, content = _get_server_response_raw_query(url, json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), EXPECTED)

if __name__ == "__main__":
    raise SystemExit("Use nosetest")
