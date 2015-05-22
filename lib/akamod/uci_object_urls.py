from amara.thirdparty import json
from akara.services import simple_service
from akara import request, response

@simple_service('POST', 'http://purl.org/la/dp/uci-object-urls',
    'uci-object-urls', 'application/json')
def uci_object_urls(body, ctype):
    '''Fill in the isShownBy & isShownAt values for UCI OAI didl recs'''

    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"

    data['isShownAt'] = data.get('identifier', [None])[0]
    resource = data.get('Resource', {})
    data['isShownBy'] = resource.get('@ref', '')
    
    return json.dumps(data)
