"""
QEng Game metadata
"""
import datetime
import enum
import typing

from pydantic import BaseModel

__all__ = [
    "GameMetadataEnums",
    "GameMetadata",
]


class GameMetadataEnums:
    class GameScoringType(enum.Enum):
        Points = '0'
        Time = '1'

    class GameStatisticsState(enum.Enum):
        AlwaysOpen = '0'
        OpenWithoutBonuses = '1'
        ClosedDuringGame = '2'
        ShortStatsOnly = '4'
        AlwaysClosed = '5'
        PassedLevelsOnly = '6'

    class GameAcceptTeamsRule(enum.Enum):
        EveryoneAutomatically = '0'
        EveryoneWhoPayedAutomatically = '1'
        EveryoneAutomaticallyAsTesters = '2'
        Manually = '3'

    class GameStartType(enum.Enum):
        Simultaneous = '0'
        Separate = '1'

    class GameCurrency(enum.Enum):
        UAH = 'UAH'
        USD = "USD"
        EUR = "EUR"
        RUB = "RUB"

    class GameType(enum.Enum):
        Other = '0'
        Green = '1'
        Yellow = '2'
        Red = '3'
        Virtual = '4'

    class GameScenarioState(enum.Enum):
        Closed = '0'
        OpenForAll = '1'
        OpenForPlayedPlayers = '2'
        OpenForFinishedTeams = '3'


class GameMetadata(BaseModel):
    scoring_type: GameMetadataEnums.GameScoringType = GameMetadataEnums.GameScoringType.Time
    statistics_state: GameMetadataEnums.GameStatisticsState = GameMetadataEnums.GameStatisticsState.AlwaysClosed
    team_limit: int = 0
    name: str = "#New Unnamed Game"
    description: str = ""
    finish_text: str = ""
    html_header: str = ""
    social_network_image_url: typing.Optional[str] = ""
    start_time: datetime.datetime = datetime.datetime(2028, 12, 29)
    end_time: datetime.datetime = datetime.datetime(2033, 12, 29)
    accept_teams_rule: GameMetadataEnums.GameAcceptTeamsRule = GameMetadataEnums.GameAcceptTeamsRule.Manually
    start_type: GameMetadataEnums.GameStartType = GameMetadataEnums.GameStartType.Simultaneous
    price: float = 0
    currency: GameMetadataEnums.GameCurrency = GameMetadataEnums.GameCurrency.UAH
    game_type: GameMetadataEnums.GameType = GameMetadataEnums.GameType.Other
    scenario_state: GameMetadataEnums.GameScenarioState = GameMetadataEnums.GameScenarioState.Closed
    answer_prefix: str = None
    default_passing_sequence: str = ""

    class Config:
        fields = {
            "scoring_type": "type",
            "statistics_state": "stat",
            "social_network_image_url": "image",
            "accept_teams_rule": "status",
            "game_type": "kind",
            "scenario_state": "scenario",
            "default_passing_sequence": "default_line",
        }
        allow_population_by_field_name = True
        use_enum_values = False
        validate_assignment = True
