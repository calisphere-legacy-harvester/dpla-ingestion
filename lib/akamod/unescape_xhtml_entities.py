from HTMLParser import HTMLParser
from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json
from dplaingestion.selector import getprop, setprop, exists
from dplaingestion.utilities import iterify

hparser = HTMLParser()

def unescape_xhtml_string(xhtml_string):
    '''Unescape any xhtml entities in a string.
    Maps to iso-latin-1 code points in unicode
    returns unescaped string
    '''
    return hparser.unescape(xhtml_string)

def unescape_xhtml_object(obj):
    '''Unescape a python object.
    Can be a string, list or dict object.
    Call recursively and return?
    '''
    if isinstance(obj, basestring):
        return unescape_xhtml_string(obj)
    elif isinstance(obj, list):
        newlist = []
        for value in obj:
            newlist.append(unescape_xhtml_object(value))
        obj = newlist
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = unescape_xhtml_object(value)
    return obj


@simple_service('POST', 'http://purl.org/org/cdlib/ucldc/unescape-xhtml-entities', 'unescape-xhtml-entities',
    'application/json')
def unescape_xhtml_entities(body, ctype, field=None):
    '''Unescape xhtml entities in data values for a field and it's subfields

    Keyword arguments:
    body -- the content to load
    ctype -- the type of content
    field -- top level field to unescape, unescape sub fields
             for now will just operate on the sourceResource data
    '''
    try:
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    # TODO: make recursive, in case it is needed for other fields
    if exists(data, field):
        prop = getprop(data, field)
        setprop(data, field, unescape_xhtml_object(prop))
    return json.dumps(data)
