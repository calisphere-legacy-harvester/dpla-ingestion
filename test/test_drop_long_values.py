from amara.thirdparty import json
from unittest import TestCase
from server_support import server, H

TC = TestCase('__init__')


def test_drop_long_values():
    """Correctly transform a date value that cannot be parsed"""
    INPUT = {
        "sourceResource": {
            "description": [
                "could be 1928ish?",
                "this is a long string will blow up flake 8, should drop this",
                "short"
            ]
        }
    }
    EXPECTED = {
        "sourceResource": {
            "description": ["could be 1928ish?", "short"]
        }
    }

    url = server() + "drop-long-values?field=description&max_length=20"

    resp, content = H.request(url, "POST", body=json.dumps(INPUT))

    TC.assertEqual(resp.status, 200)
    TC.assertEqual(json.loads(content), EXPECTED)
