'''Map the UCLA Islandora solr search items to the DPLA metadata profile.
PID is the field for the local ID of the item. Looks to be collection
java like name with an index into collection.
From Kristian Allen at UCLA the actual object can be found at:
    http://digital.library.ucla.edu/collections/islandora/object/<PID>

Will get the full sized JPEG 2000 from them for the objects.
'''
import base64

from akara import logger
from akara import request, response
from akara.services import simple_service
from amara.lib.iri import is_absolute
from amara.thirdparty import json
from dateutil.parser import parse as dateutil_parse

from dplaingestion.selector import getprop
from dplaingestion.akamod.context import CONTEXT

URL_UCLA_OBJECT_ROOT = 'http://digital.library.ucla.edu/collections/islandora/object/'

# default date used by dateutil-python to populate absent date elements during parse,
# e.g. "1999" would become "1999-01-01" instead of using the current month/day
DEFAULT_DATETIME = dateutil_parse("2000-01-01") 

def is_shown_at_transform(d):
    '''For the UCLA Islandora implementation, the URL of the local object
    page can be found from:
    http://digital.library.ucla.edu/collections/islandora/object/<PID>
    '''
    return {"isShownAt" :  ''.join((URL_UCLA_OBJECT_ROOT, d['PID'])) }

def spatial_transform(d):
    spatial = d["dc.coverage"]
    if spatial and not isinstance(spatial, list):
        spatial = [spatial]

    return {"spatial": spatial} if spatial else {}

# Structure mapping the original property to a function returning a single
# item dict representing the new property and its value
CHO_TRANSFORMER = {
    "dc.collection"       : lambda d: {"collection": d.get("dc.collection",None)},
    "dc.contributor"      : lambda d: {"contributor": d.get("dc.contributor",None)},
    "dc.coverage"         : spatial_transform,
    "dc.creator"          : lambda d: {"creator": d.get("dc.creator",None)},
    "dc.description"      : lambda d: {"description": d.get("dc.description",None)},
    "dc.date"             : lambda d: {"date": d.get("dc.date",None)},
    "dc.identifier"         : lambda d: {"identifier": d.get("dc.identifier",None)},
    "dc.language"         : lambda d: {"language": d.get("dc.language",None)},
    "dc.publisher"        : lambda d: {"publisher": d.get("dc.publisher",None)},
    "dc.relation"         : lambda d: {"relation": d.get("dc.relation",None)},
    "dc.rights"           : lambda d: {"rights": d.get("dc.rights",None)},
    "dc.subject"          : lambda d: {"subject": d.get("dc.subject",None)},
    "dc.title"            : lambda d: {"title": d.get("dc.title",None)},
    "dc.type"             : lambda d: {"type": d.get("dc.type",None)},
    "dc.format"           : lambda d: {"format": d.get("dc.format",None)},
    "dc.extent"           : lambda d: {"extent": d.get("dc.extent", None)}
}

AGGREGATION_TRANSFORMER = {
    "id"               : lambda d: {"id": d.get("id",None), "@id" : "http://ucldc/api/items/"+d.get("id","")},
    "_id"              : lambda d: {"_id": d.get("_id",None)},
    "PID"           : is_shown_at_transform,
    "originalRecord"   : lambda d: {"originalRecord": d.get("originalRecord",None)},
    "source"           : lambda d: {"dataProvider": d.get("source",None)},
    "provider"         : lambda d: {"provider": d.get("provider", None)},
    "ingestType"       : lambda d: {"ingestType": d.get("ingestType",None)},
    "ingestDate"       : lambda d: {"ingestDate": d.get("ingestDate",None)}
}

@simple_service('POST', 'http://purl.org/la/dp/ucla-solr-to-dpla', 'ucla-solr-to-dpla', 'application/ld+json')
def ucla_islandora_solr_to_dpla(body,ctype,geoprop=None):
    '''   
    Convert output of the UCLA solr index to DPLA metadata profile

    '''

    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type','text/plain')
        return "Unable to parse body as JSON"

    global GEOPROP
    GEOPROP = geoprop

    out = {
        "@context": CONTEXT,
        "sourceResource" : {}
    }

    # Apply all transformation rules from original document to sourceResource
    for p in data.keys():
        if p in CHO_TRANSFORMER:
            out['sourceResource'].update(CHO_TRANSFORMER[p](data))
        if p in AGGREGATION_TRANSFORMER:
            print("P:{}".format(p) )
            out.update(AGGREGATION_TRANSFORMER[p](data))

    # Strip out keys with None/null values?
    #out = dict((k,v) for (k,v) in out.items() if v)

    return json.dumps(out)
