from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class VoteType(Enum):
    UP = "up"
    DOWN = "down"


class VoteAction(Enum):
    ADDED ="added"
    CHANGED = "changed"
    DELETED = "deleted"
