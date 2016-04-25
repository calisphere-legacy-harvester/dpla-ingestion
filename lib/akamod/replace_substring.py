from akara import logger
from akara import response
from akara.services import simple_service
from amara.thirdparty import json
from dplaingestion.selector import getprop, setprop, exists
import re

def replace_substring_recurse_field(value, old, new):
    '''Replace the substrings found in various types of data.
    Can be strings, lists or dictionaries
    '''
    if isinstance(value, basestring):
        return value.replace(old, new).strip()
    if isinstance(value, list):
        newlist = []
        for v in value:
            newlist.append(replace_substring_recurse_field(v, old, new))
        return newlist
    if isinstance(value, dict):
        for k, v in value.items():
            value[k] = replace_substring_recurse_field(v, old, new)
        return value
    return None

@simple_service('POST', 'http://purl.org/la/dp/replace_substring',
                'replace_substring', 'application/json')
def replace_substring(body, ctype, prop=None, old=None, new=None):
    """Replaces a substring in prop

    Keyword arguments:
    body -- the content to load
    ctype -- the type of content
    prop -- the prop to apply replacing
    old -- the substring to replace
    new -- the substring to replaced old with
    
    """

    try:
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    if not old:
        logger.error("No old parameters were provided")
    else:
        if not new:
            logger.debug("NO New parameter, will replace with empty string")
            new = ''
        if exists(data, prop):
            v = getprop(data, prop)
            new_val = replace_substring_recurse_field(v, old, new)
            setprop(data, prop, new_val)

    return json.dumps(data)

def replace_regex_recurse_field(value, regex_s, new):
    '''Replace the regexs found in various types of data.
    Can be strings, lists or dictionaries
    This uses a regex to replace
    '''
    if isinstance(value, basestring):
        regex = re.compile(regex_s)
        return regex.sub(new, value).strip()
    if isinstance(value, list):
        newlist = []
        for v in value:
            newlist.append(replace_regex_recurse_field(v, regex_s, new))
        return newlist
    if isinstance(value, dict):
        for k, v in value.items():
            value[k] = replace_regex_recurse_field(v, regex_s, new)
        return value
    return None

@simple_service('POST', 'http://purl.org/la/dp/replace_regex',
                'replace_regex', 'application/json')
def replace_regex(body, ctype, prop=None, regex=None, new=None):
    """Replaces a regex in prop

    Keyword arguments:
    body -- the content to load
    ctype -- the type of content
    prop -- the prop to apply replacing
    regex -- the regex to replace
    new -- the substring to replaced regex with
    
    """

    try:
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    if not regex:
        logger.error("No regex parameter supplied")
    else:
        if not new:
            logger.debug("NO New parameter, will replace with empty string")
            new = ''
        if exists(data, prop):
            v = getprop(data, prop)
            new_val = replace_regex_recurse_field(v, regex, new)
            setprop(data, prop, new_val)

    return json.dumps(data)
