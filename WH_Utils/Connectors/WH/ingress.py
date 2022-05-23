

from WH_Utils import Prospect, Company, Event
from WH_Utils.Connectors.Coresignal import coresignal_to_company, coresingal_to_prospect
from WH_Utils.Analytics.Prospects import get_prospect_tags
from WH_Utils import EventType
from WH_Utils.Utils.test_utils import BASE_URL

import requests
import pandas as pd
import numpy as np
from datetime import datetime

from typing import Dict, List, Optional


def push_person(WH_auth_header: dict, prospect: Prospect, event_WH_ID: str, company_WH_ID: Optional[str] = None) -> None:
    """
    Pushes a prospect and all relational data to the WH backend

    Args:
        prospect: Prospect
            the person you want to push

        event_WH_ID: str
            the WH_ID of the event you want to push

        company_WH_ID: Optional[str]
            the WH_ID of the event you want to push

    Returns:
        None

    Raised:
        ConnectionError - If any of the pushes fail
    """
    response = prospect.send_to_db(WH_auth_header)
    assert response.status_code == 200, "There was an error pushing prospect {} to the DB: {}".format(prospect.id, response.text)

    prospect_id = response.json()['id']

    relate_prospect_and_event_url = BASE_URL + "/relate/person_to_event"
    params = {"personID":prospect_id, "eventID":event_WH_ID}
    prospect_to_event_response = requests.post(relate_prospect_and_event_url, params=params, headers=WH_auth_header)

    assert prospect_to_event_response.status_code == 200, "There was a problem with the prospect to event relation: {}".format(prospect_to_event_response.text)

    if company_WH_ID:
        relate_prospect_and_company_url = BASE_URL + "/relate/person_to_company"
        params = {"personID": prospect_id, "companyID": company_WH_ID}
        prospect_to_company_response = requests.post(relate_prospect_and_company_url, params=params, headers=WH_auth_header)

        assert prospect_to_company_response.status_code == 200, "There was a problem with the prospect to event relation: {}".format(
            prospect_to_company_response.text)


def push_event(
        title: str,
        description: str,
        type: EventType,
        date: datetime.date,
        link: str,
        location: str,
        value: int,
        other_info: dict,
        linkedin_of_exited_company: Optional[str] = None,
        associated_people_coresignal_ids: Optional[List[int]] = None,
        associated_people_WH_ids: Optional[List[str]] = None

) -> None:
    """

    """

    #make event, get id

    #make company, get id

    # get people ids

    #for persion in people ids
        # make person
        # get tags
        #push person

    return

