from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Order(str, Enum):
    POPULARITY = "popularity"
    DATE = "date"


class VoteType(str, Enum):
    UP = "up"
    DOWN = "down"