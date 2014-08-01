#Take relevant OAC data and populate sourceResource fields

# isShownBy -- reference image or object file on calisphere

import base64

from akara import logger
from akara import request, response
from akara.services import simple_service
from amara.lib.iri import is_absolute
from amara.thirdparty import json

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
    best_image = None
    x = 0
    thumb = data['originalRecord'].get('thumbnail', None)
    if thumb:
        x = thumb['X']
        best_image = thumb
    ref_images = data['originalRecord'].get('reference-image', [])
    if type(ref_images) == dict:
        ref_images = [ref_images]
    for obj in ref_images:
        if int(obj['X']) > x:
            x = int(obj['X'])
            best_image = obj
    if best_image:
        data["isShownBy"] = best_image
    return json.dumps(data)
