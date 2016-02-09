from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
from dplaingestion.selector import exists, getprop
from dplaingestion.utilities import iterify

class UCLASolrDCMapper(DublinCoreMapper):
    URL_UCLA_OBJECT_ROOT = 'http://digital.library.ucla.edu/collections/islandora/object/'

    def __init__(self, provider_data): 
        super(UCLASolrDCMapper, self).__init__(provider_data, prefix='dc.')

    # root mapping
    def map_is_shown_at(self, index=None):
        self.mapped_data.update( {"isShownAt" :  ''.join((self.URL_UCLA_OBJECT_ROOT, self.provider_data['PID'])),
            "isShownBy" :  ''.join((self.URL_UCLA_OBJECT_ROOT, self.provider_data['PID'], '/datastream/JPG/JPG.jpg')),
            })

    def map_data_provider(self):
        super(UCLASolrDCMapper, self).map_data_provider(prop="collection")

    def map_state_located_in(self):
        self.update_source_resource({"stateLocatedIn": [{"name": "California"}]})

    def map_spatial(self):
        if exists(self.provider_data, "dc.coverage"):
            self.update_source_resource({"spatial":
                                         iterify(getprop(self.provider_data,
                                                         "dc.coverage"))})

    def map_identifier(self):
        '''UCLA ARKs are buried in a mods field in originalRecord:

        "mods_recordInfo_recordIdentifier_mlt": "21198-zz002b1833",
        "mods_recordInfo_recordIdentifier_s": "21198-zz002b1833",
        "mods_recordInfo_recordIdentifier_t": "21198-zz002b1833",
        
        If one is found, safe to assume UCLA & make the ARK
        NOTE: I cut & pasted this to the ucla_solr_dc_mapper to get it
        into the "identifier" field
        '''
        super(UCLASolrDCMapper, self).map_identifier()
        # Now add the ark to the sourceResource/identifier
        ark = None
        id_fields =("mods_recordInfo_recordIdentifier_mlt",
                     "mods_recordInfo_recordIdentifier_s",
                     "mods_recordInfo_recordIdentifier_t",
                     "mods_recordIdentifier_ms",
                     "mods_recordIdentifier_mt")
        import sys
        for f in id_fields:
            print >> sys.stderr, "TRYING TO GET:{}".format(f)
            try:
                mangled_ark = self.provider_data[f]
                if isinstance(mangled_ark, list):
                    mangled_ark = mangled_ark[0]
                naan, arkid = mangled_ark.split('-') #could fail?
                ark = '/'.join(('ark:', naan, arkid))
                break
            except KeyError:
                print >> sys.stderr, "FAILED TO GET:{}".format(f)
                pass
    
        if ark:
            try:
                self.mapped_data["sourceResource"]['identifier'].append(ark)
            except KeyError: #no identifier
                self.mapped_data["sourceResource"]['identifier'] = [ark]
