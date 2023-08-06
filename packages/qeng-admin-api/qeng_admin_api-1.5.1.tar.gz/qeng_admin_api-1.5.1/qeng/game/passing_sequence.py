"""
Models a QEng game line (passing sequence)
"""

from pydantic import BaseModel

__all__ = [
    "PassingSequence",
]


class PassingSequence(BaseModel):
    name: str = "Sequence 1"
    level_order: str = ""

    class Config:
        fields = {
            "name": "title",
            "level_order": "task_order",
        }
        allow_population_by_field_name = True
