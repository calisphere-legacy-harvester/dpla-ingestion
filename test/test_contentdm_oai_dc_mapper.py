import os.path as path
from unittest import TestCase
from nose.plugins.attrib import attr
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=contentdm_oai_dc"
    return H.request(url, "POST", body=body)


@attr(uses_network='yes')
def test_contentdm_oai_dc_mapping():
    # at this point, the ucsd feed should be "jsonfied"
    # need to map from the jsonfied obj to sourceResource
    fixture = path.join(DIR_FIXTURES, 'contentdm_oai_dc_only.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(srcRes['title'],
                   ["Letter from J. D. Black to H. R. Coffin"])
    TC.assertEqual(srcRes['date'], [u'1924-07-24', u'1920-1929'])
    TC.assertEqual(srcRes['contributor'],
                   [u'Support provided by the Metabolic Studio.'])
    TC.assertEqual(srcRes['creator'], [u'Coffin, H. R.'])
    TC.assertEqual(srcRes['subject'], [{
        u'name': u'Business'
    }, {
        u'name': u'Black, J. D. (John David), 1893-1960'
    }, {
        u'name': u'Coffin, H. R.'
    }, {
        u'name': u'Water rights--California--Owens Valley'
    }, {
        u'name': u'Water rights--California--Los Angeles'
    }, {
        u'name': u'Metabolic Studio'
    }, {
        u'name': u'Los Angeles Aqueduct'
    }, {
        u'name': u'LA Aqueduct'
    }, {
        u'name': u'Acquaduct'
    }])

    TC.assertEqual(srcRes['spatial'],
                   [u'Los Angeles (Calif.)', u'Big Pine (Calif.)'])
    TC.assertEqual(srcRes['relation'], [
        u'J. D. Black Papers', u'CSLA-15',
        u'Series 1.; Box No. 8; Folder No. 4'
    ])
    TC.assertEqual(srcRes['description'], [
        "Letter from J. D. Black in Big Pine to H. R. Coffin",
        "J. D. Black (1893-1960), also known as Jack"
    ])
    TC.assertEqual(srcRes['type'], ["Letters", "Text"])
    TC.assertEqual(srcRes['language'], ['eng'])
    TC.assertEqual(srcRes['rights'], [
        u'http://library.lmu.edu/generalinformation/departments/digitallibraryprogram/copyrightandreproductionpolicy/'
    ])
    TC.assertEqual(srcRes['format'], ["2 pages", "image/tiff"])
    TC.assertEqual(srcRes['identifier'], [
        'http://archive.org/details/cubanc_000177', "sc_jdbp001110001",
        "sc_jdbp00111",
        "http://digital-collections.csun.edu/cdm/ref/collection/GSAC/id/21",
        "http://cdm15972.contentdm.oclc.org/bogus"
    ])
    TC.assertEqual(
        obj['isShownAt'],
        "http://digital-collections.csun.edu/cdm/ref/collection/GSAC/id/21"
    )
    TC.assertEqual(
        obj['isShownBy'],
        "http://digital-collections.csun.edu/utils/getthumbnail/collection/GSAC/id/21"
    )


def test_suppress_sound_thumbs():
    '''For type "sound", remove the isShownBy value so no image will be
    harvested.
    '''
    fixture = path.join(DIR_FIXTURES, 'cavpp_contentdm_oai.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    TC.assertEqual(obj['sourceResource']['type'], ['Sound'])
    TC.assertNotIn('isShownBy', obj)


@attr(uses_network='yes')
def test_get_larger_image():
    '''For type "image", there is usually (always?) a larger image available.
    This should only be tested when network available, couldn't get httpretty
    to work in this context.
    '''
    fixture = path.join(DIR_FIXTURES, 'contentdm_oai_image_type.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    TC.assertEqual(obj['sourceResource']['type'], ['Still Image'])
    TC.assertEqual(
        obj['isShownBy'],
        "http://northbaydigital.sonoma.edu/utils/ajaxhelper?CISOROOT=maxwell&CISOPTR=12&action=2&DMHEIGHT=2000&DMWIDTH=2000&DMSCALE=100"
    )
