import datetime
from enum import Enum
from typing import TypedDict


class conditions(Enum):
    DESIRABLE = 1
    UNDESIRABLE = 2


class Commands(Enum):
    OPEN = 1
    CLOSE = 2
    ALERT = 3


class Activity(TypedDict):
    activity_id: int
    air_condition: conditions
    temperature: str
    humidity: str
    carbon_dioxide_level: str
    command: Commands
    activity_time: str


def get_condition(index: int):
    if index < 1 or index > len(conditions):
        return list(conditions)[1].name
    else:
        return list(conditions)[index].name


def get_command(index: int):
    if index < 1 or index > len(Commands):
        return list(Commands)[1].name
    else:
        return list(Commands)[index].name
