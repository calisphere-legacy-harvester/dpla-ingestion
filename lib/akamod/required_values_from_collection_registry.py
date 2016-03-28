from amara.thirdparty import json
from akara.services import simple_service
from akara import request, response
from akara import logger
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
            'F': 'Moving Image',
            'R': 'Interactive Resource',
            'V': 'Service',
            'S': 'Software',
            'A': 'Sound', # A for audio
            'T': 'Text',
            'P': 'Physical Object',
            #'X': 'type unknown' # default, not set
            }

RIGHTS_STATUS_DEFAULT = RIGHTS_STATUS['UN']
RIGHTS_STATEMENT_DEFAULT = 'Please contact the contributing institution for more information regarding the copyright status of this object. Its presence on this site does not necessarily mean it is free from copyright restrictions.'
RIGHTS_STATEMENT_DEFAULT = 'Please contact the contributing institution for more information regarding the copyright status of this object.'

def get_collection(data):
    return getprop(data,'originalRecord/collection')[0]

def set_field_from_value_mode(data, field, mode, value, multivalue=True):
    '''Set the value for the data "field" from data in collection
    ckey field with the value passed in.
    '''
    logger.debug('Field:{} mode:{} value:{} mv:{}'.format(field, mode, value, multivalue))
    if value: #no value don't bother
        if mode=='overwrite':
            if exists(data, field):
                setprop(data, field, value)
            else:
                pp,pn = tuple(field.lstrip('/').split('/',1))
                if not pp in data:
                    data[pp] = {}
                data[pp][pn] = value
        elif mode=='append':
            new_value = []
            if exists(data, field):
                old_value = getprop(data, field)
                if isinstance(old_value, list):
                    new_value.extend(old_value)
                else:
                    new_value.append(old_value)
            if isinstance(value, list):
                new_value.extend(value)
            else:
                new_value.append(value)
            setprop(data, field, new_value)
        else: # fill blanks
            if not exists(data, field) or not getprop(data,
                    field,keyErrorAsNone=True):
                if multivalue and not isinstance(value, list):
                    value = [value]
                setprop(data, field, value)
    return data

def set_rights_from_collection(data, mode):
    collection = get_collection(data)
    rights_code = collection['rights_status']
    rights_status = RIGHTS_STATUS.get(rights_code, None)
    rights_statement = collection['rights_statement']
    rights_coll = [RIGHTS_STATEMENT_DEFAULT]
    if rights_status and rights_statement:
        rights_coll = [rights_status, rights_statement]
    elif rights_status:
        rights_coll = rights_status
    elif rights_statement:
        rights_coll = rights_statement
    data = set_field_from_value_mode(data, 'sourceResource/rights', mode,
            rights_coll)
    return data


def set_type_from_collection(data, mode):
    collection = get_collection(data)
    type_code = collection['dcmi_type']
    dcmi = DCMI_TYPES.get(type_code, None)
    data = set_field_from_value_mode(data, 'sourceResource/type', mode,
            dcmi, multivalue=False)
    return data

def set_title_for_object(data):
    data = set_field_from_value_mode(data, 'sourceResource/title', 'fill',
            'Title unknown')
    return data

@simple_service('POST',
    'http://purl.org/org/cdlib/ucldc/required-values-from-collection-registry',
                'required-values-from-collection-registry',
                'application/json')
def required_values_from_collection_registry(body, ctype, field, mode):
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
    
    if field == 'rights':
        data = set_rights_from_collection(data, mode)
    elif field == 'type':
        data = set_type_from_collection(data, mode)
    elif field == 'title':
        data = set_title_for_object(data)
    #ensure "@context" is there
    if not exists(data, "@context"):
        data["@context"] = "http://dp.la/api/items/context"
    return json.dumps(data)
