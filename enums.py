from enum import Enum


class Province(Enum):
    CONNACHT = "Connacht"
    LEINSTER = "Leinster"
    MUNSTER = "Munster"
    ULSTER = "Ulster"
    ERROR = "ERROR"


class County(Enum):
    ANTRIM = "Antrim"
    ARMAGH = "Armagh"
    CARLOW = "Carlow"
    CAVAN = "Cavan"
    CLARE = "Clare"
    CORK = "Cork"
    DERRY = "Derry"
    DONEGAL = "Donegal"
    DOWN = "Down"
    DUBLIN = "Dublin"
    FERMANAGH = "Fermanagh"
    GALWAY = "Galway"
    KERRY = "Kerry"
    KILDARE = "Kildare"
    KILKENNY = "Kilkenny"
    LAOIS = "Laois"
    LEITRIM = "Leitrim"
    LIMERICK = "Limerick"
    LONGFORD = "Longford"
    LOUTH = "Louth"
    MAYO = "Mayo"
    MEATH = "Meath"
    MONAGHAN = "Monaghan"
    OFFALY = "Offaly"
    ROSCOMMON = "Roscommon"
    SLIGO = "Sligo"
    TIPPERARY = "Tipperary"
    TYRONE = "Tyrone"
    WATERFORD = "Waterford"
    WESTMEATH = "Westmeath"
    WEXFORD = "Wexford"
    WICKLOW = "Wicklow"
    ERROR = "ERROR"


def string_to_enum(entry: str, enum: Province or County) -> Province or County:
    entry = entry.strip().upper()
    try:
        return enum[entry]
    except KeyError:
        return enum["ERROR"]

