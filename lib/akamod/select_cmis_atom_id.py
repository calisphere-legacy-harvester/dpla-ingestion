# -*- coding: utf-8 -*-
import hashlib
import sys
from amara.thirdparty import json
from amara.lib.iri import is_absolute
from akara.services import simple_service
from akara.util import copy_headers_to_dict
from akara import request, response
from dplaingestion.selector import getprop, setprop, exists

COUCH_ID_BUILDER = lambda src, lname: "--".join((src,lname))
COUCH_REC_ID_BUILDER = lambda src, id_handle: COUCH_ID_BUILDER(src,id_handle.strip().replace(" ","__"))

def select_id(source_name, data):
    objid = None
    #the json representation is crazy
    vlist = data["{http://www.w3.org/2005/Atom}entry"]["{http://docs.oasis-open.org/ns/cmis/restatom/200908/}object"]["{http://docs.oasis-open.org/ns/cmis/core/200908/}properties"]["{http://docs.oasis-open.org/ns/cmis/core/200908/}propertyId"]
    for v in vlist:
        if v.get("@propertyDefinitionId",'') ==  "cmis:objectId":
            objid = v["{http://docs.oasis-open.org/ns/cmis/core/200908/}value"]["$"]

    if not objid:
        raise ValueError("Couldn't find property to extract id")

    objid = objid.split('|')[1]

    data[u'_id'] = COUCH_REC_ID_BUILDER(source_name, objid)
    data[u'id']  = hashlib.md5(data[u'_id']).hexdigest()

@simple_service('POST', 'http://purl.org/la/dp/select-cmis-atom-id',
'select-cmis-atom-id',
                'application/json')
def selectid(body, ctype):
    '''   
    Service that accepts a JSON document and adds or sets the "id" property to
    the value of the property named by the "prop" paramater
    '''   
    try :
        data = json.loads(body)
    except:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "Unable to parse body as JSON"

    request_headers = copy_headers_to_dict(request.environ)
    source_name = request_headers.get('Source')
    try:
        select_id(source_name, data)
    except ValueError, e:
        response.code = 500
        response.add_header('content-type', 'text/plain')
        return "No id property was found"

    return json.dumps(data)


# Copyright © 2016, Regents of the University of California
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

