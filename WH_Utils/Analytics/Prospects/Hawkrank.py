from typing import List, Optional
import numpy as np
from WH_Utils.Objects.Enums import JobRank

def job_rank_to_int(rank: JobRank) -> int:
    """
    I guess these enums are not ordered for the time being so this is a small helper to
    convert to a order

    # Todo: depricate this nonsense and wrape this into the enum
    """
    ranks = {
        JobRank.founder: 10,
        JobRank.c_suite: 8,
        JobRank.vice_president: 7,
        JobRank.director: 6,
        JobRank.manager: 5,
        JobRank.senior: 4,
        JobRank.entry_level: 3,
        JobRank.other: 1,
        JobRank.intern: 0
    }
    return ranks[rank]


def get_hawkrank_company(rank: JobRank, days_at_company: Optional[int], days_pre_exit: Optional[int]) -> int:
    """
    Calculates a number between 0 and 100 that has a rough rank of equity for the company event they are associated with

    """
    if not days_at_company and not days_pre_exit:
        return 10*job_rank_to_int(rank)

    if days_pre_exit and days_at_company:
        # multiplier
        multiplier = 1.1 # change this

    else:
        multiplier = 1

    days_mult = multiplier * days_pre_exit

    metric = days_mult*job_rank_to_int(rank)
    #normalize metric to 100
    return metric



