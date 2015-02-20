import hashlib
from amara.thirdparty import json
from amara.lib.iri import is_absolute
from akara.services import simple_service
from akara.util import copy_headers_to_dict
from akara import request, response
from akara import logger

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))
COUCH_REC_ID_BUILDER = lambda src, id_handle: COUCH_ID_BUILDER(src,id_handle.strip().replace(" ","__"))

@simple_service('POST', 'http://purl.org/org/cdlib/ucldc/sfpl-marc-id', 'sfpl-marc-id',
                'application/json')
def sfpl_marc_id(body, ctype):
    '''MARC sucks'''
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"

    ident = None
    for field in data['fields']:
        if '010' in field:
            subfields = field['010']['subfields']
            for subf in subfields:
                if 'a' in subf:
                    ident = subf['a']

    if not ident:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "No id property was found"

    request_headers = copy_headers_to_dict(request.environ)
    source_name = request_headers.get('Source')
    
    data[u'_id'] = COUCH_REC_ID_BUILDER(source_name, ident)
    data[u'id']  = hashlib.md5(data[u'_id']).hexdigest()

    return json.dumps(data)
