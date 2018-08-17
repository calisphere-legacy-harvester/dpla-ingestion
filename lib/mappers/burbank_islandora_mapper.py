# -*- coding: utf-8 -*-
from dplaingestion.mappers.islandora_oai_dc_mapper import Islandora_OAIMapper
from dplaingestion.selector import exists, getprop
import re

date_reg_exp = re.compile('(\d+[-/]\d+[-/]\d+)')

class Burbank_Islandora_Mapper(Islandora_OAIMapper):
    '''Do not write dates in YYYY-MM-DD format to sourceResource,
    as they are dates digitized/captured, not created'''

    def map_date(self):
        fields = ("available", "created", "date", "dateAccepted",
                  "dateCopyrighted", "dateSubmitted", "issued",
                  "modified", "valid")
        values = []
        for field in fields:
            field = field if not self.prefix else ''.join(
                    (self.prefix, field))
            if exists(self.provider_data_source['originalRecord'], field):
                # Need to check if string or not
                prop_val = getprop(self.provider_data_source['originalRecord'], field)
                for d in prop_val:
                    # filter out YYYY-MM-DD type dates
                    fulldate = date_reg_exp.findall(d)
                    if not fulldate:
                        values.append(d)
        if values:
            self.update_source_resource({'date': values})
