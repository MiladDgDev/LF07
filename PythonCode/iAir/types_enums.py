import datetime
from enum import Enum
from typing import TypedDict


class conditions(Enum):
    DESIRABLE = 1
    UNDESIRABLE = 2

class commands(Enum):
    OPEN = 1
    CLOSE = 2
    ALERT = 3

class Activity(TypedDict):
    activity_id: int
    air_condition: conditions
    temperature: float
    humidity: float
    carbon_dioxide_level: float
    command: commands
    activity_time: datetime.datetime


def get_condition(index: int):
    if index < 1 or index > len(conditions):
        return conditions[1]
    else:
        return conditions[index]


def get_command(index: int):
    if index < 1 or index > len(commands):
        return commands[1]
    else:
        return commands[index]