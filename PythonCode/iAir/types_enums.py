import datetime
from enum import Enum
from typing import TypedDict


class Conditions(Enum):
    DESIRABLE = 1
    UNDESIRABLE = 2


class Commands(Enum):
    OPEN = 1
    CLOSE = 2
    ALERT = 3


class Activity(TypedDict):
    activity_id: int
    air_condition: Conditions
    temperature: str
    humidity: str
    carbon_dioxide_level: str
    command: Commands
    activity_time: str


class IndoorConditions(TypedDict):
    temperature: float
    humidity: float
    co2: float



class BadIndoorCondition(TypedDict):
    temperature_too_high: bool
    temperature_too_low: bool
    humidity_too_high: bool
    humidity_too_low: bool
    co2_too_high: bool


def get_condition(index: int):
    if index < 1 or index > len(Conditions):
        return list(Conditions)[1].name
    else:
        return list(Conditions)[index].name


def get_command(index: int):
    if index < 1 or index > len(Commands):
        return list(Commands)[1].name
    else:
        return list(Commands)[index].name
