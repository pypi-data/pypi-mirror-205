"""
HexTypes
"""
from enum import Enum


class HexType(Enum):
    """
    HexTypes for game board
    """
    CLEAR = 0
    JUNGLE_LIGHT = 1
    JUNGLE_HEAVY = 2
    PAVEMENT = 3
    ROUGH = 4
    RUBBLE = 5
    SAND = 6
    WATER = 7
    WOODS_LIGHT = 8
    WOODS_HEAVY = 9
