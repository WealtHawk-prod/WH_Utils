import json
from typing import List, Union, Dict, Any
import re


class AuthError(Exception):
    pass


class JsonError(Exception):
    pass


def verify_json(expected_class: str, json: Dict[str, Any]) -> None:
    """

    """
    if expected_class == 'client':
        _verify_as_client(json)
    elif expected_class == 'company':
        _verify_as_company(json)
    elif expected_class == 'user':
        _verify_as_user(json)
    elif expected_class == "event":
        _verify_as_event(json)

    return None


def _verify_as_client(json: Dict[str, Any]) -> None:
    expected_keys = ['id', 'name', 'location', 'coresignal_id', 'linkedin_url', 'picture', 'event_type', 'company',
                     'start_date', 'end_date', 'full_data', 'analytics', 'created', 'last_modified']
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(expected_keys,
                                                                                                  actual_keys))


def _verify_as_company(json: Dict[str, Any]) -> None:
    expected_keys = ['id', 'name', 'coresignal_id', 'linkedin_url', 'description', 'location', 'logo',
                     'type', 'website', 'full_data', 'created', 'last_modified']
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(expected_keys,
                                                                                                  actual_keys))


def _verify_as_user(json: Dict[str, Any]) -> None:
    expected_keys = ['id', 'first_name', 'last_name', 'email', 'other_info', 'rank', 'firebase_id', 'created', 'last_modified']
    actual_keys = list(json.keys())
    same_keys =  set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError("JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(expected_keys,
                                                                                                              actual_keys))


def _verify_as_event(json: Dict[str, Any]) -> None:
    expected_keys = ['id', 'description', 'type', 'title', 'date_of', 'link', 'industry', 'location', 'value', 'other_info', 'created', 'last_modified']
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(expected_keys,
                                                                                                  actual_keys))

def verify_auth_header(json: Dict[str, Any]) -> None:
    if "Authorization" not in json:
        raise AuthError("The auth header dict doesn't appear to be in the right format")
    s = json['Authorization']
    if not "Bearer " in s:
        raise AuthError("The auth header dict doesn't appear to be in the right format")
    return None
