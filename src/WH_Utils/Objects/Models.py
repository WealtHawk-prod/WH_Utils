"""
This is an extremly powerful module for interacting with, creating, and modifying and object we
deal with on a continual basis. This includes: Users, Clients, Companies, and Events. The idea is
that you will be able to create, pull or construct a new object simply by the way you interact with
the __init__ methods.

For example, to pull a client from the database you might invoke it like this:

```
client = Client(WH_ID = "random_letters", auth_dict = auth_header)
```

While if you wanted to construct a client you could pass a data dict in or even pass
a coresignal_id or linkedin_url instead:

```
client = Client(linkedin_url = "https://linkedin.com/mcclain-thiel", auth_dict = coresignal_auth)
```

Similarly, if you want to push this back to the daatbase, the class will know if this is a POST or PUT request and
handle everything accordingly.

Additionally, I've added some nice to have debugging features. All these classes are based on the new "Dataclass"
structure which provides some cool features like pretty printing and automatic hashing. So these classes all
have fancy printing functions and are all set for hashing stuff.

Previously some of this was handled by the pydantic version called Baseclass. I reworked that
because I wanted to use the inheritance for other stuff and I don't know how MI works in python.


"""
from datetime import datetime, date
from typing import Any, Optional, Union, List

from pydantic import Json, HttpUrl

from src.WH_Utils.Objects.Enums import UserRank, EventType, CompanyType
from src.WH_Utils.Objects.Object_utils import verify_json, verify_auth_header


from dataclasses import dataclass


@dataclass
class User:
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    other_info: Optional[Any]
    rank: Optional[UserRank]
    firebase_id: Optional[str]
    created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, WH_ID: str = None, auth_header: dict = None, data_dict = None):
        """
        verify combonation of variables and call the right function with the right params.

        """

        return

    def _build_from_WH_db(self, WH_ID: str, auth_header: dict) -> None:
        return

    def _build_from_data_dict(self, data: dict) -> None:
        verify_json("user", data)
        return

    def send_to_db(self, auth_header: dict) -> None:
        return

    def __repr__(self) -> str:
        return "UserID: {} \n Name: {},{}\n Email: {}, \n, Rank: {}".format(self.id, self.last_name, self.first_name, self.email, self.rank)

    def __str__(self) -> str:
        return "UserID: {} \n Name: {},{}\n Email: {}, \n, Rank: {}".format(self.id, self.last_name, self.first_name, self.email, self.rank)


@dataclass
class Client:
    id: Optional[str]
    name: Optional[str]
    location: Optional[str]
    coresignal_id: Optional[int]
    linkedin_url: Optional[HttpUrl]
    picture: Optional[HttpUrl]
    event_type: Optional[EventType]
    company: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    full_data: Optional[Any]
    analytics: Optional[Any]
    date_created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, WH_ID: str = None, auth_header: dict = None, data_dict = None):
        """
        verify combonation of variables and call the right function with the right params.

        """

        return

    def _build_from_WH_db(self, WH_ID: str, auth_header: dict) -> None:
        return

    def _build_from_data_dict(self, data: dict):
        verify_json("client", data)
        return

    def _build_from_coresignal(self, coresignal_id: Optional[int], linkedin_url: Optional[HttpUrl], auth_header: dict) -> None:
        return

    def send_to_db(self, auth_header: dict) -> None:
        return

    def __repr__(self) -> str:
        return "ClientID: {} \n Name: {} \n Location: {}".format(self.id, self.name, self.location)

    def __str__(self) -> str:
        return "ClientID: {} \n Name: {} \n Location: {}".format(self.id, self.name, self.location)

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

    def __init__(self, WH_ID: str = None, auth_header: dict = None, data_dict = None):
        """
        verify combonation of variables and call the right function with the right params.

        """

        return

    def _build_from_WH_db(self, WH_ID: str, auth_header: dict) -> None:
        return

    def _build_from_data_dict(self, data: dict) -> None:
        verify_json("client", data)
        return

    def _build_from_coresignal(self, coresignal_id: Optional[int], linkedin_url: Optional[HttpUrl], auth_header: dict) -> None:
        return

    def send_to_db(self, auth_header: dict) -> None:
        return

    def __repr__(self) -> str:
        return "CompanyID: {} \n Name: {}".format(self.id, self.name)

    def __str__(self) -> str:
        return "CompanyID: {} \n Name: {}".format(self.id, self.name)


@dataclass
class Event:
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    type: Optional[EventType]
    date_of: Optional[date]
    link: Optional[HttpUrl]
    industry: Optional[str]
    location: Optional[str]
    value: Optional[int]
    other_info: Optional[Any]
    created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, WH_ID: str = None, auth_header: dict = None, data_dict = None):
        """
        verify combonation of variables and call the right function with the right params.

        """

        return

    def _build_from_WH_db(self, WH_ID: str, auth_header: dict) -> None:
        return

    def _build_from_data_dict(self, data: dict) -> None:
        verify_json("client", data)
        return

    def _build_from_coresignal(self, coresignal_id: Optional[int], linkedin_url: Optional[HttpUrl], auth_header: dict) -> None:
        return

    def send_to_db(self, auth_header: dict) -> None:
        return


    def __repr__(self) -> str:
        return "EventID: {} \n Title: {}".format(self.id, self.title)

    def __str__(self) -> str:
        return "EventID: {} \n Title: {}".format(self.id, self.title)

@dataclass
class SignupSchema:
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    location: Optional[str]
    picture: Optional[str]
    password: Optional[str]
    company: Optional[str]
    rank: Optional[str]

@dataclass
class AddTaskSchema:
    title: Optional[str]
    content: Optional[Json]
    email: Optional[str]
