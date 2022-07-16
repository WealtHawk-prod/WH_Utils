from typing import Any, Optional, Union, List, Dict, Any
import requests
import uuid
import json
from datetime import datetime, timedelta
from pydantic import Json, HttpUrl, BaseModel

from WH_Utils.Objects.Enums import UserRank, OrgRank
from WH_Utils.Objects.Object_utils import (
    verify_json,
    verify_auth_header,
    minus_key,
    WH_DB_URL,
)


class User(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    email: str
    other_info: Optional[dict]
    firebase_id: str
    stripe_id: str
    location: Optional[str]
    created: Optional[datetime]
    last_modified: Optional[datetime]
    in_database: bool = False
    rank: UserRank = UserRank.USER_NEW
    organization_rank: OrgRank = OrgRank.USER

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    @staticmethod
    def from_db(WH_ID: str, auth_header: Dict[str, Any]):
        verify_auth_header(auth_header)
        request = requests.get(
            WH_DB_URL + "/user", params={"userID": WH_ID}, headers=auth_header
        )
        content = request.json()[0]
        if "detail" in list(content.keys()) and content["detail"] == "User Not Found":
            raise ValueError("User Not Found or bad auth")

        return User(**content)

    def send_to_db(self, auth_header: Dict[str, Any]) -> requests.Response:
        """
        Sends the current object to the WH Database

        It will try to figure out if the object is already in the database by looking at the initialization
        method by looking at the `in_database` attribute. For example, if you constructed the object using
        WH_auth credentials and a WH_ID, then obviously the object is in the DB and so the function will
        attempt a PUT request to update the user. If 'in_database' is `False` then it will attempt a `POST`
        request. It's python so its mutable obviously so change it if needed.

        Args
        ------

            auth_header: Dict[str, Any]
                the authorization header for the WH database. It should be a dict with at least the key
                'Authorization' where the value is the key generated by logging in

        Returns
        ---------
            response: requests.Response
                the response of the backend API to your request. If it was a sucessful ``POST`` request it will look like:

                    ``>>> exampleClient.send_to_db(WH_auth_dict).content.decode()``

                    ``Not expecting client in database. Attempting Post request.``

                    ``'{"id":"1fd84bd0-779d-4a10-8c71-e2cf008d23ed"}'``

                But a successful ``PUT`` request will look like:



        """
        data = self.__dict__
        data = minus_key("in_database", data)
        url = "https://db.wealthawk.com/user"
        data["other_info"] = json.dumps(self.other_info)

        if self.in_database:
            response = requests.put(url, json=data, headers=auth_header)
        else:
            response = requests.post(url, json=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content)

        return response

    def __repr__(self) -> str:
        return "UserID: {} \n Name: {}, {}\n Email: {}, \n Rank: {}".format(
            self.id, self.last_name, self.first_name, self.email, self.rank
        )

    def __str__(self) -> str:
        return "UserID: {} \n Name: {}, {}\n Email: {}, \n Rank: {}".format(
            self.id, self.last_name, self.first_name, self.email, self.rank
        )
