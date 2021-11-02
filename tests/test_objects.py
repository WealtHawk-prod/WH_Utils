import pytest

import os
import sys
import json
#sys.path.insert(0, os.path.abspath('src'))

import WH_Utils.Objects.Enums as WH_Enums
import WH_Utils.Objects.Models as WH_Models

with open("test_data/auth.json", 'r') as f:
    auth_data = json.load(f)

auth_dict = {
    "accept": 'application/json',
    "Authorization": auth_data['API_KEY']
}


class TestEnums:

    def test_user_enum_valid(self):
        s = WH_Enums.UserRank("user")
        assert isinstance(s, WH_Enums.UserRank)

    def test_user_enum_invalid(self):
        with pytest.raises(ValueError):
            s = WH_Enums.UserRank("not a rank")


class TestModels:

    def test_user_valid_json(self):
        with open("test_data/user.json", 'r') as f:
            data = json.load(f)
        user = WH_Models.User(data_dict=data)
        assert isinstance(user, WH_Models.User)


    def test_user_invalid_json(self):
        assert True

    def test_user_from_db(self):
        user = WH_Models.User(WH_ID="6091f72d-9b4c-4af9-9b25-e75811a2667e", auth_header=auth_dict)
        assert isinstance(user, WH_Models.User)

