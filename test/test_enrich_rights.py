from server_support import server, H, print_error_log
from amara.thirdparty import json
from dict_differ import DictDiffer, assert_same_jsons, pinfo

def _get_server_response(body):
    url = server() + "enrich-rights"
    return H.request(url, "POST", body=body)

def test_rights_enrichment():
    INPUT = {
        "_id": "123",
        "sourceResource": {
            "rightsURI": "http://rightsstatements.org/vocab/NoC-CR/1.0/"
        }
    }
    EXPECTED = {
        "_id": "123",
        "sourceResource": {
            "rights": "Use of this Item is not restricted by copyright and/or related rights. As part of the acquisition or digitization of this Item, the organization that has made the Item available is contractually required to limit the use of this Item. Limitations may include, but are not limited to, privacy issues, cultural protections, digitization agreements or donor agreements. Please refer to the organization that has made the Item available for more information.",
            "rightsURI": "http://rightsstatements.org/vocab/NoC-CR/1.0/"
        }
    }
    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert_same_jsons(EXPECTED, json.loads(content))

def test_rights_stay_same():
    # Delete sourceResource.rightsURI if not valid RS/CC URI
    INPUT = {
        "_id": "123",
        "sourceResource": {
            "rightsURI": "Please contact the contributing institution"
        }
    }
    EXPECTED = {
        "_id": "123",
        "sourceResource": { }
    }
    resp, content = _get_server_response(json.dumps(INPUT))
    assert resp.status == 200
    assert_same_jsons(EXPECTED, json.loads(content))
