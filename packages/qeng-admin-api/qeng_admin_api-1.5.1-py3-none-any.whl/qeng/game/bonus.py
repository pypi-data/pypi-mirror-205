"""
Models a QEng bonus
"""

from pydantic import BaseModel, Field
import typing

__all__ = [
    "Bonus",
    "GlobalBonus",
]


class _BaseBonus(BaseModel):
    answers: typing.Union[str, typing.List[str]] = Field(default_factory=list)
    bonus_amount: int = 0
    description: str = None
    text_after_solved: str = None

    class Config:
        fields = {
            "answers": "code",
            "bonus_amount": "time",
            "text_after_solved": "hint",
        }
        allow_population_by_field_name = True


class Bonus(_BaseBonus):
    number: int = None
    delay_appearance_seconds: int = None
    availability_duration_seconds: int = None
    time_left_conversion_coefficient: float = None

    class Config:
        fields = {
            "delay_appearance_seconds": "delay",
            "availability_duration_seconds": "duration",
            "time_left_conversion_coefficient": "duration_k",
        }
        allow_population_by_field_name = True


class GlobalBonus(_BaseBonus):
    available_from_level_n: int = 0
    available_to_level_n: int = 0

    class Config:
        fields = {
            "available_from_level_n": "first_task_n",
            "available_to_level_n": "last_task_n",
            "time_left_conversion_coefficient": "duration_k",
        }
        allow_population_by_field_name = True
