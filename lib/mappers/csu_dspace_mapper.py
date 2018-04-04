from dplaingestion.mappers.contentdm_oai_dc_mapper import CONTENTdm_OAI_Mapper
from dplaingestion.selector import getprop
import urllib


class CSU_DSpace_Mapper(CONTENTdm_OAI_Mapper):
    '''A mapper for multi-campus CSU DSpace METS feed
       In registry, make sure "metadataprefix=mets" in Harvest Endpoint/Extra Data
    '''

    def get_handle(self):
        '''Return DSpace handle.net-type numerical values representing collection & object
        '''
        objectID = getprop(self.provider_data_source, 'identifier')
        for d in objectID:
            if "hdl.handle.net" in d:
                handle = d.replace('http://hdl.handle.net/', '')
        return handle

    def map_is_shown_by(self):
        '''Take handle from ID field, take first original filename & URL encode it, concatenate to single URL
        '''
        handle = self.get_handle()
        fNameOrig = getprop(self.provider_data_source, 'originalName')
        for f in fNameOrig:
            # don't take .txt, .doc, .tiff
            if not any(x in f.lower() for x in [".txt", ".doc", ".tif"]):
                fNameEncode = urllib.quote(f)
                if '.pdf' in f.lower():
                    # get small thumb for PDF text objects
                    thumbnail_url = ''.join(
                        ('http://dspace.calstate.edu/bitstream/handle/',
                         handle, '/', fNameEncode, '.jpg'))
                    self.mapped_data.update({'isShownBy': thumbnail_url})
                elif ".wav" in f.lower() or ".mp4" in f.lower():
                    # don't get thumbs for AV objects
                    pass
                else:
                    # get larger preview for image objects
                    thumbnail_url = ''.join(
                        ('http://dspace.calstate.edu/bitstream/handle/',
                         handle, '/', fNameEncode))
                    self.mapped_data.update({'isShownBy': thumbnail_url})

    def map_is_shown_at(self):
        '''Take handle from ID field to construct record link
        '''
        handle = self.get_handle()
        if handle:
            record_link = ''.join(
                ('http://dspace.calstate.edu/handle/', handle))
            self.mapped_data.update({'isShownAt': record_link})

    def map_language(self):
        self.source_resource_orig_to_prop("languageTerm", "language")

    def map_subject(self):
        self.source_resource_orig_to_prop("topic", "subject")

    def map_date(self):
        self.source_resource_orig_to_prop("dateIssued", "date")

    def map_creator(self):
        self.source_resource_orig_to_prop("namePart", "creator")

    def map_type(self):
        #Take type from file MIME type since descriptive type/genre
        #values don't fit DCMI type vocab
        self.source_resource_orig_to_prop("formatName", "type")
        #fields = ("type", "genre")
        #self.source_resource_orig_list_to_prop(fields, 'type')
