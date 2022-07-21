from typing import List, Optional, Dict
import numpy as np
import pandas as pd
from WH_Utils.Objects.Enums import JobRank
from WH_Utils import Prospect
from WH_Utils.Analytics.Data.HW_Background import COL_INDEX


def hawkrank(prospect: Prospect) -> Dict[str, float]:
    """
    Calculate the HawkRank for a prospect.

    Args:
        prospect: Prospect
            The prospect to calculate the HawkRank for.

    Returns:
        Dict[str, float]
            A dictionary of the score breakdown for the prospect.

    Raises:
        ValueError: If There is too much missing data to calculate the score.

    # TODO: Make this possible.
    """
    raise NotImplementedError("This function is not yet implemented.")


def HawkRank_for_Company_event(job_rank: Optional[JobRank] = None, location: Optional[str] = None,
                               industry_index: Optional[int] = None, years_at_company: Optional[int] = None,
                               total_years: Optional[int] = None) -> Dict[str, float]:
    """
    Public wrapper function for `_hawk_rank_from_company_event`.

    This function will calculate the HawkRank for a prospect that is affiliated with a company event like an IPO or
    acquisition.

    This replaces any missing values with a reasonable but conservative value. If run with no parameters, it will return
    a value of about 30 which is a reasonable default. An enrty level person with a bit of experience bit still affiliated
    with an exit. This is a reasonable default.

    Args:
        job_rank: JobRank
            The rank the person has in the company.
        location: str
            the name of the city the person is based in.
        industry_index: ind
            the industry index for the job (1-8) higher numbers for higher paying industries
        years_at_company: int
            Number of years the person spent at the company
        total_years: int
            Number of years the person has worked

    Returns:
        Dict[str, float]
            A dictionary of the score breakdown for the prospect.

    Raises:
        ValueError: If There is too much missing data to calculate the score.

    """
    if job_rank is None:
        job_rank = JobRank.ENTRY_LEVEL

    if location is None:
        location = "Unknown"

    if industry_index is None:
        industry_index = 3

    if years_at_company is None:
        years_at_company = 1.5

    if total_years is None:
        total_years = 3

    return _hawk_rank_from_company_event(location, industry_index, job_rank, years_at_company, total_years)


def _hawk_rank_from_company_event(location: str, industry_index: int, job_rank: JobRank, years_at_company: float,
                                  total_years: float) -> Dict[str, float]:
    """
    Args:
        location: str

    """
    mean_location_score, std_loc_score = np.mean(list(COL_INDEX.values())), np.std(list(COL_INDEX.values()))
    location_score = COL_INDEX[location] if location in COL_INDEX else mean_location_score
    location_score = (location_score - mean_location_score) / std_loc_score
    years_at_company = np.min([years_at_company, 6])
    total_years = np.min([total_years, 10])

    loc_coef, industery_coeff, rank_coeff, yac_coeff, total_years_coeff = 3, 1, 4, 4, 3

    location_socre = loc_coef * location_score
    industry_score = industery_coeff * industry_index
    rank_score = rank_coeff * int(job_rank)
    yac_score = yac_coeff * years_at_company
    total_years_score = total_years_coeff * total_years

    total_score = np.sum([location_socre, industry_score, rank_score, yac_score, total_years_score])
    total_score = np.min([int(total_score), 100])

    breakdown = {
        "Value": round(total_score),
        "Industry": round(industry_score),
        "Job Rank": round(rank_score),
        "Time at Company": round(yac_score),
        "Total Experience": round(total_years_score),
        "Location Index": round(location_socre)
    }

    return breakdown
