import sys
from unittest import TestCase
from dplaingestion.mappers.marc_mapper import MARCMapper


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
            
def test_map_creator():
    TC.assertEqual(_MAPPER.mapped_data['sourceResource']['creator'],
                        ['Schultheis, Herman.'])
