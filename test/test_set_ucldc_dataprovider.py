# coding: utf-8
from copy import deepcopy
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "set-ucldc-dataprovider"
    return H.request(url, "POST", body=body)

def test_set_repo_only():
    '''All data have a repo, some have campus'''
    INPUT = { 'originalRecord':
            { "collection": [
                {"repository":[ { "name": "Los Angeles Public Library",
                    "@id": "https://registry.cdlib.org/api/v1/repository/143/",
                    "campus": [ ],
                    }
                    ]
                }
              ]
            }
    }
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['dataProvider'], 'Los Angeles Public Library')

def test_set_has_campus():
    INPUT = { 'originalRecord':
            { "collection": [
                { "repository": [
                    { "@id": "https://registry.cdlib.org/api/v1/repository/4/",
                      "name": "Bancroft Library",
                      "campus": [{ "name": "UC Berkeley",
                      "@id": "https://registry.cdlib.org/api/v1/campus/1/",}]
                    }
                    ]
                }
              ]
            }
    }
    resp, content = _get_server_response(json.dumps(INPUT))
    TC.assertEqual(resp.status, 200)
    content = json.loads(content)
    TC.assertEqual(content['dataProvider'], 'UC Berkeley, Bancroft Library')

#TODO: handle multiple repos, campuses.... Luckily repo is only on one campus
