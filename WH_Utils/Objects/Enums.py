"""
This is a simple module that is largly for type safty. It's more lightly documented that
most of the library because it should be pretty self explanitory. They are just simple
enum classes for the most part.
"""

from enum import Enum


# from aenum import Enum


class UserRank(str, Enum):
    """Enum for the possible ranks of users

    Simple enum class for the possible ranks a user can have. These are linked to permissions.

    Args
    ---------

        admin: Highest rank available. Can do literally anything. This should probably only ever be Ethan and McClain.

        analyst: Developed specifically for internal WH employees. They should have the ability to read update and soft delete.

        user: This is the default class for a paying user.

        user_expired: If they were once a user but no longer. Basically a user soft delete.

        user_new: If they are a new user not yet initialized by stripe webhook.


    """

    ADMIN = "admin"
    ANALYST = "analyst"
    USER = "user"
    USER_EXPIRED = "user_expired"
    USER_NEW = "user_new"
    USER_WAITLIST = "user_waitlist"


class OrgRank:
    ADMIN = "admin"
    USER = "user"
    NONE = "none"


class Followables(str, Enum):
    """All available followable entities

    Args
    -----
        company
        client
        event
    """

    COMPANY = "company"
    PROSPECT = "prospect"
    EVENT = "event"


class EventType(str, Enum):
    """The possible MIM events.

    Args
    -----
        IPO
        acquisition
        trust_dis
        divorce
        lottery
        injury
        other
    """

    IPO = "IPO"
    ACQUISITION = "Acquisition"
    FUND_RAISE = "fund_raise"
    TRUST_DIS = "trust_dis"
    DIVORCE = "Divorce"
    LOTTERY = "lottery"
    INJURY = "injury"
    OTHER = "other"


class CompanyType(str, Enum):
    """Possible stages of company.

    Args
    ------

        public: a publicly traded company
        private: a privatly held company
        state_owned: self explanitory
        subsidiary_of_public: I honestly don't know
        sole_proprietor: a small company owned by a single person
        partnership: like a sole_proprietor but with > 1 person

    """

    PUBLIC = "public"
    PRIVATE = "private"
    STATE_OWNED = "state_owned"
    SUBSIDIARY_OF_PUBLIC = "subsidiary_of_public"
    SOLE_PROPRIETOR = "sole proprietor"
    PARTNERSHIP = "partnership"


class JobRank(str, Enum):
    """
    The possible ranks a person can have within their company ranked from most to least equity
    """

    FOUNDER = "founder"
    C_SUITE = "c-suite"
    VICE_PRESIDENT = "vp"
    DIRECTOR = "director"
    MANAGER = "manager"
    SENIOR = "senior"
    ENTRY_LEVEL = "entry"
    INTERN = "intern"
    OTHER = "other"


class EventStage(str, Enum):
    """
    The possible stages an event can take
    """

    NOT_STARTED = "Not Started"
    EARLY_STAGE = "Early Stage"
    IN_PROGRESS = "In Progress"
    LATE_STAGE = "Late Stage"
    CLOSED = "Closed"
