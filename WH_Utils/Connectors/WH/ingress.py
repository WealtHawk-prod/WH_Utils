

from WH_Utils import Prospect, Company, Event
from WH_Utils.Connectors.Coresignal import coresignal_to_company, coresingal_to_prospect
from WH_Utils.Analytics.Prospects import get_prospect_tags
from WH_Utils import EventType

import requests
import pandas as pd
import numpy as np
from datetime import datetime

from typing import Dict, List, Optional

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
    return

