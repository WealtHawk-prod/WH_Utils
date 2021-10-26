import pytest

import os
import sys
sys.path.insert(0, os.path.abspath('src'))

import WH_Utils.Objects.Enums as WH_Enums


class TestEnums:

    def test_user_enum_valid(self):
        s = WH_Enums.UserRank("user")
        assert isinstance(s, WH_Enums.UserRank)

    def test_user_enum_invalid(self):
        with pytest.raises(ValueError):
            s = WH_Enums.UserRank("not a rank")
