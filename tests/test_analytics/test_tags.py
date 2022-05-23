from WH_Utils import Prospect, Event
from WH_Utils.Analytics.Prospects import get_prospect_tags
#from WH_Utils.Analytics.Events import get_event_stage

import json
from datetime import datetime, date

class TestTags:
    def test_prospect_tags(self):
        with open("tests/test_data/objects_data/prospect_data_dict.json", 'r') as f:
            data = json.load(f)
        prospect = Prospect(data_dict=data)
        tag_dict = get_prospect_tags(prospect, company_id=4368043, event_date=date(2017, 10, 12))

        expected_keys = ['title', 'employee_rank', 'languages_spoken', 'age', 'joined_pre_exit', 'days_at_company_preexist']
        actual_keys = list(tag_dict.keys())
        assert expected_keys == actual_keys, f"Unexpected keys. Expected: {expected_keys}, Actual: {actual_keys}"


