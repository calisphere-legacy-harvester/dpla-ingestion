import sys
import argparse
import ConfigParser
import httplib
import json
import couchdb

COUCHDB_VIEW = 'all_provider_docs/by_provider_name'

config = ConfigParser.ConfigParser()
config.readfp(open('akara.ini'))

class EnrichmentError(Exception):
    pass

def main(enrichment,
         collection_key=None, 
         url_couchdb=None,
         couchdb_name=None,
         couch_view=COUCHDB_VIEW,):
    '''Enrich couch docs in the given collection.
    Should probably use ingestion_doc to get provider and record results
    TODO: get couchdb info from akara.ini
    '''
    print('ENRICH {}'.format(enrichment))
    print('KEY {}'.format(collection_key))
    if not collection_key:
        print('WARNING: Running {} on all docs.......'.format(enrichment))
    if not url_couchdb:
        url_couchdb = config.get('CouchDb', 'URL')
    if not couchdb_name:
        couchdb_name = config.get('CouchDb', 'ItemDatabase')
    _couchdb = couchdb.Server(url=url_couchdb)[couchdb_name]
    v = _couchdb.view(couch_view, include_docs='true',
                               key=collection_key) if collection_key else \
                               _couchdb.view(couch_view, include_docs='true')
    port = int(config.get('Akara', 'Port'))
    conn = httplib.HTTPConnection("localhost", port)
    for r in v:
        try:
            source = r.doc['originalRecord']['collection'][0]['@id']
        except KeyError, e:
            print("BAD ID: {}".format(r.doc['_id']))
            print("KEYS:{}".format(r.doc['originalRecord'].keys()))
            raise e
        headers = {
                "Source": source,
                "Content-Type": "application/json",
                "Pipeline-item": enrichment,
                }
        conn.request("POST", "/enrich", json.dumps([r.doc]), headers)
        resp = conn.getresponse()

        if not resp.status == 200:
            raise EnrichmentError("Error (status {}) for doc {}".format(resp.status,
                r.doc['_id']))

        data = json.loads(resp.read())
        for _id, ndoc  in data['enriched_records'].items():
            ndoc['originalRecord'] = ndoc['originalRecord']['originalRecord']
            _couchdb.save(ndoc)

def define_arguments():
    """Defines command line arguments for the current script"""
    parser = argparse.ArgumentParser()
    #parser.add_argument("ingestion_document_id", 
    #                    help="The ID of the ingestion document")
    parser.add_argument("enrichment_path", 
                        help="path for the enrichment to run")
    parser.add_argument("--key", 
                        help="collection key in couch, currently collection slug")
    return parser

if __name__=='__main__':
    parser = define_arguments()
    args = parser.parse_args(sys.argv[1:])
    main(args.enrichment_path, collection_key=args.key)
