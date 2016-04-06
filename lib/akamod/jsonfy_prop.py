import numbers
from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json
from dplaingestion.selector import getprop, setprop, delprop

def jsonfy_obj(obj):
    '''Jsonfy a python dict object. For immediate sub items (not recursive yet
    if the data can be turned into a json object, do so.
    Unpacks string json objects buried in some blacklight/solr feeds.
    '''
    obj_jsonfied = {}
    if isinstance(obj, numbers.Number) or isinstance(obj, bool):
        return obj
    if isinstance(obj, basestring):
        try:
            x = json.loads(obj)
        except (ValueError, TypeError) as e:
            x = obj
        return x
    for key, value in obj.items():
        if isinstance(value, list):
            new_list = []
            for v in value:
                try:
                    x = jsonfy_obj(v)
                    new_list.append(x)
                except (ValueError, TypeError) as e:
                    new_list.append(v)
            obj_jsonfied[key] = new_list
        else: #usually singlevalue string, not json
            try:
                x = json.loads(value)
            except (ValueError, TypeError) as e:
                x = value
            obj_jsonfied[key] = x
    return obj_jsonfied

@simple_service("POST", "http://purl.org/la/dp/jsonfy-prop",
                "jsonfy-prop", "application/json")
def jsonfy_prop(body, ctype, prop=None):
    """ Some data is packed as strings that contain json. (UCSD)
    Take the data in the given property and turn any sub-values that can be 
    read by json.loads into json object.
    """

    try:
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    if prop:
        obj = getprop(data, prop, True)
    else:
        obj = data

    obj_jsonfied = jsonfy_obj(obj)
    if prop:
        setprop(data, prop, obj_jsonfied)
    else:
        data = obj_jsonfied
    return json.dumps(data)
