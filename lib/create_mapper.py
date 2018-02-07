def create_mapper(mapper_type, data):
    """
    Given a mapper_type, creates imports and instanstiates the appropriate
    Mapper class with the given data.
    """

    def _create_pymarc_mapper(data):
        from dplaingestion.mappers.marc_mapper import PyMARCMapper
        return PyMARCMapper(data)

    def _create_dublin_core_mapper(data):
        from dplaingestion.mappers.dublin_core_mapper import DublinCoreMapper
        return DublinCoreMapper(data)

    def _create_bpl_mapper(data):
        from dplaingestion.mappers.bpl_mapper import BPLMapper
        return BPLMapper(data)

    def _create_uva_mapper(data):
        from dplaingestion.mappers.uva_mapper import UVAMapper
        return UVAMapper(data)

    def _create_mdl_mapper(data):
        from dplaingestion.mappers.mdl_mapper import MDLMapper
        return MDLMapper(data)

    def _create_cdl_json_mapper(data):
        from dplaingestion.mappers.cdl_json_mapper import CDLJSONMapper
        return CDLJSONMapper(data)

    def _create_mapv3_json_mapper(data):
        from dplaingestion.mappers.mapv3_json_mapper import MAPV3JSONMapper
        return MAPV3JSONMapper(data)

    def _create_mdl_json_mapper(data):
        from dplaingestion.mappers.mdl_json_mapper import MDLJSONMapper
        return MDLJSONMapper(data)

    def _create_gpo_mapper(data):
        from dplaingestion.mappers.gpo_mapper import GPOMapper
        return GPOMapper(data)

    def _create_scdl_mapper(data):
        from dplaingestion.mappers.scdl_mapper import SCDLMapper
        return SCDLMapper(data)

    def _create_edan_mapper(data):
        from dplaingestion.mappers.edan_mapper import EDANMapper
        return EDANMapper(data)

    def _create_nara_mapper(data):
        from dplaingestion.mappers.nara_mapper import NARAMapper
        return NARAMapper(data)

    def _create_nypl_mapper(data):
        from dplaingestion.mappers.nypl_mapper import NYPLMapper
        return NYPLMapper(data)

    def _create_untl_mapper(data):
        from dplaingestion.mappers.untl_mapper import UNTLMapper
        return UNTLMapper(data)

    def _create_missouri_mapper(data):
        from dplaingestion.mappers.missouri_mapper import MissouriMapper
        return MissouriMapper(data)

    def _create_lapl_marc_mapper(data):
        from dplaingestion.mappers.lapl_marc_mapper import LAPLMARCMapper
        return LAPLMARCMapper(data)

    def _create_ucla_solr_dc_mapper(data):
        from dplaingestion.mappers.ucla_solr_dc_mapper import UCLASolrDCMapper
        return UCLASolrDCMapper(data)

    def _create_sfpl_marc_mapper(data):
        from dplaingestion.mappers.sfpl_marc_mapper import SFPLMARCMapper
        return SFPLMARCMapper(data)

    def _create_csl_marc_mapper(data):
        from dplaingestion.mappers.csl_marc_mapper import CSLMARCMapper
        return CSLMARCMapper(data)

    def _create_pspl_marc_mapper(data):
        from dplaingestion.mappers.pspl_oai_dc_mapper import PSPL_OAIMapper
        return PSPL_OAIMapper(data)

    def _create_ucldc_nuxeo_dc_mapper(data):
        from dplaingestion.mappers.ucldc_nuxeo_dc_mapper import \
                UCLDCNuxeoMapper
        return UCLDCNuxeoMapper(data)

    def _create_ucldc_nuxeo_mapper(data):
        from dplaingestion.mappers.ucldc_nuxeo_mapper import UCLDCNuxeoMapper
        return UCLDCNuxeoMapper(data)

    def _create_ucsd_blacklight_dc_mapper(data):
        from dplaingestion.mappers.ucsd_blacklight_dc_mapper import \
                UCSDBlacklightDCMapper
        return UCSDBlacklightDCMapper(data)

    def _create_oac_dc_mapper(data):
        from dplaingestion.mappers.oac_dc_mapper import OAC_DCMapper
        return OAC_DCMapper(data)

    def _create_oac_dc_mapper_suppress_desc_2(data):
        from dplaingestion.mappers.oac_dc_mapper_suppress_description_2 \
            import OAC_DCMapperSuppressDescription2
        return OAC_DCMapperSuppressDescription2(data)

    def _create_ucsf_xml_mapper(data):
        from dplaingestion.mappers.ucsf_xml_mapper import UCSFXMLFeedMapper
        return UCSFXMLFeedMapper(data)

    def _create_ucsf_solr_mapper(data):
        from dplaingestion.mappers.ucsf_solr_mapper import UCSFSolrFeedMapper
        return UCSFSolrFeedMapper(data)

    def _create_ucsb_aleph_mapper(data):
        from dplaingestion.mappers.ucsb_aleph_marc import UCSBAlephMarcMapper
        return UCSBAlephMarcMapper(data)

    def _create_oac_dc_mapper_suppress_publisher(data):
        from dplaingestion.mappers.oac_dc_mapper_suppress_publisher import \
                OAC_DCMapperSuppressPublisher
        return OAC_DCMapperSuppressPublisher(data)

    def _create_lmu_oai_dc_mapper(data):
        from dplaingestion.mappers.lmu_oai_dc import LMU_OAI_Mapper
        return LMU_OAI_Mapper(data)

    def _create_contentdm_oai_dc_mapper(data):
        from dplaingestion.mappers.contentdm_oai_dc_mapper import \
                CONTENTdm_OAI_Mapper
        return CONTENTdm_OAI_Mapper(data)

    def _create_cavpp_contentdm_oai_dc_mapper(data):
        from dplaingestion.mappers.cavpp_contentdm_oai_dc_mapper import \
                CAVPP_CONTENTdm_OAI_Mapper
        return CAVPP_CONTENTdm_OAI_Mapper(data)

    def _create_csudh_contentdm_oai_dc_mapper(data):
        from dplaingestion.mappers.csudh_contentdm_oai_dc_mapper import \
                CSUDH_CONTENTdm_OAI_Mapper
        return CSUDH_CONTENTdm_OAI_Mapper(data)

    def _create_chula_vista_pl_contentdm_oai_dc_mapper(data):
        from dplaingestion.mappers.chula_vista_pl_contentdm_oai_dc_mapper \
                import CVPL_CONTENTdm_OAI_Mapper
        return CVPL_CONTENTdm_OAI_Mapper(data)

    def _create_chapman_oai_dc(data):
        from dplaingestion.mappers.chapman_oai_mapper import Chapman_OAI_Mapper
        return Chapman_OAI_Mapper(data)

    def _create_contentdm_oai_dc_mapper_suppress_description(data):
        from dplaingestion.mappers. \
                contentdm_oai_dc_mapper_suppress_description \
                import CONTENTdm_OAI_Suppress_Description_Mapper
        return CONTENTdm_OAI_Suppress_Description_Mapper(data)

    def _create_vault_oai_dc_mapper(data):
        from dplaingestion.mappers.cca_vault_oai_dc_mapper import \
                CCA_VaultOAIMapper
        return CCA_VaultOAIMapper(data)

    def _create_cmis_atom_dc_mapper(data):
        from dplaingestion.mappers.cmis_atom_mapper import CMISAtomDCMapper
        return CMISAtomDCMapper(data)

    def _create_califa_oai_dc_mapper(data):
        from dplaingestion.mappers.califa_oai_dc_mapper import Califa_OAIMapper
        return Califa_OAIMapper(data)

    def _create_csa_omeka_mapper(data):
        from dplaingestion.mappers.csa_omeka_mapper import CSA_OAIMapper
        return CSA_OAIMapper(data)

    def _create_mpd_omeka_mapper(data):
        from dplaingestion.mappers.mpd_omeka_mapper import MPD_OAIMapper
        return MPD_OAIMapper(data)

    def _create_ucb_blacklight_dc_mapper(data):
        from dplaingestion.mappers.ucb_blacklight_dc_mapper import \
            UCBBlacklightDCMapper
        return UCBBlacklightDCMapper(data)

    def _create_cabrillo_mapper(data):
        from dplaingestion.mappers.cabrillo_suppress_description import \
            Cabrillo_suppress_description
        return Cabrillo_suppress_description(data)

    def _create_contentdm_oai_dc_mapper_get_sound_thumbs(data):
        from dplaingestion.mappers.contentdm_oai_dc_mapper_get_sound_thumbs \
            import CONTENTdm_OAI_Mapper_get_sound_thumbs
        return CONTENTdm_OAI_Mapper_get_sound_thumbs(data)

    def _create_islandora_mapper(data):
        from dplaingestion.mappers.islandora_oai_dc_mapper import Islandora_OAIMapper
        return Islandora_OAIMapper(data)

    def _create_chico_mapper(data):
        from dplaingestion.mappers.chico_oai_mapper import Chico_OAI_Mapper
        return Chico_OAI_Mapper(data)

    def _create_up_mapper(data):
        from dplaingestion.mappers.up_oai_mapper import UP_OAI_Mapper
        return UP_OAI_Mapper(data)

    def _create_csu_sac_mapper(data):
        from dplaingestion.mappers.csu_sac_oai_mapper import CSU_Sac_OAI_Mapper
        return CSU_Sac_OAI_Mapper(data)

    def _create_black_gold_mapper(data):
        from dplaingestion.mappers.black_gold_mapper import BlackGold_OAIMapper
        return BlackGold_OAIMapper(data)

    def _create_ucb_bampfa_mapper(data):
        from dplaingestion.mappers.ucb_bampfa_solr_mapper import UCB_BAMPFA_Mapper
        return UCB_BAMPFA_Mapper(data)

    def _create_calpoly_mapper(data):
        from dplaingestion.mappers.calpoly_oai_dc_mapper import CalPoly_OAIMapper
        return CalPoly_OAIMapper(data)

    def _create_flickr_api_mapper(data):
        from dplaingestion.mappers.flickr_api_mapper import FlickrMapper
        return FlickrMapper(data)

    def _create_youtube_video_snippet_api_mapper(data):
        from dplaingestion.mappers.youtube_video_snippet_mapper import YouTubeVideoSnippetMapper
        return YouTubeVideoSnippetMapper(data)

    def _create_chs_islandora_mapper(data):
        from dplaingestion.mappers.chs_islandora_mapper import CHS_Islandora_Mapper
        return CHS_Islandora_Mapper(data)

    def _create_csu_ci_mapper(data):
        from dplaingestion.mappers.csu_ci_mets_mapper import CSU_CI_METS_Mapper
        return CSU_CI_METS_Mapper(data)

    def _create_caltech_maccready_mapper(data):
        from dplaingestion.mappers.caltech_maccready_mapper import CalTech_MacCready_Mapper
        return CalTech_MacCready_Mapper(data)

    def _create_sacramento_xml_mapper(data):
        from dplaingestion.mappers.sacramento_xml_mapper import SacramentoXMLMapper
        return SacramentoXMLMapper(data)

    def _create_lapl_oai_mapper(data):
        from dplaingestion.mappers.lapl_oai_mapper import LAPL_OAIMapper
        return LAPL_OAIMapper(data)

    def _create_yosemite_oai_mapper(data):
        from dplaingestion.mappers.yosemite_oai_mapper import Yosemite_OAIMapper
        return Yosemite_OAIMapper(data)

    def _create_emuseum_xml_mapper(data):
        from dplaingestion.mappers.emuseum_xml_mapper import eMuseumXMLMapper
        return eMuseumXMLMapper(data)

    def _create_uci_didl_mapper(data):
        from dplaingestion.mappers.uci_didl_mapper import UCI_DIDL_Mapper
        return UCI_DIDL_Mapper(data)

    mappers = {
        'marc': lambda d: _create_pymarc_mapper(d),
        'dublin_core': lambda d: _create_dublin_core_mapper(d),
        'lapl_marc': lambda d: _create_lapl_marc_mapper(d),
        'sfpl_marc': lambda d: _create_sfpl_marc_mapper(d),
        'csl_marc': lambda d: _create_csl_marc_mapper(d),
        'pspl_oai_dc': lambda d: _create_pspl_marc_mapper(d),
        'ucla_solr_dc': lambda d: _create_ucla_solr_dc_mapper(d),
        'ucldc_nuxeo_dc': lambda d: _create_ucldc_nuxeo_mapper(d),
        'ucldc_nuxeo': lambda d: _create_ucldc_nuxeo_mapper(d),
        'ucsd_blacklight_dc': lambda d: _create_ucsd_blacklight_dc_mapper(d),
        'oac_dc': lambda d: _create_oac_dc_mapper(d),
        'oac_dc_suppress_desc_2':
            lambda d: _create_oac_dc_mapper_suppress_desc_2(d),
        'oac_dc_suppress_publisher':
            lambda d: _create_oac_dc_mapper_suppress_publisher(d),
        'ucsf_xml': lambda d: _create_ucsf_xml_mapper(d),
        'ucsf_solr': lambda d: _create_ucsf_solr_mapper(d),
        'ucsb_aleph_marc': lambda d: _create_ucsb_aleph_mapper(d),
        'missouri': lambda d: _create_missouri_mapper(d),
        'mapv3_json': lambda d: _create_mapv3_json_mapper(d),
        'mdl_json': lambda d: _create_mdl_json_mapper(d),
        'cdl_json': lambda d: _create_cdl_json_mapper(d),
        'contentdm_oai_dc': lambda d: _create_contentdm_oai_dc_mapper(d),
        'cavpp_contentdm_oai_dc':
            lambda d: _create_cavpp_contentdm_oai_dc_mapper(d),
        'csudh_contentdm_oai_dc':
            lambda d: _create_csudh_contentdm_oai_dc_mapper(d),
        'chula_vista_pl_contentdm_oai_dc':
            lambda d: _create_chula_vista_pl_contentdm_oai_dc_mapper(d),
        'lmu_oai_dc': lambda d: _create_lmu_oai_dc_mapper(d),
        'contentdm_oai_dc_suppress_description':
            lambda d: _create_contentdm_oai_dc_mapper_suppress_description(d),
        'chapman_oai_dc': lambda d: _create_chapman_oai_dc(d),
        'cca_vault_oai_dc': lambda d: _create_vault_oai_dc_mapper(d),
        'califa_oai_dc': lambda d: _create_califa_oai_dc_mapper(d),
        'csa_omeka': lambda d: _create_csa_omeka_mapper(d),
        'mpd_omeka': lambda d: _create_mpd_omeka_mapper(d),
        'ucb_blacklight': lambda d: _create_ucb_blacklight_dc_mapper(d),
        'cmis_atom': lambda d: _create_cmis_atom_dc_mapper(d),
        'cabrillo_suppress_description': lambda d: _create_cabrillo_mapper(d),
        'contentdm_oai_dc_get_sound_thumbs': lambda d: _create_contentdm_oai_dc_mapper_get_sound_thumbs(d),
        'islandora_oai_dc': lambda d: _create_islandora_mapper(d),
        'chico_oai_dc': lambda d: _create_chico_mapper(d),
        'up_oai_dc': lambda d: _create_up_mapper(d),
        'csu_sac_oai_dc': lambda d: _create_csu_sac_mapper(d),
        'black_gold_oai': lambda d: _create_black_gold_mapper(d),
        'ucb_bampfa_solr': lambda d: _create_ucb_bampfa_mapper(d),
        'calpoly_oai_dc': lambda d: _create_calpoly_mapper(d),
        'flickr_api': lambda d: _create_flickr_api_mapper(d),
        'youtube_video_snippet': lambda d: _create_youtube_video_snippet_api_mapper(d),
        'chs_islandora': lambda d: _create_chs_islandora_mapper(d),
        'csu_ci_mets': lambda d: _create_csu_ci_mapper(d),
        'caltech_maccready': lambda d: _create_caltech_maccready_mapper(d),
        'sacramento_xml': lambda d: _create_sacramento_xml_mapper(d),
        'lapl_oai_dc': lambda d: _create_lapl_oai_mapper(d),
        'yosemite_oai_dc': lambda d: _create_yosemite_oai_mapper(d),
        'emuseum_xml': lambda d: _create_emuseum_xml_mapper(d),
        'uci_didl': lambda d: _create_uci_didl_mapper(d),
    }

    return mappers.get(mapper_type)(data)
