[![Lines Of Code](https://tokei.rs/b1/github/Phaust94/qeng_admin_api?category=code)](https://github.com/Phaust94/qeng_admin_api)

This library allows interacting with QEng admin API

### Uploading new levels:

A level has NOT to have a `level_order_number` parameter set on LevelMetadata 
in order to be considered new.

```python
from qeng.game import Level, LevelSector, LevelMetadata, Bonus, Hint
from qeng import QengAPI

level = Level(
    level_metadata=LevelMetadata(
        in_game_name="Test1",
        task_text="tst1",
        autopass_time_seconds=100,
        bonus_for_not_autopass=10,
        time_multiplier_in_stats=0.3,
        stats_name="Public name",
        surrender_code="surr",
        task_script="alert(1)",
        answer_format="Word dick",
        answers_limit=19,
        answers_limit_duration_seconds=1000,
        answers_limit_penalty=4,
    ),
    sectors=[
        LevelSector(name="Test sec1", codes=["dick", "vag"])
    ],
    hints=[
        Hint(description="test_hint2", text="Look at me go", penalty=3)
    ],
    bonuses=[
        Bonus(
            answers=["a", "b"],
            delay_appearance_seconds=10,
            bonus_amount=30,
            description="this is bonus",
            text_after_solved="this is after"
        )
    ]
)

GAME_ID = 80
api = QengAPI("LOGIN", 'PASSWORD')
api.upload_level(level, GAME_ID)
```

### Updating existing levels:

A level has to have a `level_order_number` parameter set on LevelMetadata.
If bonuses, hints or sectors are present - these will be completely overwritten.
For level metadata - only the ones passed, will be updated, the rest will stay as they were

```python
from qeng.game import Level, LevelSector, LevelMetadata, Hint, Bonus
from qeng import QengAPI

level = Level(
    level_metadata=LevelMetadata(
        level_order_number=10,
        task_text="QGJHGJHSGDJHS",
    ),
    sectors=[
    ],
    hints=[
        Hint(description="test_hint2", text="Look at me go", penalty=3)
    ],
    bonuses=[
        Bonus(
            answers=["a", "b"],
            delay_appearance_seconds=10,
            text_after_solved="this is after"
        )
    ]
)

GAME_ID = 80
api = QengAPI("USER", 'PASSWORD')
api.update_level(level, GAME_ID)
```

### Getting whole game JSON

```python
from qeng import QengAPI

api = QengAPI("USERNAME", 'PASSWORD')
GAME_ID = 80
game = api.get_game(GAME_ID)
print(game)
```

This prints:
```python
game_metadata=GameMetadata(
    scoring_type=<GameScoringType.Time: '1'>, 
    statistics_state=<GameStatisticsState.PassedLevelsOnly: '6'>,
    team_limit=3,
    name='#SECRET',
    description='<p>Test game</p>',
    finish_text='', 
    social_network_image_url='https://imagizer.imageshack.com/img923/6088/DICK.jpg',
    start_time=datetime.datetime(2028, 1, 15, 21, 0),
    end_time=datetime.datetime(2028, 1, 19, 21, 0), 
    accept_teams_rule=<GameAcceptTeamsRule.EveryoneWhoPayedAutomatically: '1'>,
    start_type=<GameStartType.Separate: '1'>,
    price=600.3,
    currency=<GameCurrency.UAH: 'UAH'>,
    game_type=<GameType.Virtual: '4'>,
    scenario_state=<GameScenarioState.Open: '1'>,
    answer_prefix='aa', 
    default_passing_sequence=''
)
levels=[
    Level(
        level_metadata=LevelMetadata(
            level_order_number=1,
            autopass_time_seconds=None,
            bonus_for_not_autopass=None,
            time_multiplier_in_stats=None,
            in_game_name='Test1',
            stats_name=None, 
            surrender_code=None,
            task_text='',
            task_script=None,
            answer_format=None,
            answers_limit=None,
            answers_limit_duration_seconds=None,
            answers_limit_penalty=None,
            codes_required=0,
            autopass_reduction_with_each_code_seconds=0,
            code_bonus=0,
            finish_confirmation=<LevelFinishConfirmation.Smart: '1'>,
            bonus_display_style=<LevelBonusDisplayStyle.List: '0'>,
            bonus_closing_order=<LevelBonusClosingOrder.CloseBonusesAsIs: '0'>
        ),
        sectors=[], 
        bonuses=[], 
        hints=[]
    ), 
    Level(
        level_metadata=LevelMetadata(
            level_order_number=2,
            autopass_time_seconds=3368,
            bonus_for_not_autopass=22,
            time_multiplier_in_stats=None,
            in_game_name='New test level',
            stats_name=None,
            surrender_code=None,
            task_text='<a href="https://google.com">GUGL!</a>\n<br><br>\nА ответ - 42\n',
            task_script=None,
            answer_format=None,
            answers_limit=None,
            answers_limit_duration_seconds=None,
            answers_limit_penalty=None,
            codes_required=0,
            autopass_reduction_with_each_code_seconds=0,
            code_bonus=0,
            finish_confirmation=<LevelFinishConfirmation.Smart: '1'>,
            bonus_display_style=<LevelBonusDisplayStyle.List: '0'>,
            bonus_closing_order=<LevelBonusClosingOrder.CloseBonusesAsIs: '0'>),
            sectors=[
                LevelSector(
                    name='тест', codes='41,42,43'
                )
            ],
            bonuses=[],
            hints=[]
        )
    ]
    global_bonuses=[]
    passing_sequences=[
        PassingSequence(name='Линейка 33', level_order='1,3,4')
    ]
```

### Editing and uploading a game

```python
from qeng import QengAPI
from qeng import game as qgc

api = QengAPI("USERNAME", 'PASSWORD')
GAME_ID = 80
# Get the game first
game = api.get_game(GAME_ID)
# Changing game team acceptance rule
game.game_metadata.accept_teams_rule = qgc.GameMetadataEnums.GameAcceptTeamsRule.Manually
# Switching game to Red
game.game_metadata.game_type = qgc.GameMetadataEnums.GameType.Red
# Dropping all levels except first
game.levels = game.levels[:1]

# Defining a new level
txt = """<a href="https://google.com">GUGL22!</a>
"""
new_level = qgc.Level(
    level_metadata=qgc.LevelMetadata(
        autopass_time_seconds=222,
        bonus_for_not_autopass=33,
        in_game_name="New test level 2",
        task_text=txt,
    ),
    sectors=[
        qgc.LevelSector(
            name="тест",
            codes="86",
        )
    ]
)
game.levels.append(new_level)
# Upload now
api.upload_game(game, GAME_ID, delete_existing_levels=True)
```

### Uploading a part of a game

```python
from qeng import QengAPI

api = QengAPI("USERNAME", 'PASSWORD')
GAME_ID = 80
game = api.get_game(GAME_ID)
# Uploading only a part of a game
api.upload_global_bonuses(game.global_bonuses, game_id=81)
```