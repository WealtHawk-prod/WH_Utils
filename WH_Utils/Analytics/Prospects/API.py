from WH_Utils.Objects.Prospect import Prospect
from WH_Utils.Analytics.Prospects.Nodes import get_company_data, classify_job_title

from typing import List, Dict, Union, Optional


def run_analytics(prospect: Prospect) -> Dict[str, str]:
    """
    Get all analytics for a prospect

    Currently supported analytics:
        - ect
    """

    data = get_company_data(prospect)

    try:
        age = prospect.age

    except:
        age = None

    data = {
        "title": data['title'],
        "employee_rank": classify_job_title([data['title']])[0],
        "languages_spoken": prospect.languages,
        "age": age,
        "joined_pre_exit": data["joined_pre_exit?"],
        "days_at_company_preexist": data['time_pre_exit']
    }

    return data
