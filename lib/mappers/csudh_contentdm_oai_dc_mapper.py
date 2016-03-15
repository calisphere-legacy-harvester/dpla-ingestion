from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.selector import exists, getprop

class CSUDH_CONTENTdm_OAI_Mapper(CONTENTdm_OAI_Mapper):
    '''A mapper for CONTENTdm OAI feed from CSUDH
    There is a weird situation here. Some objects have 2 titles, with the
    first being an identifier. This causes problems with the front end, which
    shows the first title. So the titles are the IDs, which looks horrible.

    There are 2 types of IDs, ARKs & a local id. We're going to drop ARKs
    because not sure that CSUDH is actually using them. For the local ids of
    form "csudh_ish_<id num>", we can put these into the identifier and they
    won't get used for our ID.

    '''
    def map_title(self):
        '''map_title is run after map identifier, so sourceResource/identifier
        should already exist
        '''
        prop = 'title'
        provider_prop = prop if not self.prefix else ''.join((self.prefix, prop))
        if exists(self.provider_data_source, provider_prop):
            data = getprop(self.provider_data_source, provider_prop)
            if isinstance(data, basestring):
                self.update_source_resource({prop: data})
            else: #should be list
                #build new title data
                new_title = []
                for t in data:
                    if t.startswith('ark:'):
                        pass #drop it
                    elif t.startswith('csudh'):
                        #append to sourceResource/identifier
                        self.mapped_data["sourceResource"].get('identifier',
                                []).append(t)
                    else: #add to real title
                        new_title.append(t)
                if new_title:
                    self.update_source_resource({prop: new_title})

