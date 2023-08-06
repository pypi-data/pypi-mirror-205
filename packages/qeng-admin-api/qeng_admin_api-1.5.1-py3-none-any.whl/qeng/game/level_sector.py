"""
Models a QEng level answer
"""

from pydantic import BaseModel, Field
import typing

__all__ = [
    "LevelSector",
]


class LevelSector(BaseModel):
    name: str = ""
    codes: typing.Union[
        str, typing.List[str]
    ] = Field(default_factory=list)

    class Config:
        fields = {"codes": "code"}
        allow_population_by_field_name = True
