from akara import logger, response, module_config
from akara.services import simple_service
from dplaingestion.selector import getprop, delprop
from amara.thirdparty import json
from akara import logger

rightsURIs = \
        module_config('enrich_rights').get('rights_URIs')

@simple_service('POST', 'http://purl.org/la/dp/enrich-rights', 'enrich-rights',
                'application/json')

def enrichrights(body,
               action="enrich-rights",
               prop="sourceResource/rights"):
    """
    Service that accepts a JSON document and enriches the "rights" field of that document by mapping URI values from Creative Commons or Rightsstatement.org URI value, where found, to human-readable version of corresponding statement. If no CC/Rightsstatement URI found, leave the rights value as-is. Also strips version # from URI for easier pattern matching
    """
    global rightsURIs

    try:
        data = json.loads(body)
    except Exception:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    rights_strings = []
    try:
        sr_rights = data['sourceResource'].get('rightsURI')
    except KeyError:
        # In this case, sourceResource is not present, so give up and return the original data unmodified.
        id_for_msg = data.get('_id', '[no id]')
        logger.warning('enrich-rights lacks sourceResource for _id %s' % \
                id_for_msg)
        return body
    if sr_rights:
        for t in sr_rights if (type(sr_rights) == list) else [sr_rights]:
            t_flat = t
            if type(t) == dict:
                t_flat = t.get('#text', None)
                if not t_flat:
                    t_flat = t.get('text', '')
            rights_strings.append(t_flat)
    try:
        data['sourceResource']['rights'] = \
                rights_for_strings_and_mappings([
                    (rights_strings, rightsURIs),
                ])
    except ValueError:
        # Delete sourceResource.rightsURI if not valid RS/CC URI
        delprop(data, "sourceResource/rightsURI")
        id_for_msg = data.get('_id', '[no id]')
        logger.warning('Not a valid CC or RS rights URI for item with _id: %s' % \
                       id_for_msg)
        pass

    return json.dumps(data)

def _rightsstatement_for_uri(s, mappings):
    """Given a URI string, return corresponding human readable text, or original value if not a URI.

    mapping: a tuple of (string, type)
    """
    rights_string = s.lower()
    for pair in mappings.items():

        if pair[0] in rights_string:
            return pair[1]

    raise ValueError

def rights_for_strings_and_mappings(string_map_combos):
    """_rights_for_strings_and_mappings([(list, list_of_tuples), ...])

    Given pairs of (list of strings, list of mapping tuples), try to find a
    matching rights statement.
    """
    for strings, mappings in string_map_combos:
        for s in strings:
            s = str(s)
            t = _rightsstatement_for_uri(s, mappings)
            if t:
                return t
