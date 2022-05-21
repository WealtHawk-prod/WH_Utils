"""
Description of Company class
"""

from typing import Any, Optional, Union, List, Dict, Any
import requests
import uuid
import json
from datetime import datetime, timedelta

from pydantic import Json, HttpUrl

from WH_Utils.Objects.Enums import CompanyType
from WH_Utils.Objects.Object_utils import (
    verify_json,
    verify_auth_header,
    minus_key,
    WH_DB_URL,
)

from dataclasses import dataclass


@dataclass
class Company:
    id: Optional[str]
    name: Optional[str]
    coresignal_id: Optional[int]
    linkedin_url: Optional[HttpUrl]
    industry: Optional[str]
    description: Optional[str]
    location: Optional[str]
    logo: Optional[HttpUrl]
    type: Optional[CompanyType]
    website: Optional[HttpUrl]
    created: Optional[datetime]
    last_modified: Optional[datetime]
    full_data: Optional[Any]

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        WH_ID: Optional[str] = None,
        auth_header: Optional[Dict[str, Any]] = None,
        data_dict: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        verify combination of variables and call the right function with the right params.

        """
        if WH_ID and auth_header:
            self._build_from_WH_db(WH_ID, auth_header)
        elif data_dict:
            self._build_from_data_dict(data_dict)
        else:
            raise ValueError("Invalid combination of init parameters")

    def _build_from_WH_db(self, WH_ID: str, auth_header: Dict[str, Any]) -> None:
        verify_auth_header(auth_header)
        request = requests.get(
            WH_DB_URL + "/company", params={"companyID": WH_ID}, headers=auth_header
        )
        content = request.json()

        for key in list(content.keys()):
            self.__dict__[key] = content[key]

        if not self.full_data or self.full_data == '"null"':
            self.full_data = {}

        self.in_database = True

    def _build_from_data_dict(self, data: Dict[str, Any]) -> None:
        verify_json("company", data)
        for key in list(data.keys()):
            self.__dict__[key] = data[key]

        if not self.id:
            self.id = str(uuid.uuid4())

        if not self.full_data:
            self.full_data = {}

        self.in_database = False

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
                the response of the backend API to your request. If it was a sucessful POST request it will look like:
                >>> exampleClient.send_to_db(WH_auth_dict).content.decode()
                Not expecting client in database. Attempting Post request.
                '{"id":"1fd84bd0-779d-4a10-8c71-e2cf008d23ed"}'

        """
        data = self.__dict__
        data = minus_key("in_database", data)
        url = WH_DB_URL + "/company"
        data["full_data"] = json.dumps(data["full_data"])

        if self.in_database:
            response = requests.put(url, json=data, headers=auth_header)
        else:
            response = requests.post(url, json=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content.decode())

        return response

    def __repr__(self) -> str:
        return "CompanyID: {} \n Name: {}".format(self.id, self.name)

    def __str__(self) -> str:
        return "CompanyID: {} \n Name: {}".format(self.id, self.name)
