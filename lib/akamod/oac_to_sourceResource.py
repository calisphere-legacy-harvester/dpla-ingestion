#Take relevant OAC data and populate sourceResource fields

# isShownBy -- reference image or object file on calisphere

import base64

from akara import logger
from akara import request, response
from akara.services import simple_service
from amara.lib.iri import is_absolute
from amara.thirdparty import json

URL_BASE = 'http://content.cdlib.org/'
URL_SUFFIX = '/thumbnail'

@simple_service('POST', 'http://purl.org/cdlib/dsc/oac-to-sourceResource', 'oac-to-sourceResource', 'application/ld+json')
def oac_to_sourceResource(body, ctype):
    '''   
    Fill in the sourceResource fields that map from OAC only fields (not DC)

    '''
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse data object body as JSON"
    x = 0
    best_image = None
    for obj in data['originalRecord']['reference-image']:
        if int(obj['x']) > x:
            x = int(obj['x'])
            best_image = obj
    data["isShownBy"] = best_image
    return json.dumps(data)
