import os.path as path
from unittest import TestCase
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')

def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=contentdm_oai_dc"
    return H.request(url, "POST", body=body)

def test_contentdm_oai_dc_mapping():
    # at this point, the ucsd feed should be "jsonfied"
    # need to map from the jsonfied obj to sourceResource
    fixture = path.join(DIR_FIXTURES,
            'contentdm_oai.json')
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
    TC.assertEqual(srcRes['subject'], [
        {u'name': u'Business'},
        {u'name': u'Black, J. D. (John David), 1893-1960'},
        {u'name': u'Coffin, H. R.'},
        {u'name': u'Water rights--California--Owens Valley'},
        {u'name': u'Water rights--California--Los Angeles'},
        {u'name': u'Metabolic Studio'},
        {u'name': u'Los Angeles Aqueduct'},
        {u'name': u'LA Aqueduct'},
        {u'name': u'Acquaduct'}])

    TC.assertEqual(srcRes['spatial'], [u'Los Angeles (Calif.)',
                                       u'Big Pine (Calif.)'])
    TC.assertEqual(srcRes['relation'], [
                            u'J. D. Black Papers',
                            u'CSLA-15',
                            u'Series 1.; Box No. 8; Folder No. 4'])
    TC.assertEqual(srcRes['description'], [
      "Letter from J. D. Black in Big Pine to H. R. Coffin", 
      "J. D. Black (1893-1960), also known as Jack"])
    TC.assertEqual(srcRes['type'], [ "Letters", "Text"])
    TC.assertEqual(srcRes['language'], ['eng'])
    TC.assertEqual(srcRes['rights'], [
        u'http://library.lmu.edu/generalinformation/departments/digitallibraryprogram/copyrightandreproductionpolicy/'])
    TC.assertEqual(srcRes['format'], ["2 pages", "image/tiff"])
    TC.assertEqual(srcRes['identifier'], [ 
      "sc_jdbp001110001",
      "sc_jdbp00111",
      "http://digitalcollections.lmu.edu/cdm/ref/collection/johndblack/id/262"
    ])
    TC.assertEqual(obj['isShownAt'], 
      "http://digitalcollections.lmu.edu/cdm/ref/collection/johndblack/id/262")
    TC.assertEqual(obj['isShownBy'], 
      "http://digitalcollections.lmu.edu/utils/getthumbnail/collection/johndblack/id/262")
