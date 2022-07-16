"""
Description of Event Class
"""

from datetime import datetime, date
from typing import Any, Optional, Dict
import requests
import uuid
import json

from pydantic import HttpUrl, BaseModel, Json

from WH_Utils.Objects.Enums import EventType
from WH_Utils.Objects.Object_utils import (
    verify_auth_header,
    minus_key,
    WH_DB_URL,
)


class Event(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    title: str
    description: str
    type: EventType
    date_of: date
    link: Optional[HttpUrl]
    industry: Optional[str]
    location: Optional[str]
    value: Optional[int] = 0
    other_info: dict = {}
    created: Optional[datetime] = datetime.now()
    last_modified: Optional[datetime] = datetime.now()
    in_database: bool = False

    def __repr__(self) -> str:
        return "EventID: {} \n Title: {}".format(self.id, self.title)

    def __str__(self) -> str:
        return "EventID: {} \n Title: {}".format(self.id, self.title)

    @staticmethod
    def from_db(WH_ID: str, auth_header: Dict[str, Any]):
        verify_auth_header(auth_header)
        request = requests.get(
            WH_DB_URL + "/event", params={"eventID": WH_ID}, headers=auth_header
        )
        content = request.json()

        if isinstance(content['date_of'], str):
            content['date_of'] = datetime.strptime(content['date_of'], "%Y-%m-%d").date()

        return Event(**content)


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
        url = "https://db.wealthawk.com/event"
        data["other_info"] = json.dumps(data["other_info"])
        data["date_of"] = str(self.date_of)
        data["created"] = None
        data["last_modified"] = None

        if self.in_database:
            response = requests.put(url, json=data, headers=auth_header)
        else:
            response = requests.post(url, json=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content.decode())

        return response


