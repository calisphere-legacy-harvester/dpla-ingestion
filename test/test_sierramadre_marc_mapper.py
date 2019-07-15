# coding: utf-8
import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

# http://stackoverflow.com/questions/18084476/is-there-a-way
# -to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=sierramadre_marc"
    return H.request(
        url,
        "POST",
        body=body, )


def test_sierra_marc_mapper():
    fixture = path.join(DIR_FIXTURES, 'sierramadre-marc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('001', INPUT)
        TC.assertIn('856', INPUT)
    resp, content = _get_server_response(INPUT)
    assert str(resp.status).startswith("2"), str(resp) + "\n" + content

    doc = json.loads(content)

    TC.assertEqual(
        doc['isShownAt'],
        'https://sierramadre.biblionix.com/catalog/biblio/240977414'
    )

    TC.assertEqual(
        doc['isShownBy'],
        'http://cityofsierramadre.hosted.civiclive.com/UserFiles/Servers/Server_212309/Image/City%20Hall/Departments/Library/Historical%20Images/1999.70.1.jpg'
    )
