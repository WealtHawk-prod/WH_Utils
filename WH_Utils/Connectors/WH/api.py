import requests
from typing import List, Dict, Union

from WH_Utils.Objects.Event import Event
from WH_Utils.Objects.Prospect import Prospect
from WH_Utils.Objects.Company import Company

base_url = "https://db.wealthawk.com"

def get_event_by_person(client: Union[Prospect, str], auth_header: Dict[str, str]) -> Event:
    """

    """
    id = client.id if isinstance(client, Prospect) else client
    path = "/relate/person_to_event_by_person"
    url = base_url+path
    params = {"eventID": id}
    event_id = requests.get(url, params).json()[0]['eventID']
    event = Event(WH_ID=event_id, auth_header=auth_header)
    return event


def get_company_by_person(client: Union[Prospect, str], auth_header: Dict[str, str]) -> Company:
    """

    """
    id = client.id if isinstance(client, Prospect) else client
    path = "/relate/person_to_company_by_person"
    url = base_url+path
    params = {"eventID": id}
    companyID = requests.get(url, params).json()[0]['companyID']
    company = Company(WH_ID=companyID, auth_header=auth_header)
    return company
