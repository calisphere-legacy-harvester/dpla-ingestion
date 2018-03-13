# -*- encoding: utf-8 -*-
import os.path as path
from unittest import TestCase
from nose.plugins.attrib import attr
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=up_oai_dc"
    return H.request(url, "POST", body=body)


def test_up_oai_dc_mapping():
    fixture = path.join(DIR_FIXTURES, 'up-oai.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('id', INPUT)
        resp, content = _get_server_response(INPUT)
    TC.assertEqual(resp.status, 200)
    obj = json.loads(content)
    TC.assertIn('sourceResource', obj)
    TC.assertIn('originalRecord', obj)
    srcRes = obj['sourceResource']
    TC.assertEqual(obj['isShownAt'],
                   "https://scholarlycommons.pacific.edu/pacific-review/6")
    TC.assertEqual(
        obj['isShownBy'],
        "http://scholarlycommons.pacific.edu/pacific-review/1005/preview.jpg")
    TC.assertEqual(srcRes['identifier'], [
        "https://scholarlycommons.pacific.edu/pacific-review/6",
        "http://scholarlycommons.pacific.edu/cgi/viewcontent.cgi?article=1005&amp;context=pacific-review"
    ])
    TC.assertEqual(srcRes['description'], [
        "Topics Include: Japanese, Japan, school, education, food, California, bank, family",
        "The Delia Locke Diaries are part of the Locke-Hammond Family Papers. In addition to the diaries, these papers include a broad range of materials on the family and Lockeford, California, the town they founded in the 1850s. Delia (Hammond) Locke was the matriarch of the family. Born in 1832, she married Dr. Dean Jewett Locke and moved to California in 1855. That same year Delia began keeping a daily diary. Her thumbnail diaries from 1855 to 1918 have been digitized to create this online collection. The diaries provide a remarkable documentation of life in rural northern California in the 19th century. The daily happenings of Delia's life and the Lockeford community are recorded, including the activities of church and temperance organizations as well as the Mokelumne River Ladies' Sewing Circle. Nearly every entry begins with temperature recordings taken at sunrise. To see additional years of the Delia Locke Diaries, click here to return to the homepage: http://scholarlycommons.pacific.edu/dld/"
    ])

# Copyright © 2016, Regents of the University of California
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
