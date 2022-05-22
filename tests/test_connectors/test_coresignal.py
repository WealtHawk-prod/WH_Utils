from WH_Utils import Prospect, Company
from WH_Utils.Connectors.Coresignal import coresignal_to_company, coresingal_to_prospect
from WH_Utils.Utils.test_utils import CS_auth_dict


class TestCoresignalConnectors:
    prospect_coresignal_id = "64362271" #mcclain
    company_coresignal_id = "33158580" #wealthawk

    def test_prospect(self):
        cs_prospect = coresingal_to_prospect(id=TestCoresignalConnectors.prospect_coresignal_id, auth_dict=CS_auth_dict, company_id=TestCoresignalConnectors.company_coresignal_id)
        assert isinstance(cs_prospect, Prospect)

    def test_company(self):
        cs_company = coresignal_to_company(id=TestCoresignalConnectors.company_coresignal_id, auth_dict=CS_auth_dict)
        assert isinstance(cs_company, Company)