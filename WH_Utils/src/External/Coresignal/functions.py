import pandas as pd
import requests
import numpy as np
import os, sys
import json



def get_person_by_id(id_number, auth_dict):
    """
    This function just fetches a person by the id number from coresignal.
    params:
        self: its in a class
        id_number: the coresignal id number. Should be aquired from a coresignal query.
    returns:
        person_data (JSON): the full response from coresignal
    """
    url = "https://api.coresignal.com/dbapi/v1/collect/member/{}".format(id_number)
    response = requests.get(url, headers=auth_dict)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        raise ValueError("Bad Response Code. Response code: {}".format(response.status_code))

def get_person_by_url(linkedin_url, auth_dict):
    """
    Returns the coresignal for a person given the persons linkedin URL
    :param linkedin_url:
    :type linkedin_url:
    :return:
    :rtype:
    """
    if linkedin_url.endswith("/"):
        linkedin_url = linkedin_url[:-1]
    short_hand = linkedin_url.split("/")[-1]
    url = "https://api.coresignal.com/dbapi/v1/collect/member/{}".format(short_hand)
    response = requests.get(url, headers=auth_dict)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        raise ValueError("Bad Response Code. Response code: {}".format(response.status_code))



def find_employees_by_work_history(company_url, auth_dict):
    """
    Finds a list of employee coresignal id numbers based on where the employees worked.
    params:
        company_url: the linkedin_url of the company you want to find past employees of.
    returns:
        list of strings where every item is an id number of someone who worked at the target comapny
    """
    url = "https://api.coresignal.com/dbapi/v1/search/member"
    data = {"experience_company_linkedin_url": company_url}
    response = requests.post(url, headers=auth_dict, json=data)
    t = response.text[1:-1].split(',')
    return t
