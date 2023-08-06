"""
TurnPhases
"""
from enum import Enum


class TurnPhase(Enum):
    """
    TurnPhases for gameplay.
    """
    INITIATIVE = 0
    MOVEMENT = 1
    WEAPON_ATTACK = 2
    PHYSICAL_ATTACK = 3
    HEAT = 4
    END = 5
