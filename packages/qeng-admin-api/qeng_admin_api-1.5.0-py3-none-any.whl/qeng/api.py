"""
QEng API
"""
import json
import typing

import pydantic
import requests
from requests.cookies import RequestsCookieJar
from dataclasses import dataclass

from qeng.game import Level, Game, GameMetadata, GlobalBonus, PassingSequence

__all__ = [
    "QengAPI",
]

QENG_URL = 'https://qeng.org'


@dataclass
class QengAPI:
    username: str
    password: str
    domain_url: str = QENG_URL

    _cookies: RequestsCookieJar = None

    def __post_init__(self):
        self.authorize()
        return None

    @property
    def authorized(self) -> bool:
        return self._cookies is not None

    def authorize(self) -> None:
        endpoint = "login.php"
        auth = {'user': self.username, 'pass': self.password}
        res = requests.post(
            f"{self.domain_url}/{endpoint}",
            params={"json": 1},
            data=auth,
        )
        res.raise_for_status()
        succ = res.json()
        assert "login_error" not in succ, f"Invalid login/password: {succ['login_error']!r}"
        cookies = res.cookies
        self._cookies = cookies
        return None

    def _base_upload_level(self, level: Level, game_id: int) -> None:
        endpoint = "import_tasks.php"

        level_json = level.json(exclude_none=True, by_alias=True, exclude_unset=True)
        level_json = json.loads(level_json)

        upload_res = requests.post(
            f"{self.domain_url}/{endpoint}",
            params={
                "gid": game_id,
                "json": 1,
            },
            json=[level_json],
            cookies=self._cookies,
        )
        upload_res.raise_for_status()
        succ = upload_res.json()
        assert succ.get("success"), f"Failed to upload JSON because of {succ.get('error')!r}"
        return None

    def upload_level(self, level: Level, game_id: int) -> None:
        assert level.level_metadata.level_order_number is None, "Can't upload NEW level with level nuber specified"
        return self._base_upload_level(level, game_id)

    def update_level(self, level: Level, game_id: int) -> None:
        """
        If bonuses, hints or sectors are present - these will be completely overwritten.
        For level metadata - only the ones passed, will be updated, the rest will stay as they were
        :param level: Level class
        :param game_id: id of the game
        :return: None
        """
        assert level.level_metadata.level_order_number is not None, "Can't update level without level number specified"
        return self._base_upload_level(level, game_id)

    def get_game(self, game_id: int) -> Game:
        game_json = self.get_game_raw_json(game_id=game_id)
        game_inst = Game.parse_obj(game_json)
        return game_inst

    def get_game_raw_json(self, game_id: int) -> typing.Dict[str, typing.Any]:
        endpoint = "game_export.php"

        res = requests.get(
            f"{self.domain_url}/{endpoint}",
            params={
                "gid": game_id,
                "json": 1,
            },
            cookies=self._cookies,
        )
        res.raise_for_status()
        game_json = res.json()
        if "error" in game_json:
            raise ValueError(game_json["error"])
        return game_json

    def _upload_object(self, obj: typing.Any, game_id: int):
        endpoint = "import_tasks.php"

        params = {
            "gid": game_id,
            "json": 1,
        }

        res = requests.post(
            f"{self.domain_url}/{endpoint}",
            params=params,
            json=obj,
            cookies=self._cookies,
        )
        res.raise_for_status()
        json_data = res.json()
        if "error" in json_data:
            raise ValueError(json_data["error"])
        return None

    @staticmethod
    def _pydantic_to_json(obj: pydantic.BaseModel) -> typing.Any:
        obj_json = obj.json(exclude_none=True, by_alias=True, exclude_unset=True)
        obj_json = json.loads(obj_json)
        return obj_json

    @staticmethod
    def _map_name(obj: typing.Any, key_alias: str) -> typing.Dict[str, typing.Any]:
        key = Game.Config.fields[key_alias]
        obj_json = {
            key: obj
        }
        return obj_json

    def upload_game(self, game: Game, game_id: int, delete_existing_levels: bool = True) -> None:
        game_json = self._pydantic_to_json(game)
        if delete_existing_levels:
            game_json["delete_all_tasks"] = 1
        self._upload_object(game_json, game_id)
        return None

    def upload_game_metadata(self, game_metadata: GameMetadata, game_id: int) -> None:
        game_metadata_json = self._pydantic_to_json(game_metadata)
        game_metadata_json = self._map_name(game_metadata_json, "game_metadata")
        self._upload_object(game_metadata_json, game_id)
        return None

    def upload_global_bonuses(self, global_bonuses: typing.List[GlobalBonus], game_id: int) -> None:
        bonuses_json = [self._pydantic_to_json(b) for b in global_bonuses]
        bonuses_json = self._map_name(bonuses_json, "global_bonuses")
        self._upload_object(bonuses_json, game_id)
        return None

    def upload_passing_sequences(self, passing_sequences: typing.List[GlobalBonus], game_id: int) -> None:
        passing_sequences_json = [self._pydantic_to_json(b) for b in passing_sequences]
        passing_sequences_json = self._map_name(passing_sequences_json, "passing_sequences")
        self._upload_object(passing_sequences_json, game_id)
        return None
