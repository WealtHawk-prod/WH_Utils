from enum import Enum


class UserRank(str, Enum):
    admin = "admin"
    analyst = "analyst"
    user = "user"
    user_expired = "user_expired"


class Followables(str, Enum):
    company = "company"
    client = "client"
    event = "event"


class EventType(str, Enum):
    IPO = "IPO"
    acquisition = "acquisition"
    trust_dis = "trust_dis"
    divorce = "divorce"
    lottery = "lottery"
    injury = "injury"
    other = "other"


class CompanyType(str, Enum):
    public = 'public'
    private = 'private'
    state_owned = 'state_owned'
    subsidiary_of_public = 'subsidiary_of_public'
    sole_proprietor = 'sole proprietor'
    partnership = 'partnership'
