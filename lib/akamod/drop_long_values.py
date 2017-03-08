# pass in a Couchdb doc, get back one with de-duplicated sourceResource values
from amara.thirdparty import json
from akara.services import simple_service
from akara import response


@simple_service('POST', 'http://purl.org/org/cdlib/ucldc/drop-long-values',
                'drop-long-values', 'application/json')
def drop_long_values(body, ctype, field=None, max_length=150):
    ''' Look for long values in the sourceResource field specified.
    If value is longer than max_length, delete
    '''
    try:
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    fieldvalues = data['sourceResource'].get(field)
    if isinstance(fieldvalues, list):
        new_list = []
        for item in fieldvalues:
            if len(item) <= int(max_length):
                new_list.append(item)
        data['sourceResource'][field] = new_list
    else:  # scalar
        if len(fieldvalues) > int(max_length):
            del data['sourceResource'][field]

    return json.dumps(data)
