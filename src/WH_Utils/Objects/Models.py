from datetime import datetime, date
from typing import Any, Optional

from pydantic import Json, HttpUrl

from src.WH_Utils.Objects.Enums import UserRank, EventType, CompanyType
from dataclasses import dataclass


@dataclass
class BaseModel:

    def __init__(self, WH_ID: str = None, auth_header: dict = None):
        return

@dataclass
class User(BaseModel):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    other_info: Optional[Any]
    rank: Optional[UserRank]
    firebase_id: Optional[str]
    created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

@dataclass
class Client(BaseModel):
    id: Optional[str]
    name: Optional[str]
    location: Optional[str]
    coresignal_id: Optional[int]
    linkedin_url: Optional[HttpUrl]
    picture: Optional[HttpUrl]
    event_type: Optional[EventType]
    company: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    full_data: Optional[Any]
    analytics: Optional[Any]
    date_created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

@dataclass
class Company(BaseModel):
    id: Optional[str]
    name: Optional[str]
    coresignal_id: Optional[int]
    linkedin_url: Optional[HttpUrl]
    industry: Optional[str]
    description: Optional[str]
    location: Optional[str]
    logo: Optional[HttpUrl]
    type: Optional[CompanyType]
    website: Optional[HttpUrl]
    created: Optional[datetime]
    last_modified: Optional[datetime]
    full_data: Optional[Any]

    class Config:
        arbitrary_types_allowed = True

@dataclass
class Event(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    type: Optional[EventType]
    date_of: Optional[date]
    link: Optional[HttpUrl]
    industry: Optional[str]
    location: Optional[str]
    value: Optional[int]
    other_info: Optional[Any]
    created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

@dataclass
class SignupSchema(BaseModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    location: Optional[str]
    picture: Optional[str]
    password: Optional[str]
    company: Optional[str]
    rank: Optional[str]

@dataclass
class AddTaskSchema(BaseModel):
    title: Optional[str]
    content: Optional[Json]
    email: Optional[str]
