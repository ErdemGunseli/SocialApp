from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class Order(Enum):
    POPULARITY = "popularity"
    DATE = "date"


class VoteType(Enum):
    UP = "up"
    DOWN = "down"
