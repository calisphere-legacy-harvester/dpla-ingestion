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
                      }
                    ]
           }

_MAPPER = MARCMapper(_FIELDS,
                datafield_tag='fields',
                controlfield_tag='fields',
                pymarc=True
                )

TC = TestCase('__init__')

def test_map_is_shown_at():
    _MAPPER.map_datafield_tags()
    print(_MAPPER.mapped_data)
    TC.assertEqual(_MAPPER.mapped_data['isShownAt'],
                       "http://jpg1.lapl.org/sola1/00000001.jpg")
            
