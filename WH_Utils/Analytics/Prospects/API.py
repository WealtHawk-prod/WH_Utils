from WH_Utils.Objects.Prospect import Prospect

from typing import List, Dict, Union, Optional

def run_analytics(prospect: Prospect) ->  Dict[str, str]:
    """
    Get all analytics for a prospect

    Currently supported analytics:
        - ect
    """
    return