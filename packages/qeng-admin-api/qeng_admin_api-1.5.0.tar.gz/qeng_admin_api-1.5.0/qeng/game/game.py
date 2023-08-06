"""
Models a QEng game
"""

import typing
import datetime
import pprint

from pydantic import BaseModel, Field

from qeng.game.level import Level
from qeng.game.bonus import GlobalBonus
from qeng.game.passing_sequence import PassingSequence
from qeng.game.game_metadata import GameMetadata

__all__ = [
    "Game",
]


class Game(BaseModel):
    game_metadata: GameMetadata = Field(default_factory=GameMetadata)
    levels: typing.List[Level] = Field(default_factory=list)
    global_bonuses: typing.List[GlobalBonus] = Field(default_factory=list)
    passing_sequences: typing.List[PassingSequence] = Field(default_factory=list)

    class Config:
        fields = {
            "game_metadata": "game",
            "levels": "tasks",
            "global_bonuses": "gbonuses",
            "passing_sequences": "lines",
        }
        allow_population_by_field_name = True
        json_encoders = {
            datetime.datetime: str,
        }
