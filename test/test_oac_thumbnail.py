from server_support import server, H
from amara.thirdparty import json


def _get_server_response(body):
    url = server() + "oac-thumbnail"
    print("URL:"+url)
    return H.request(url, "POST", body=body)

def test_oac_thumb_url_generation():
    INPUT = {
        "_id": "zukas-hale-papers--http://ark.cdlib.org/ark:/13030/hb958006wx",
        "ingestDate": "2014-08-09T10:53:45.564254",
        "ingestionSequence": 2,
        "ingestType": "item",
        "dataProvider": "The Bancroft Library. University of California, Berkeley. Berkeley, Calif., 94720-6000; http://bancroft.berkeley.edu",
        "originalRecord": {
            "facet-oac-tab": "digital item",
            "iso-start-date": "1975:00:00",
            "relation-from": "http://www.oac.cdlib.org/findaid/ark:/13030/tf796nb2t9|Hale Zukas Papers, 1971-1998",
            "relation": [
                "http://www.oac.cdlib.org/findaid/ark:/13030/tf796nb2t9",
                "docs -- drilm",
                "http://bancroft.berkeley.edu/collections/drilm",
            ],
        "dateStamp": "2006-02-03",
        "identifier": [
            "http://ark.cdlib.org/ark:/13030/hb958006wx",
            "BANC MSS 99/150 c [Carton 1, Folder 12: D]"
        ]
        },
        "id": "9d25a4b21372f07fcfd00415dc7ab257"
    }
    BAD_INPUT = {
        "_id": "zukas-hale-papers--http://ark.cdlib.org/13030/hb958006wx",
        "ingestDate": "2014-08-09T10:53:45.564254",
        "ingestionSequence": 2,
        "ingestType": "item",
        "dataProvider": "The Bancroft Library. University of California, Berkeley. Berkeley, Calif., 94720-6000; http://bancroft.berkeley.edu",
        "originalRecord": {
            "facet-oac-tab": "digital item",
            "iso-start-date": "1975:00:00",
            "relation-from": "http://www.oac.cdlib.org/findaid/ark:/13030/tf796nb2t9|Hale Zukas Papers, 1971-1998",
            "relation": [
                "http://www.oac.cdlib.org/findaid/ark:/13030/tf796nb2t9",
                "docs -- drilm",
                "http://bancroft.berkeley.edu/collections/drilm",
            ],
        "dateStamp": "2006-02-03",
        "identifier": [
            "http://ark.cdlib.org/ark:/13030/hb958006wx",
            "BANC MSS 99/150 c [Carton 1, Folder 12: D]"
        ]
        },
        "id": "9d25a4b21372f07fcfd00415dc7ab257"
    }
    EXPECTED = "http://content.cdlib.org/ark:/13030/hb958006wx/thumbnail"

    resp, content = _get_server_response(json.dumps(BAD_INPUT))
    assert resp.status == 500
    print content
    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert EXPECTED == json.loads(content)["object"]

if __name__=="__main__":
    test_oac_thumb_url_generation()
    #raise SystemExit("Use nosetests")
