# -*- coding: utf-8 -*-
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=yosemite_oai_dc"
    return H.request(url, "POST", body=body)


def test_black_gold_mapping():
    fixture = path.join(DIR_FIXTURES, 'yosemite-oai.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    TC.assertEqual(
        obj['isShownAt'],
        "https://npgallery.nps.gov/AssetDetail/0657c92b4ad6449eb3b0fca3e10be5f6"
    )
    TC.assertEqual(
        obj['isShownBy'],
        "https://npgallery.nps.gov/GetAsset/0657c92b4ad6449eb3b0fca3e10be5f6/proxy/hires/"
    )
