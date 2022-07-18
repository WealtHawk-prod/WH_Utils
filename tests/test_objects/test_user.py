import json
from WH_Utils.Objects.User import User
from WH_Utils.Utils.test_utils import WH_auth_dict, BASE_URL
import requests

import os

script_path = os.path.realpath(__file__)
parent_path = os.path.dirname(script_path)
json_path = os.path.join(os.path.sep, parent_path, "../test_data/objects_data", "user.json")


class TestUser:

    def test_user_valid_json(self):
        with open(json_path, 'r') as f:
            data = json.load(f)
        user = User(**data)
        assert isinstance(user, User)

    def test_user_invalid_json(self):
        assert True

    def test_user_from_db(self):
        user = User.from_db(WH_ID="6091f72d-9b4c-4af9-9b25-e75811a2667e", auth_header=WH_auth_dict)
        assert isinstance(user, User)

    def test_push_to_db(self):
        with open(json_path, 'r') as f:
            data = json.load(f)
        user = User(**data)
        response = user.send_to_db(WH_auth_dict)

        # deleting users isnt really a route

        if response.status_code == 200:
            id = response.json()['id']
            # response2 = requests.delete(BASE_URL + "/user", params={'id': id})

        assert response.status_code == 200
