import sys
import os.path as path
from unittest import TestCase
from dplaingestion.mappers.marc_mapper import MARCMapper
from server_support import server, H
from amara.thirdparty import json

DIR_FIXTURES = path.join(path.abspath(path.split(__file__)[0]), 'fixtures')

#http://stackoverflow.com/questions/18084476/is-there-a-way-to-use-python-unit-test-assertions-outside-of-a-testcase
TC = TestCase('__init__')


_FIELDS = {"fields": [{ "856": {
                        "subfields": [
                            {
                                "u": "http://jpg1.lapl.org/sola1/00000001.jpg"
                            }
                        ],
                        "ind1": "4",
                        "ind2": " "
                        },
                      },
                      {
                        "100": {
                          "ind2": " ",
                          "subfields": [
                            {
                              "a": "Schultheis, Herman."
                            }
                          ],
                          "ind1": "1"
                        }
                      },
                    ]
           }

_MAPPER = MARCMapper(_FIELDS,
                datafield_tag='fields',
                controlfield_tag='fields',
                pymarc=True
                )

TC = TestCase('__init__')

_MAPPER.map_datafield_tags()

def test_map_is_shown_at():
    TC.assertEqual(_MAPPER.mapped_data['isShownAt'],
                       "http://jpg1.lapl.org/sola1/00000001.jpg")
    TC.assertEqual(_MAPPER.mapped_data['isShownBy'],
                       "http://jpg1.lapl.org/sola1/00000001.jpg")
            
def test_map_creator():
    TC.assertEqual(_MAPPER.mapped_data['sourceResource']['creator'],
                        ['Schultheis, Herman.'])


def _get_server_response(body):
    url = server() + "dpla_mapper?mapper_type=marc"
    return H.request(url, "POST", body=body,
            )

def test_full_marc_doc():
    fixture = path.join(DIR_FIXTURES, 'ucsb-aleph-marc.json')
    with open(fixture) as f:
        INPUT = f.read()
        TC.assertIn('530', INPUT)
        resp, content = _get_server_response(INPUT)
    assert str(resp.status).startswith("2"), str(resp) + "\n" + content

    doc = json.loads(content)
    TC.assertIn(u'sourceResource', doc)
    TC.assertIn(u'title', doc[u'sourceResource'])
    TC.assertEqual(doc['sourceResource']['title'], ["Sailor's hornpipe medley [sound recording]."]) 
    #NOTE: regular marc mapper grabs first 856$u field
    TC.assertEqual(doc['isShownAt'], "http://digilib.syr.edu/u?/cylinder,364")
    TC.assertEqual(doc['isShownBy'], "http://digilib.syr.edu/u?/cylinder,364")
    TC.assertEqual(doc['sourceResource']['contributor'], [u"D'Almaine, Charles, 1871-1943. itr"])
    TC.assertEqual(doc['sourceResource']['date'], {u'begin': u'1912', u'end': u'1912', u'displayDate': u'[1912]'})
    TC.assertEqual(doc['sourceResource']['description'], 
                [u'Edison Amberol: 960.',
                 u'Year of release from "The Edison Phonograph Monthly," v.10 (1912).',
                 u'Introduces "Jenny Linn," "Lockers," "Acrobat," "Champion" and "Autograph."',
                 u"Charles D'Almaine.",
                 u'Violin solo with orchestra accompaniment.',
                 u'Todd collection.',
                 u'Also available online via the Internet.'])
    TC.assertEqual(doc['sourceResource']['extent'],
            [u'1 cylinder (ca. 4 min.) : 2 1/4 x 4 in.'])
    TC.assertEqual(doc['sourceResource']['format'],
            [u'Electronic resource'])
    #TODO: this is broken return spaces    TC.assertEqual(doc['sourceResource']['language'], '')
    TC.assertEqual(doc['sourceResource']['publisher'],
            [u'Orange, N.J. : Edison Amberol,'])
    print "SUBJECT RETURNED:{}".format(doc['sourceResource']['subject'])
    TC.assertEqual(doc['sourceResource']['subject'],
            [{'name':u'Popular instrumental music--1911-1920.'},
             {'name': u'Violin with orchestra.'},
             {'name': u'Fiddle tunes.'}])
    TC.assertEqual(doc['sourceResource']['type'],
            'Sound')
