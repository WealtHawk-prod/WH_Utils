import json
from WH_Utils.Objects.Prospect import Prospect
from WH_Utils.Utils.test_utils import WH_auth_dict, BASE_URL
import requests
import warnings

import os
script_path = os.path.realpath(__file__)
parent_path = os.path.dirname(script_path)
json_path = os.path.join(os.path.sep, parent_path, "../test_data/objects_data", "prospect_data_dict.json")

class TestProspect:

    def test_user_valid_json(self):
        with open(json_path, 'r') as f:
            data = json.load(f)
        prospect = Prospect(**data)
        assert isinstance(prospect, Prospect)

    def test_user_invalid_json(self):
        assert True

    def test_user_from_db(self):
        prospect_id="21e38609-11f9-42c1-b785-d8a6e78fc7ff"
        prospect = Prospect.from_db(WH_ID=prospect_id, auth_header=WH_auth_dict)
        assert isinstance(prospect, Prospect)

    def test_push_to_db(self):
        with open(json_path, 'r') as f:
            data = json.load(f)
        prospect = Prospect(**data)

        response = prospect.send_to_db(WH_auth_dict)

        if response.status_code == 200:
            id = response.json()['id']
            response2 = requests.delete(BASE_URL + "/person", params={'personID': id}, headers=WH_auth_dict)
            if response2.status_code != 200:
                print(response2.text)
                warnings.warn("Test Prospect Not deleted. ProspectID {} was added but there was a problem deleting. {}".format(id, response2.text))

        assert response.status_code == 200
