"""
Models a QEng hint
"""

from pydantic import BaseModel
import typing

__all__ = [
    "Hint",
]


class Hint(BaseModel):
    number: int = None
    description: str = None
    text: str = None
    delay_seconds: int = None
    penalty: int = 0

    class Config:
        fields = {
            "description": "info",
            "delay_seconds": "delay",
            "text": "hint",
        }
        allow_population_by_field_name = True
