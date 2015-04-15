import hashlib
import sys
from amara.thirdparty import json
from amara.lib.iri import is_absolute
from akara.services import simple_service
from akara.util import copy_headers_to_dict
from akara import request, response
from dplaingestion.selector import getprop, setprop, exists

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))
COUCH_REC_ID_BUILDER = lambda src, id_handle: COUCH_ID_BUILDER(src,id_handle.strip().replace(" ","__"))

@simple_service('POST', 'http://purl.org/la/dp/select-oac-id', 'select-oac-id',
                'application/json')
def selectid(body, ctype):
    '''   
    Service that accepts a JSON document and adds or sets the "id" property to
    the value of the property named by the "prop" paramater
    '''   
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    request_headers = copy_headers_to_dict(request.environ)
    source_name = request_headers.get('Source')

    objid = None
    v = getprop(data, 'identifier')
    if isinstance(v,basestring):
        objid = v
    else:
        if v:
            for h in (v if isinstance(v, list) else [v]):
                if h['text'].startswith('http://ark.cdlib.org/ark:'):
                    if is_absolute(h['text']):
                        objid = h['text']
                if not objid:
                    objid = v[0]

    if not objid:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "No id property was found"

    data[u'_id'] = COUCH_REC_ID_BUILDER(source_name, objid)
    data[u'id']  = hashlib.md5(data[u'_id']).hexdigest()
    data[u'isShownAt'] = objid
    data[u'isShownBy'] = objid + '/thumbnail'

    return json.dumps(data)
