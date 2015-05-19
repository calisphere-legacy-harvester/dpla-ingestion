# pass in a Couchdb doc, get back one with de-duplicated sourceResource values
from amara.thirdparty import json
from amara.lib.iri import is_absolute
from akara.services import simple_service
from akara.util import copy_headers_to_dict
from akara import request, response
from dplaingestion.selector import getprop, setprop, exists

@simple_service('POST', 'http://purl.org/org/cdlib/ucldc/dedupe-sourceresource',
                'dedupe-sourceresource',
                'application/json')
def dedupe_srcres(body, ctype):
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    doc = remove_blank_values(data)
    return json.dumps(dedupe_sourceresource(doc))

def remove_blank_values(doc):
    '''Remove blank values from the sourceResource'''
    for key, value in doc['sourceResource'].items():
        if not value:
            del doc['sourceResource'][key]
    return doc

# from harvester.post_processing.dedup_sourceresource
# need to un-duplicate this code, but circular import?
def dedupe_sourceresource(doc):
    ''' Look for duplicate values in the doc['sourceResource'] and 
    remove.
    Values must be *exactly* the same
    '''
    for key, value in doc['sourceResource'].items():
        if isinstance(value, list):
            # can't use set() because of dict values (non-hashable)
            new_list = []
            for item in value:
                if item not in new_list:
                    new_list.append(item)
            doc['sourceResource'][key] = new_list
    return doc
