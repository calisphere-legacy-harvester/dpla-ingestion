import base64

from akara import logger
from akara import request, response
from akara.services import simple_service
from amara.lib.iri import is_absolute
from amara.thirdparty import json

URL_BASE = 'http://content.cdlib.org/'
URL_SUFFIX = '/thumbnail'

@simple_service('POST', 'http://purl.org/cdlib/dsc/oac-thumbnail', 'oac-thumbnail', 'application/ld+json')
def oac_thumbnail(body, ctype):
    '''   
    Fill in the OAC thumbnail location.
    http://content.cdlib.org/<ark>/thumbnail


    '''
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"

    ark = ''.join(('ark:', data['_id'].split('ark:')[1]))
    data["object"] = ''.join((URL_BASE, ark, URL_SUFFIX))
    return json.dumps(data)
