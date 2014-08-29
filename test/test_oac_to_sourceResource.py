from server_support import server, H
from amara.thirdparty import json


def _get_server_response(body):
    url = server() + "oac-to-sourceResource"
    return H.request(url, "POST", body=body)

def test_oac_isShownBy():
    '''Test that the isShownBy is correctly grabbed from 
    OAC original records
    '''
    INPUT = {
        "_id": "yoshikawa-family-collection--http://ark.cdlib.org/ark:/13030/tf8779p3bw",
        "id": "bc46e3740d4ac92658be203231ffa87e",
        "originalRecord": {}

    }
    EXPECTED = {
          "Y": 105,
          "X": 125,
          "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/thumbnail"
    }

    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert 'isShownBy' not in json.loads(content)
    INPUT['originalRecord']['thumbnail'] = {
                "Y": 105,
                "X": 125,
                "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/thumbnail"
    }
    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert EXPECTED == json.loads(content)["isShownBy"]
    INPUT['originalRecord']['reference-image'] = [{
                    "Y": 633,
                    "X": 750,
                    "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/med-res"
                    }
                ]
    EXPECTED['X'] = 750
    EXPECTED['Y'] = 633
    EXPECTED['src'] = "http://content.cdlib.org/ark:/13030/tf8779p3bw/med-res"
    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert EXPECTED == json.loads(content)["isShownBy"]
    INPUT['originalRecord']['reference-image'].append({
                    "Y": 1262,
                    "X": 1500,
                    "src": "http://content.cdlib.org/ark:/13030/tf8779p3bw/hi-res"
                    }
                )
    EXPECTED['X'] = 1500
    EXPECTED['Y'] = 1262
    EXPECTED['src'] = "http://content.cdlib.org/ark:/13030/tf8779p3bw/hi-res"
    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert EXPECTED == json.loads(content)["isShownBy"]


if __name__=="__main__":
    raise SystemExit("Use nosetests")
