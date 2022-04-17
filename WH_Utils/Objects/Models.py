"""
This is an extremely powerful module for interacting with, creating, and modifying and object we
deal with on a continual basis. This includes: Users, Clients, Companies, and Events. The idea is
that you will be able to create, pull or construct a new object simply by the way you interact with
the ``__init__`` methods.

For example, to pull a client from the database you might invoke it like this:

``client = Client(WH_ID = "random_letters", auth_dict = auth_header)``

While if you wanted to construct a client you could pass a data dict in or even pass
a coresignal_id or linkedin_url instead:


``client = Client(linkedin_url = "https://linkedin.com/mcclain-thiel", auth_dict = coresignal_auth)``

Similarly, if you want to push this back to the datatbase, the class will know if this is a POST or PUT request and
handle everything accordingly. **NOTE: ** It does this by making an `in_database` parameter for every instance. This
is determined by how the object was created. Foe example if you initialize the object with parameters WH_ID and auth_dict,
then the object is pulled from the database and we theerefore know that it is already present in the WH DB so `in_database`
is set to `True` and calling `send_to_database()` on this object will result in a `PUT` request. Any other form of
initialization will assume that the model is not in the database and so will result in `POST` request. If you know
the object is in the database but the `in_database` attribute is false, you can change it which will in turn change
how the object is pushed to the DB.

Additionally, I've added some nice to have debugging features. All these classes are based on the new "Dataclass"
structure which provides some cool features like pretty printing and automatic hashing. So these classes all
have fancy printing functions and are all set for hashing stuff.

Previously some of this was handled by the pydantic version called Baseclass. I reworked that
because I wanted to use the inheritance for other stuff and I don't know how MI works in python.


"""
from datetime import datetime, date
from typing import Any, Optional, Union, List, Dict, Any
import requests
import uuid
import json

from pydantic import Json, HttpUrl

from WH_Utils.Objects.Enums import UserRank, EventType, CompanyType
from WH_Utils.Objects.Object_utils import verify_json, verify_auth_header, minus_key, linkedin_dates_to_ts, get_company_data
from WH_Utils.External import Coresignal


from dataclasses import dataclass

WH_DB_URL = "https://db.wealthawk.com"


@dataclass
class User:
    """
    Class attributes
        - id: Optional[str]
        - first_name: Optional[str]
        - last_name: Optional[str]
        - email: Optional[str]
        - other_info: Optional[Any]
        - rank: Optional[UserRank]
        - firebase_id: Optional[str]
        - created: Optional[datetime]
        - last_modified: Optional[datetime]


    Initialization function:
        This function allows several combinations of parameters tha behave differently.

        if only `data_dict` parameter is passed in:
            a `User` object will be constructed from the data passed in via the dictionary. The data dict must
            have the same keys as the object itself.

        if `WH_ID` and `auth_header` are passed in:
            this will cause the program to attempt to pull the user from the WH database. User with that UUID
            must already exist in the database and the credentials must be valid and properly formatted.

        All other combinations are invalid.

    Args
    -----
        WH_ID: Optional[str]
            the UUID of a user in the database

        auth_header: Optional[Dict[str, Any]]
            the authorization header for the WEALTHAWK database

        data_dict: Optional[Dict[str, Any]]
            data to construct a user from
    """

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

    def __init__(self,
                WH_ID: Optional[str] = None,
                auth_header: Optional[Dict[str, Any]] = None,
                data_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialization function for user

        This function allows several combinations of parameters tha behave differently.

        if only `data_dict` parameter is passed in:
            a `User` object will be constructed from the data passed in via the dictionary. The data dict must
            have the same keys as the object itself.

        if `WH_ID` and `auth_header` are passed in:
            this will cause the program to attempt to pull the user from the WH database. User with that UUID
            must already exist in the database and the credentials must be valid and properly formatted.

        All other combinations are invalid.

        Args
        -----
            WH_ID: Optional[str]
                the UUID of a user in the database

            auth_header: Optional[Dict[str, Any]]
                the authorization header for the WEALTHAWK database

            data_dict: Optional[Dict[str, Any]]
                data to construct a user from

        """
        if WH_ID and auth_header:
            self._build_from_WH_db(WH_ID, auth_header)
        elif data_dict:
            self._build_from_data_dict(data_dict)
        else:
            raise ValueError("Invalid combination of init parameters")


    def _build_from_WH_db(self, WH_ID: str, auth_header: Dict[str, Any]) -> None:
        verify_auth_header(auth_header)
        request = requests.get(WH_DB_URL + "/user", params={'userID': WH_ID}, headers=auth_header)
        content = request.json()[0]
        if "detail" in list(content.keys()) and content['detail'] == "User Not Found":
            raise ValueError("User Not Found or bad auth")

        for key in list(content.keys()):
            self.__dict__[key] = content[key]

        # this is a hacky fix for the fact that the api wont send empty JSON types it just sends "null" which
        # breaks the verification on push
        if not self.other_info:
            self.other_info = {}

        self.in_database = True


    def _build_from_data_dict(self, data: Dict[str, Any]) -> None:
        verify_json("user", data)
        for key in list(data.keys()):
            self.__dict__[key] = data[key]

        if not self.id:
            self.id = str(uuid.uuid4())

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
                the response of the backend API to your request. If it was a sucessful ``POST`` request it will look like:

                    ``>>> exampleClient.send_to_db(WH_auth_dict).content.decode()``

                    ``Not expecting client in database. Attempting Post request.``

                    ``'{"id":"1fd84bd0-779d-4a10-8c71-e2cf008d23ed"}'``

                But a successful ``PUT`` request will look like:



        """
        data = self.__dict__
        data = minus_key("in_database", data)
        url = "https://db.wealthawk.com/user"
        data['other_info'] = json.dumps(self.other_info)

        if self.in_database:
            response = requests.put(url, json = data, headers = auth_header)
        else:
            response = requests.post(url, json = data, headers = auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content)

        return response

    def __repr__(self) -> str:
        return "UserID: {} \n Name: {}, {}\n Email: {}, \n Rank: {}".format(self.id, self.last_name, self.first_name, self.email, self.rank)

    def __str__(self) -> str:
        return "UserID: {} \n Name: {}, {}\n Email: {}, \n Rank: {}".format(self.id, self.last_name, self.first_name, self.email, self.rank)


@dataclass
class Prospect:
    """
    Class attributes
        - id: Optional[str]
        - name: Optional[str]
        - location: Optional[str]
        - coresignal_id: Optional[int]
        - linkedin_url: Optional[HttpUrl]
        - picture: Optional[HttpUrl]
        - event_type: Optional[EventType]
        - company: Optional[str]
        - start_date: Optional[date]
        - end_date: Optional[date]
        - full_data: Optional[Any]
        - analytics: Optional[Any]
        - date_created: Optional[datetime]
        - last_modified: Optional[datetime]

    Initialization function:
        This function allows several combinations of parameters tha behave differently.

        if only `data_dict` parameter is passed in:
            a `User` object will be constructed from the data passed in via the dictionary. The data dict must
            have the same keys as the object itself.

        if `WH_ID` and `auth_header` are passed in:
            this will cause the program to attempt to pull the user from the WH database. User with that UUID
            must already exist in the database and the credentials must be valid and properly formatted.

        All other combinations of the first 5 parameters are invalid.

    Args
    -----
        WH_ID: Optional[str]
            the UUID of a user in the database

        auth_header: Optional[Dict[str, Any]]
            the authorization header for the WEALTHAWK database

        data_dict: Optional[Dict[str, Any]]
            data to construct a user from
    """
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

    def __init__(self,
                WH_ID: Optional[str] = None,
                auth_header: Optional[Dict[str, Any]] = None,
                data_dict: Optional[Dict[str, Any]] = None,
                company_name: Optional[str] = None,
                event_type: Optional[EventType] = None) -> None:

        self.company = company_name
        self.event_type = event_type

        if WH_ID and auth_header:
            self._build_from_WH_db(WH_ID, auth_header)
        elif data_dict:
            self._build_from_data_dict(data_dict)
        else:
            raise ValueError("Invalid combination of init parameters")

    @property
    def languages(self) -> Optional[List[str]]:
        """
        parses full_data for prospect languages
        """
        if not self.full_data or 'member_languages_collection' not in self.full_data:
            return None

        member_lang = self.full_data['member_languages_collection']

        # iterate through language info to return a list of language names
        langs = [lang_data['member_language_list']['language']
                 for lang_data in member_lang
                 if 'member_language_list' in lang_data]

        if len(langs) == 0:
            return None
        else:
            return langs

    @property
    def event(self, auth_header: Dict[str, Any]) -> Optional['Event']:
        verify_auth_header(auth_header)

        # access db api to get event_id
        request = requests.get(WH_DB_URL + "/relate/person_to_event",
                               params={'personID': self.id}, headers=auth_header)
        content = request.json()

        if len(content) == 0:
            return None

        event_id = content[0]['eventID']

        # Get event object from ID
        event = Event(WH_ID=event_id, auth_header=auth_header)
        return event

    def _build_from_WH_db(self, WH_ID: Optional[str], auth_header: Dict[str, Any]) -> None:
        verify_auth_header(auth_header)
        request = requests.get(WH_DB_URL + "/person", params={'personID': WH_ID}, headers=auth_header)
        content = request.json()

        for key in list(content.keys()):
            self.__dict__[key] = content[key]

        if not self.full_data or self.full_data == '"null"':
            self.full_data = {}

        if not self.analytics or self.analytics == '"null"':
            self.analytics = {}

        self.in_database = True

    def _build_from_data_dict(self, data: Dict[str, Any]) -> None:
        verify_json("client", data)
        for key in list(data.keys()):
            self.__dict__[key] = data[key]

        if not self.id:
            self.id = str(uuid.uuid4())
        self.in_database = False
        if not self.analytics:
            self.analytics = {}

        if not self.full_data:
            self.full_data = {}

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

                 >>> exampleClient.send_to_db(WH_auth_dict).content.decode()

                 ``Not expecting client in database. Attempting Post request.``

                 ``'{"id":"1fd84bd0-779d-4a10-8c71-e2cf008d23ed"}'``

                But a successful ``PUT`` request will look like:

        """
        data = self.__dict__
        data = minus_key("in_database", data)
        url = WH_DB_URL + "/person"
        data['analytics'] = json.dumps(self.analytics)
        data['full_data'] = json.dumps(self.full_data)

        if self.in_database:
            print("Expecting Client in Database. Attempting PUT request")
            response = requests.put(url, json=data, headers=auth_header)
        else:
            print("Not expecting client in database. Attempting Post request.")
            response = requests.post(url, json=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content)

        return response

    def __repr__(self) -> str:
        return "ProspectID: {} \n Name: {} \n Location: {}".format(self.id, self.name, self.location)

    def __str__(self) -> str:
        return "ProspectID: {} \n Name: {} \n Location: {}".format(self.id, self.name, self.location)


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

    def __init__(self,
                WH_ID: Optional[str] = None,
                auth_header: Optional[Dict[str, Any]] = None,
                data_dict: Optional[Dict[str, Any]]= None) -> None:
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
        request = requests.get(WH_DB_URL + "/company", params={'companyID': WH_ID}, headers=auth_header)
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
        data['full_data'] = json.dumps(data['full_data'])
        data['analytics'] = json.dumps(data['analytics'])


        if self.in_database:
            print("Expected that object is already in database. Attempting PUT request")
            response = requests.put(url, json=data, headers=auth_header)
        else:
            print('Object not expected in database. Attempting POST request.')
            response = requests.post(url, data=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content.decode())

        return response

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

    def __init__(self,
                WH_ID: Optional[str] = None,
                auth_header: Optional[Dict[str, Any]] = None,
                data_dict: Optional[Dict[str, Any]] = None):
        """
        verify combination of variables and call the right function with the right params.

        """
        if WH_ID and auth_header:
            self._build_from_WH_db(WH_ID,auth_header)
        elif data_dict:
            self._build_from_data_dict(data_dict)
        else:
            raise ValueError("Invalid Combination of initialization variables. Did you include the auth_header?")

    def _build_from_WH_db(self, WH_ID: str, auth_header: Dict[str, Any]) -> None:
        verify_auth_header(auth_header)
        request = requests.get(WH_DB_URL + "/event", params={'eventID': WH_ID}, headers=auth_header)
        content = request.json()

        for key in list(content.keys()):
            self.__dict__[key] = content[key]

        if not self.full_data or self.full_data == '"null"':
            self.full_data = {}

        self.in_database = True
        return

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
        url = "https://db.wealthawk.com/event"
        data['other_info'] = json.dumps(data['other_info'])

        if self.in_database:
            print("Expected that object is already in database. Attempting PUT request")
            response = requests.put(url, json=data, headers=auth_header)
        else:
            print('Object not expected in database. Attempting POST request.')
            response = requests.post(url, data=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content.decode())

        return response


    def __repr__(self) -> str:
        return "EventID: {} \n Title: {}".format(self.id, self.title)

    def __str__(self) -> str:
        return "EventID: {} \n Title: {}".format(self.id, self.title)

