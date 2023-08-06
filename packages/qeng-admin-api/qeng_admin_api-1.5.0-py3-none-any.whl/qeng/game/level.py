"""
Models a QEng level
"""

import typing

from pydantic import BaseModel, Field

from qeng.game.level_metadata import LevelMetadata
from qeng.game.level_sector import LevelSector
from qeng.game.bonus import Bonus
from qeng.game.hint import Hint

__all__ = [
    "Level"
]


class Level(BaseModel):
    level_metadata: LevelMetadata = Field(default_factory=LevelMetadata)
    sectors: typing.List[LevelSector] = Field(default_factory=list)
    bonuses: typing.List[Bonus] = Field(default_factory=list)
    hints: typing.List[Hint] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        fields = {"level_metadata": "task", "sectors": "codes"}
