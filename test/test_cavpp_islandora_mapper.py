import os.path as path
from unittest import TestCase
from nose.plugins.attrib import attr
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=cavpp_islandora"
    return H.request(url, "POST", body=body)

@attr(uses_network='yes')
def test_cavpp_overrides():
    fixture = path.join(DIR_FIXTURES,
            'cavpp_islandora.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(obj['isShownAt'], 'http://archive.org/details/corob_000252')
    TC.assertEqual(obj['isShownBy'][0],
      "https://californiarevealed.org/islandora/object/cavpp%3A24434/datastream/TN/view/Polk%27s%20Oakland%20%28California%29%20city%20directory%2C%20including%20Alameda%2C%20Berkeley%2C%20Emeryville%20and%20Piedmont.jpg")
    srcRes = obj['sourceResource']
    TC.assertNotIn('http://cdm15972.contentdm.oclc.org/bogus',
            srcRes['identifier'])
    TC.assertEqual(srcRes['identifier'],
                            [u"http://archive.org/details/corob_000252",
                            u"2016-050-0029"])
    TC.assertEqual(srcRes['provenance'],
                            [u"Butte County Library",
                            u"The California Revealed Project is supported by the U.S. Institute of Museum and Library Services under the provisions of the Library Services and Technology Act, administered in California by the State Librarian."])
    TC.assertEqual(srcRes['type'],[u'Sound'])
