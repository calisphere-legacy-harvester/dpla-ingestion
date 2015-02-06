from amara.thirdparty import json
from amara.lib.iri import is_absolute
from akara.services import simple_service
from akara.util import copy_headers_to_dict
from akara import request, response
from akara import logger
from dplaingestion.selector import getprop, setprop, exists

URL_BASE_OBJECT_VIEW = 'http://rescarta.lapl.org/ResCarta-Web/'
URL_BASE_THUMBNAIL = 'http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id='

@simple_service('POST', 'http://purl.org/org/cdlib/ucldc/lapl-oai-isShown-26096', 'lapl-oai-isShown-26096',
                'application/json')
def lapl_oai_isShown_26096(body, ctype):
    '''Map from the oai source records for LAPL collection 26096 (city
    directory) to the isShownAt & isShownBy properties.

    These are calculated from a portion of the identifier data per Adrian.
    The dc identifiers are of format:
    rescarta.lapl.org/jsp/RcWebImageViewer.jsp?doc_id=040428be-8b21-4de1-9b1e-3421068c0f1c/cl000000/20140507/00000002

    isShownAt:
    Use dc:identifier, but strip off "rescarta.lapl.org/jsp" and
    replace with "http://rescarta.lapl.org/ResCarta-Web/jsp"
    e.g.
    http://rescarta.lapl.org/ResCarta-Web/jsp/RcWebImageViewer.jsp?doc_id=040428be-8b21-4de1-9b1e-3421068c0f1c/cl000000/20140123/00000002

    isShownBy:
    Base URL is: 
    http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id= 
    after obj_id= use the charracters in the dc:identifier field that begin with    ""c1"" to the end of the identifier to get the specific identifier and
    append

    An example of the complete URLis:
    http://rescarta.lapl.org/ResCarta-Web/servlet/RcWebThumbnail?obj_type=SERIAL_MONOGRAPH&pg_idx=0&obj_id=cl000000/20140507/00000027
    '''

    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"
    
    if exists(data,'originalRecord/identifier'):
        identifier_url = getprop(data,'originalRecord/identifier')[0]
        # split off at /jsp
        object_view_path = identifier_url[identifier_url.index('jsp'):]
        data['isShownAt'] = URL_BASE_OBJECT_VIEW + object_view_path
        obj_id = object_view_path[object_view_path.index('=')+1:]
        obj_thumb_id = obj_id.split('/', 1)[1]
        data['isShownBy'] = URL_BASE_THUMBNAIL + obj_thumb_id

    return json.dumps(data)
