from WH_Utils.Objects.Prospect import Prospect
from WH_Utils.Objects.Enums import JobRank
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from typing import Dict, List, Any
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

torch_device = "cuda" if torch.cuda.is_available() else 'cpu'
tokenizer = AutoTokenizer.from_pretrained("McClain/JobTitleClassification", use_auth_token=True)
model = AutoModelForSequenceClassification.from_pretrained("McClain/JobTitleClassification", use_auth_token=True).to(torch_device)
map_to_string = ['C-Suite', "Director", "VP", "Manager", "Senior", "Entry", "Intern", "Other"]


def get_company_data_by_id(prospect: Prospect, company_id: int, date: datetime.date) -> Dict[str, Any]:
    """
    This function gets all the data related to an employment record

    """
    d = [x for x in prospect.__dict__["full_data"]["member_experience_collection"] if x['company_id'] == company_id]
    df = pd.DataFrame().from_records(d)

    df["date_from_df"] = pd.to_datetime(df.date_from)
    df = df.sort_values("date_from_df", ascending=False)

    date_started = df["date_from_df"].min()
    title = df.iloc[0]['title']

    days_pre_exit = (date - date_started).days

    data = {
        "title": title,
        "joined_pre_exit?": True if days_pre_exit > 0 else False,
        "time_pre_exit": days_pre_exit
    }

    return data


def classify_job_title(sentences: List[str]) -> List[JobRank]:
    """
    Classify a list of job titles into one of the following ranks: ['C-Suite', "Director", "VP", "Manager", "Senior", "Entry", "Intern", "Other"]

    Args
    ----
        sentences: List[str]
            the list of job titles as strings

    Returns
    --------
        ranks: List[JobRank]
            The list of the classified ranks

    """
    encoded = [tokenizer.encode(x, return_tensors="pt").to(torch_device) for x in sentences]
    predictions = [int(model(e).logits.argmax()) for e in encoded]
    str_pred = [JobRank(map_to_string[int(x)]) for x in predictions]
    return str_pred
