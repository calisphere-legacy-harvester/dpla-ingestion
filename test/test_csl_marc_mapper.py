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
    url = server() + "dpla_mapper?mapper_type=csl_marc"
    return H.request(
        url,
        "POST",
        body=body, )


def test_csl_marc_mapper():
    fixture = path.join(DIR_FIXTURES, 'csl-marc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('001', INPUT)
        TC.assertIn('856', INPUT)
    resp, content = _get_server_response(INPUT)
    assert str(resp.status).startswith("2"), str(resp) + "\n" + content

    doc = json.loads(content)

    TC.assertEqual(
        doc['isShownAt'],
        'http://catalog.library.ca.gov/F/?func=find-b&request=001409080&find_code=SYS'
    )

    TC.assertEqual(
        doc['isShownBy'],
        'http://catalog.library.ca.gov/exlibris/aleph/u21_1/csl_objects/csl50/calif/view/26/1992-4833_000094379.jpg'
    )
