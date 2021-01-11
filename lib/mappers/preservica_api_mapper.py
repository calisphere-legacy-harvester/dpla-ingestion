# -*- coding: utf-8 -*-
from dplaingestion.mappers.mapper import Mapper


class PreservicaAPIMapper(Mapper):

    def __init__(self, provider_data):
        super(PreservicaAPIMapper, self).__init__(provider_data)

        self.dc_metadata = self.provider_data[
            "{http://www.openarchives.org/OAI/2.0/oai_dc/}dc"]
        preservica_id = self.provider_data.get('preservica_id', None)
        self.preservica_id = preservica_id.get('$', None)

    def map_is_shown_at(self):
        is_shown_at = "https://oakland.access.preservica.com/file/sdb:digitalFile%7C{}/".format(self.preservica_id)
        self.mapped_data.update({"isShownAt": is_shown_at})

    def map_is_shown_by(self):
        is_shown_by = "https://oakland.access.preservica.com/download/thumbnail/sdb:digitalFile%7C{}".format(self.preservica_id)
        self.mapped_data.update({"isShownBy": is_shown_by})

    def map_source_resource(self):
        self.mapped_data.get('sourceResource').update({'stateLocatedIn':'California'})

        DC_elements = ['contributor', 'coverage', 'creator', 'date',
                    'description', 'format', 'identifier', 'language',
                    'publisher', 'relation', 'rights', 'source', 'subject',
                    'title', 'type']

        for key in self.dc_metadata:
            if key in DC_elements:

                source_resource_fieldname = key
                value = self.dc_metadata[key]

                if isinstance(value, dict):
                    value = value.get('$', None)
                    if value:
                        if isinstance(value, int):
                            value = str(value)
                        value = [value]
                elif isinstance(value, list):
                    value_list = []
                    for d in value:
                        list_element = d.get('$', None)
                        if list_element:
                            if isinstance(list_element, int):
                                list_element = str(list_element, int)
                            value_list.append({'name': list_element})
                    value = value_list

                if key == 'coverage':
                    source_resource_fieldname = 'spatial'

                if not(key and value):
                    continue

                self.mapped_data.get('sourceResource')[source_resource_fieldname] = value
