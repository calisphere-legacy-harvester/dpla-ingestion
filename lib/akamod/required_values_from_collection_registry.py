from amara.thirdparty import json
#from amara.lib.iri import is_absolute
from akara.services import simple_service
#from akara.util import copy_headers_to_dict
#from akara import request, response
#from akara import logger
from dplaingestion.selector import getprop, setprop, exists


# repeating self here, how to get from avram?
RIGHTS_STATUS = { 'CR':'copyrighted',
                  'PD': 'public domain',
                  'UN': 'copyright unknown',
                  #'X':  'rights status unknown', # or should throw error?
                }
DCMI_TYPES = {'C': 'Collection',
            'D': 'Dataset',
            'E': 'Event',
            'I': 'Image',
            'R': 'Interactive Resource',
            'V': 'Service',
            'S': 'Software',
            'A': 'Sound', # A for audio
            'T': 'Text',
            #'X': 'type unknown' # default, not set
            }

@simple_service('POST',
    'http://purl.org/org/cdlib/ucldc/required-values-from-collection-registry',
                'required-values-from-collection-registry',
                'application/json')
def required_values_from_collection_registry(body, ctype, mode):
    '''Get values for the required fields sourceResource.rights &
    sourceResource.type from the collection registry data.
    Default mode is to fill in missing data.
    mode='overwrite' will overwrite existing data
    mode='append' will add the values
    '''
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"
    
    #switch on mode
    collection = getprop(data,'originalRecord/collection')[0]
    rights_code = collection['rights_status']
    rights_status = RIGHTS_STATUS.get(rights_code, None)
    rights_statement = collection['rights_statement']
    rights_coll = None
    if rights_status and rights_statement:
        rights_coll = [rights_status, rights_statement]
    elif rights_status:
        rights_coll = rights_status
    elif rights_statement:
        rights_coll = rights_statement
    type_code = collection['dcmi_type']
    dcmi = DCMI_TYPES.get(type_code, None)
    if mode=='overwrite':
        if not dcmi or not rights_coll:
            raise ValueError('Overwrite values specified but collection is missing data')
        setprop(data, 'sourceResource/rights', rights_coll)
        setprop(data, 'sourceResource/type', dcmi)
    elif mode=='append':
        if dcmi:
            type_data = getprop(data, 'sourceResource/type')
            new_type = []
            if isinstance(type_data, list):
                new_type.extend(type_data)
            else:
                new_type.append(type_data)
            new_type.append(dcmi)
            setprop(data, 'sourceResource/type', new_type)
        if rights_coll:
            rights_data = getprop(data, 'sourceResource/rights')
            new_rights = []
            if isinstance(rights_data, list):
                new_rights.extend(rights_data)
            else:
                new_rights.append(rights_data)
            if isinstance(rights_coll, list):
                new_rights.extend(rights_coll)
            else:
                new_rights.append(rights_coll)
            setprop(data, 'sourceResource/rights', new_rights)
    else: # fill blanks
        if not exists(data,'sourceResource/type'):
            if dcmi:
                setprop(data, 'sourceResource/type', dcmi)
        if not exists(data,'sourceResource/rights'):
            if not rights_status and not rights_statement:
                raise ValueError('Collection does not contain rights information for {}'.format(data['_id']))
            else:
                rights = rights_coll
            setprop(data, 'sourceResource/rights', rights)
            
    return json.dumps(data)
