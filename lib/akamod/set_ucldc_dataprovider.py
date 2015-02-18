from amara.thirdparty import json
from akara.services import simple_service
from akara import request, response
#from akara import logger
from dplaingestion.selector import getprop, setprop, exists

@simple_service('POST',
    'http://purl.org/org/cdlib/ucldc/set-ucldc-dataprovider',
                'set-ucldc-dataprovider',
                'application/json')
def set_ucldc_dataprovider(body, ctype):
    '''For ucldc, we always have a originalRecord/repository entry and
    an originalRecord/campus (which may be blank).
    Concatenate these, separated by a , for dataProvider value
    '''
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"
    
    repo = getprop(data,'originalRecord/repository')[0]
    campus = getprop(data,'originalRecord/campus')
    dataProvider = repo['name']
    if campus:
        dataProvider = ', '.join((campus[0]['name'], repo['name']))
    setprop(data, 'dataProvider', dataProvider)
    return json.dumps(data)
