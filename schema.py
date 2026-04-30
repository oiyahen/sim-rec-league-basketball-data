#Schema, let's you know what is in each table
games = [
    "game_id",
    "week",
    "date",
    "team_a_id",
    "team_b_id",
    "team_a_score",
    "team_b_score"
]

player_game_stats = [
    "game_id",
    "team_id",
    "player_id",
    "jersey_number",
    "player_name",
    "minutes",
    "pts",
    "reb",
    "ast",
    "fgm",
    "fga",
    "three_pm",
    "three_pa",
    "ftm",
    "fta",
    "to",
    "pf",
    "stl",
    "blk"
]
players = ["player_id",
           "player_name",
           "team_id",
           "jersey_number"
]
teams = [
    "team_id",
    "team_name",
    "team_abbr"
]

teams_data = [
    {"team_id": 1, "team_name": "Bad Boyz", "team_abbr": "BB"},
    {"team_id": 2, "team_name": "Two Eazy", "team_abbr": "TE"},
    {"team_id": 3, "team_name": "HomeGrown", "team_abbr": "HG"},
    {"team_id": 4, "team_name": "Skyhawks", "team_abbr": "SH"},
    {"team_id": 5, "team_name": "Oldmen", "team_abbr": "OM"},
    {"team_id": 6, "team_name": "Magic onna Wed", "team_abbr": "MOW"},
    {"team_id": 7, "team_name": "The Mob", "team_abbr": "TM"}
]
