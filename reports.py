from data import games_data, teams_data, players_data, player_game_stats_data




#
#
#
#GAME SUMMARY
#
#
#
#
def get_team(team_id):
    return next(t for t in teams_data if t["team_id"] == team_id)


def get_player(player_id):
    return next(p for p in players_data if p["player_id"] == player_id)


def team_record(team_id):
    wins = 0
    losses = 0

    for game in games_data:
        if game["team_a_score"] is None or game["team_b_score"] is None:
            continue

        team_played = team_id in [game["team_a_id"], game["team_b_id"]]

        if not team_played:
            continue

        if game["team_a_score"] > game["team_b_score"]:
            winner = game["team_a_id"]
        else:
            winner = game["team_b_id"]

        if winner == team_id:
            wins += 1
        else:
            losses += 1

    return f"{wins}-{losses}"


def pct(made, attempts):
    return (made / attempts * 100) if attempts > 0 else 0


def total(stats, key):
    return sum(p[key] for p in stats)


def team_totals(stats):
    return {
        "pts": total(stats, "pts"),
        "reb": total(stats, "reb"),
        "ast": total(stats, "ast"),
        "fg": f"{total(stats, 'fgm')}-{total(stats, 'fga')} ({pct(total(stats, 'fgm'), total(stats, 'fga')):.1f}%)",
        "three": f"{total(stats, 'three_pm')}-{total(stats, 'three_pa')} ({pct(total(stats, 'three_pm'), total(stats, 'three_pa')):.1f}%)",
        "ft": f"{total(stats, 'ftm')}-{total(stats, 'fta')} ({pct(total(stats, 'ftm'), total(stats, 'fta')):.1f}%)",
        "stl": total(stats, "stl"),
        "blk": total(stats, "blk"),
        "to": total(stats, "to"),
        "pf": total(stats, "pf")
    }


def player_rows(stats):
    rows = ""

    for stat in stats:
        player = get_player(stat["player_id"])

        rows += f"""
        <tr>
            <td>#{player["jersey_number"]} {player["player_name"]}</td>
            <td>{stat["minutes"]}</td>
            <td>{stat["pts"]}</td>
            <td>{stat["reb"]}</td>
            <td>{stat["ast"]}</td>
            <td>{stat["fgm"]}-{stat["fga"]}</td>
            <td>{stat["three_pm"]}-{stat["three_pa"]}</td>
            <td>{stat["ftm"]}-{stat["fta"]}</td>
            <td>{stat["stl"]}</td>
            <td>{stat["blk"]}</td>
            <td>{stat["to"]}</td>
            <td>{stat["pf"]}</td>
        </tr>
        """

    return rows


def export_game_report(game_id):
    game = next(g for g in games_data if g["game_id"] == game_id)

    team_a = get_team(game["team_a_id"])
    team_b = get_team(game["team_b_id"])

    team_a_stats = [
        p for p in player_game_stats_data
        if p["game_id"] == game_id and p["team_id"] == team_a["team_id"]
    ]

    team_b_stats = [
        p for p in player_game_stats_data
        if p["game_id"] == game_id and p["team_id"] == team_b["team_id"]
    ]

    a_totals = team_totals(team_a_stats)
    b_totals = team_totals(team_b_stats)


#
#
#
#
#
#
#----------------------------------------------------asked ai to do this, copied a template from a google search
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{team_a["team_name"]} vs {team_b["team_name"]}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            color: #222;
            padding: 30px;
        }}

        .report {{
            max-width: 1100px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        }}

        .scoreboard {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            text-align: center;
            margin-bottom: 25px;
        }}

        .team-name {{
            font-size: 28px;
            font-weight: bold;
        }}

        .score {{
            font-size: 48px;
            font-weight: bold;
            padding: 0 30px;
        }}

        .record {{
            color: #666;
            font-size: 15px;
            margin-top: 6px;
        }}

        h2 {{
            margin-top: 35px;
            border-bottom: 2px solid #222;
            padding-bottom: 8px;
        }}

        .team-stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}

        .stat-card {{
            background: #fafafa;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 18px;
        }}

        .stat-row {{
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #eee;
            padding: 7px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 14px;
        }}

        th {{
            background: #222;
            color: white;
            padding: 8px;
        }}

        td {{
            border-bottom: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}

        td:first-child, th:first-child {{
            text-align: left;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .report {{
                box-shadow: none;
            }}
        }}
    </style>
</head>

<body>
    <div class="report">

        <div class="scoreboard">
            <div>
                <div class="team-name">{team_a["team_name"]}</div>
                <div class="record">Record: {team_record(team_a["team_id"])}</div>
            </div>

            <div class="score">{game["team_a_score"]} - {game["team_b_score"]}</div>

            <div>
                <div class="team-name">{team_b["team_name"]}</div>
                <div class="record">Record: {team_record(team_b["team_id"])}</div>
            </div>
        </div>

        <h2>Team Stats</h2>

        <div class="team-stats">
            <div class="stat-card">
                <h3>{team_a["team_name"]}</h3>
                <div class="stat-row"><span>Points</span><strong>{a_totals["pts"]}</strong></div>
                <div class="stat-row"><span>Rebounds</span><strong>{a_totals["reb"]}</strong></div>
                <div class="stat-row"><span>Assists</span><strong>{a_totals["ast"]}</strong></div>
                <div class="stat-row"><span>FG</span><strong>{a_totals["fg"]}</strong></div>
                <div class="stat-row"><span>3FG</span><strong>{a_totals["three"]}</strong></div>
                <div class="stat-row"><span>FT</span><strong>{a_totals["ft"]}</strong></div>
                <div class="stat-row"><span>Steals</span><strong>{a_totals["stl"]}</strong></div>
                <div class="stat-row"><span>Blocks</span><strong>{a_totals["blk"]}</strong></div>
                <div class="stat-row"><span>Turnovers</span><strong>{a_totals["to"]}</strong></div>
                <div class="stat-row"><span>Fouls</span><strong>{a_totals["pf"]}</strong></div>
            </div>

            <div class="stat-card">
                <h3>{team_b["team_name"]}</h3>
                <div class="stat-row"><span>Points</span><strong>{b_totals["pts"]}</strong></div>
                <div class="stat-row"><span>Rebounds</span><strong>{b_totals["reb"]}</strong></div>
                <div class="stat-row"><span>Assists</span><strong>{b_totals["ast"]}</strong></div>
                <div class="stat-row"><span>FG</span><strong>{b_totals["fg"]}</strong></div>
                <div class="stat-row"><span>3FG</span><strong>{b_totals["three"]}</strong></div>
                <div class="stat-row"><span>FT</span><strong>{b_totals["ft"]}</strong></div>
                <div class="stat-row"><span>Steals</span><strong>{b_totals["stl"]}</strong></div>
                <div class="stat-row"><span>Blocks</span><strong>{b_totals["blk"]}</strong></div>
                <div class="stat-row"><span>Turnovers</span><strong>{b_totals["to"]}</strong></div>
                <div class="stat-row"><span>Fouls</span><strong>{b_totals["pf"]}</strong></div>
            </div>
        </div>

        <h2>{team_a["team_name"]} Player Box Score</h2>
        <table>
            <tr>
                <th>Player</th><th>MIN</th><th>PTS</th><th>REB</th><th>AST</th><th>FG</th><th>3FG</th><th>FT</th><th>STL</th><th>BLK</th><th>TO</th><th>PF</th>
            </tr>
            {player_rows(team_a_stats)}
        </table>

        <h2>{team_b["team_name"]} Player Box Score</h2>
        <table>
            <tr>
                <th>Player</th><th>MIN</th><th>PTS</th><th>REB</th><th>AST</th><th>FG</th><th>3FG</th><th>FT</th><th>STL</th><th>BLK</th><th>TO</th><th>PF</th>
            </tr>
            {player_rows(team_b_stats)}
        </table>

    </div>
</body>
</html>
"""

    file_name = f"game_{game_id}_report.html"

    with open(file_name, "w") as file:
        file.write(html)

    print(f"Created {file_name}")



# TEAM SEASON STATS
#
#
#
#
#
#asked ai to do this, I don't know HTML well - made some small edits (color, sizing) ----------------------------------------------------------------------
def export_team_overview_report():
    def total(stats, key):
        return sum(p[key] for p in stats)

    def pct(made, attempts):
        return (made / attempts * 100) if attempts > 0 else 0

    def team_record(team_id):
        wins = 0
        losses = 0

        for game in games_data:
            if game["team_a_score"] is None or game["team_b_score"] is None:
                continue

            if team_id not in [game["team_a_id"], game["team_b_id"]]:
                continue

            if game["team_a_score"] > game["team_b_score"]:
                winner = game["team_a_id"]
            else:
                winner = game["team_b_id"]

            if winner == team_id:
                wins += 1
            else:
                losses += 1

        return wins, losses

    team_rows = []

    for team in teams_data:
        team_id = team["team_id"]
        team_name = team["team_name"]

        team_games = [
            g for g in games_data
            if team_id in [g["team_a_id"], g["team_b_id"]]
        ]

        games_played = len(team_games)

        team_stats = [
            p for p in player_game_stats_data
            if p["team_id"] == team_id
        ]

        opponent_stats = [
            p for p in player_game_stats_data
            if p["game_id"] in [g["game_id"] for g in team_games]
            and p["team_id"] != team_id
        ]

        wins, losses = team_record(team_id)

        pts = total(team_stats, "pts")
        reb = total(team_stats, "reb")
        ast = total(team_stats, "ast")
        stl = total(team_stats, "stl")
        blk = total(team_stats, "blk")
        turnovers = total(team_stats, "to")

        fgm = total(team_stats, "fgm")
        fga = total(team_stats, "fga")
        three_pm = total(team_stats, "three_pm")
        three_pa = total(team_stats, "three_pa")
        ftm = total(team_stats, "ftm")
        fta = total(team_stats, "fta")

        opp_pts = total(opponent_stats, "pts")
        opp_fgm = total(opponent_stats, "fgm")
        opp_fga = total(opponent_stats, "fga")
        opp_three_pm = total(opponent_stats, "three_pm")
        opp_three_pa = total(opponent_stats, "three_pa")
        opp_turnovers = total(opponent_stats, "to")

        team_rows.append({
            "team_name": team_name,
            "record": f"{wins}-{losses}",
            "wins": wins,
            "losses": losses,

            "ppg": pts / games_played,
            "rpg": reb / games_played,
            "apg": ast / games_played,
            "spg": stl / games_played,
            "bpg": blk / games_played,
            "topg": turnovers / games_played,

            "fgapg": fga / games_played,
            "fgmpg": fgm / games_played,
            "fg_pct": pct(fgm, fga),

            "three_fgapg": three_pa / games_played,
            "three_fgmpg": three_pm / games_played,
            "three_pct": pct(three_pm, three_pa),

            "ftapg": fta / games_played,
            "ftmpg": ftm / games_played,
            "ft_pct": pct(ftm, fta),

            "ppga": opp_pts / games_played,
            "opp_fg_pct": pct(opp_fgm, opp_fga),
            "opp_three_pct": pct(opp_three_pm, opp_three_pa),
            "forced_topg": opp_turnovers / games_played
        })

    team_rows = sorted(
        team_rows,
        key=lambda t: (t["wins"], -t["losses"]),
        reverse=True
    )

    rows = ""

    for team in team_rows:
        rows += f"""
        <tr>
            <td>{team["team_name"]}</td>
            <td>{team["record"]}</td>
            <td>{team["ppg"]:.1f}</td>
            <td>{team["rpg"]:.1f}</td>
            <td>{team["apg"]:.1f}</td>
            <td>{team["spg"]:.1f}</td>
            <td>{team["bpg"]:.1f}</td>
            <td>{team["topg"]:.1f}</td>
            <td>{team["fgapg"]:.1f}</td>
            <td>{team["fgmpg"]:.1f}</td>
            <td>{team["fg_pct"]:.1f}%</td>
            <td>{team["three_fgapg"]:.1f}</td>
            <td>{team["three_fgmpg"]:.1f}</td>
            <td>{team["three_pct"]:.1f}%</td>
            <td>{team["ftapg"]:.1f}</td>
            <td>{team["ftmpg"]:.1f}</td>
            <td>{team["ft_pct"]:.1f}%</td>
            <td>{team["ppga"]:.1f}</td>
            <td>{team["opp_fg_pct"]:.1f}%</td>
            <td>{team["opp_three_pct"]:.1f}%</td>
            <td>{team["forced_topg"]:.1f}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>League Team Overview</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    padding: 30px;
}}

.container {{
    background: white;
    padding: 30px;
    border-radius: 12px;
    max-width: 1400px;
    margin: auto;
}}

h1 {{
    text-align: center;
    margin-bottom: 5px;
}}

.subtitle {{
    text-align: center;
    color: #black;
    margin-bottom: 25px;
}}

.table-wrap {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th {{
    background: #222;
    color: white;
    padding: 9px;
    white-space: nowrap;
}}

td {{
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #ddd;
    white-space: nowrap;
}}

td:first-child {{
    text-align: left;
    font-weight: bold;
}}

.offense {{
    background: #black;
}}

.defense {{
    background: #black;
}}

@media print {{
    body {{
        background: white;
        padding: 0;
    }}

    .container {{
        max-width: none;
        padding: 10px;
    }}

    table {{
        font-size: 10px;
    }}
}}
</style>

</head>

<body>
<div class="container">

<h1>League Team Overview</h1>
<div class="subtitle">Rec league team performances for the season</div>

<div class="table-wrap">
<table>
<tr>
    <th>Team</th>
    <th>Record</th>

    <th class="offense">PPG</th>
    <th class="offense">RPG</th>
    <th class="offense">APG</th>
    <th class="offense">SPG</th>
    <th class="offense">BPG</th>
    <th class="offense">TOPG</th>

    <th class="offense">FGAPG</th>
    <th class="offense">FGMPG</th>
    <th class="offense">FG%</th>

    <th class="offense">3FGAPG</th>
    <th class="offense">3FGMPG</th>
    <th class="offense">3FG%</th>

    <th class="offense">FTAPG</th>
    <th class="offense">FTMPG</th>
    <th class="offense">FT%</th>

    <th class="defense">PPGA</th>
    <th class="defense">Opp FG%</th>
    <th class="defense">Opp 3FG%</th>
    <th class="defense">Forced TOPG</th>
</tr>

{rows}

</table>
</div>

</div>
</body>
</html>
"""

    with open("team_overview_report.html", "w") as f:
        f.write(html)

    print("Created team_overview_report.html")

#-----------------------------------------------------------------------
#
#
#
#
#
#
#
#
#

#helpers for player leader boards
def player_season_stats():
    player_totals = {}

    for stat in player_game_stats_data:
        player_id = stat["player_id"]

        if player_id not in player_totals:
            player_totals[player_id] = {
                "games": 0,
                "pts": 0,
                "reb": 0,
                "ast": 0,
                "stl": 0,
                "blk": 0,
                "fgm": 0,
                "fga": 0,
                "three_pm": 0,
                "three_pa": 0,
                "team_id": stat["team_id"]
            }

        player_totals[player_id]["games"] += 1
        player_totals[player_id]["pts"] += stat["pts"]
        player_totals[player_id]["reb"] += stat["reb"]
        player_totals[player_id]["ast"] += stat["ast"]
        player_totals[player_id]["stl"] += stat["stl"]
        player_totals[player_id]["blk"] += stat["blk"]

        player_totals[player_id]["fgm"] += stat["fgm"]
        player_totals[player_id]["fga"] += stat["fga"]
        player_totals[player_id]["three_pm"] += stat["three_pm"]
        player_totals[player_id]["three_pa"] += stat["three_pa"]

    player_averages = []

    for player_id, stats in player_totals.items():
        gp = stats["games"]

        if gp < 5:
            continue

        fgm = stats["fgm"]
        fga = stats["fga"]
        three_pm = stats["three_pm"]
        three_pa = stats["three_pa"]

        fg_pct = (fgm / fga * 100) if fga > 0 else 0
        three_pct = (three_pm / three_pa * 100) if three_pa > 0 else 0

        player_averages.append({
            "player_id": player_id,
            "team_id": stats["team_id"],
            "gp": gp,

            "ppg": stats["pts"] / gp,
            "rpg": stats["reb"] / gp,
            "apg": stats["ast"] / gp,
            "spg": stats["stl"] / gp,
            "bpg": stats["blk"] / gp,

            "fg_pct": fg_pct,
            "three_pct": three_pct,

            "fga": fga,
            "three_pa": three_pa
        })

    return player_averages

def export_league_leaders_report():

    players = player_season_stats()

    def get_player_name(player_id):
        player = next(p for p in players_data if p["player_id"] == player_id)
        return player["player_name"]

    def get_team_abbr(team_id):
        team = next(t for t in teams_data if t["team_id"] == team_id)
        return team["team_abbr"]

    def leader_rows(stat_key, is_pct=False, min_attempt_key=None, min_attempts=0):
        eligible_players = players

        if min_attempt_key:
            eligible_players = [
                p for p in players
                if p[min_attempt_key] >= min_attempts
            ]

        leaders = sorted(
            eligible_players,
            key=lambda p: p[stat_key],
            reverse=True
        )[:5]

        rows = ""

        for i, player in enumerate(leaders, start=1):
            value = player[stat_key]

            if is_pct:
                value_display = f"{value:.1f}%"
            else:
                value_display = f"{value:.1f}"

            rows += f"""
            <tr>
                <td>{i}</td>
                <td>{get_player_name(player["player_id"])}</td>
                <td>{get_team_abbr(player["team_id"])}</td>
                <td>{player["gp"]}</td>
                <td>{value_display}</td>
            </tr>
            """

        return rows
#------------------------------Leaderboard HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>League Leaders</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    padding: 30px;
}}

.container {{
    max-width: 1000px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 14px;
}}

h1 {{
    text-align: center;
}}

.grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}}

.card {{
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 18px;
    background: #fafafa;
}}

h2 {{
    margin-top: 0;
    font-size: 20px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background: #222;
    color: white;
    padding: 8px;
}}

td {{
    padding: 8px;
    border-bottom: 1px solid #ddd;
    text-align: center;
}}

td:nth-child(2), th:nth-child(2) {{
    text-align: left;
}}

.note {{
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}}

@media print {{
    body {{
        background: white;
        padding: 0;
    }}

    .container {{
        box-shadow: none;
        max-width: none;
    }}
}}
</style>

</head>

<body>
<div class="container">

<h1>League Leaders</h1>
<div class="note">Minimum 5 games played. FG% requires 30 FGA. 3FG% requires 15 3FGA.</div>

<div class="grid">

<div class="card">
<h2>Points Per Game</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>PPG</th></tr>
{leader_rows("ppg")}
</table>
</div>

<div class="card">
<h2>Rebounds Per Game</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>RPG</th></tr>
{leader_rows("rpg")}
</table>
</div>

<div class="card">
<h2>Assists Per Game</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>APG</th></tr>
{leader_rows("apg")}
</table>
</div>

<div class="card">
<h2>Steals Per Game</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>SPG</th></tr>
{leader_rows("spg")}
</table>
</div>

<div class="card">
<h2>Blocks Per Game</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>BPG</th></tr>
{leader_rows("bpg")}
</table>
</div>

<div class="card">
<h2>Field Goal %</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>FG%</th></tr>
{leader_rows("fg_pct", is_pct=True, min_attempt_key="fga", min_attempts=30)}
</table>
</div>

<div class="card">
<h2>3 Point %</h2>
<table>
<tr><th>#</th><th>Player</th><th>Team</th><th>GP</th><th>3FG%</th></tr>
{leader_rows("three_pct", is_pct=True, min_attempt_key="three_pa", min_attempts=15)}
</table>
</div>

</div>
</div>
</body>
</html>
"""

    with open("league_leaders_report.html", "w") as f:
        f.write(html)

    print("Created league_leaders_report.html")


#---------------------------------------------------------------
#Roster Stats Sheet
#
#
#
#
#
#


#helpers
def team_player_season_stats(team_id):

    player_totals = {}

    for stat in player_game_stats_data:
        if stat["team_id"] != team_id:
            continue

        player_id = stat["player_id"]

        if player_id not in player_totals:
            player_totals[player_id] = {
                "games": 0,
                "minutes": 0,
                "pts": 0,
                "reb": 0,
                "ast": 0,
                "stl": 0,
                "blk": 0,
                "to": 0,
                "fgm": 0,
                "fga": 0,
                "three_pm": 0,
                "three_pa": 0,
                "ftm": 0,
                "fta": 0
            }

        player_totals[player_id]["games"] += 1
        player_totals[player_id]["minutes"] += stat["minutes"]
        player_totals[player_id]["pts"] += stat["pts"]
        player_totals[player_id]["reb"] += stat["reb"]
        player_totals[player_id]["ast"] += stat["ast"]
        player_totals[player_id]["stl"] += stat["stl"]
        player_totals[player_id]["blk"] += stat["blk"]
        player_totals[player_id]["to"] += stat["to"]

        player_totals[player_id]["fgm"] += stat["fgm"]
        player_totals[player_id]["fga"] += stat["fga"]
        player_totals[player_id]["three_pm"] += stat["three_pm"]
        player_totals[player_id]["three_pa"] += stat["three_pa"]
        player_totals[player_id]["ftm"] += stat["ftm"]
        player_totals[player_id]["fta"] += stat["fta"]

    players = []

    for player_id, stats in player_totals.items():
        gp = stats["games"]

        players.append({
            "player_id": player_id,
            "gp": gp,
            "mpg": stats["minutes"] / gp,
            "ppg": stats["pts"] / gp,
            "rpg": stats["reb"] / gp,
            "apg": stats["ast"] / gp,
            "spg": stats["stl"] / gp,
            "bpg": stats["blk"] / gp,
            "topg": stats["to"] / gp,

            "fg": f"{stats['fgm']}-{stats['fga']}",
            "fg_pct": (stats["fgm"] / stats["fga"] * 100) if stats["fga"] > 0 else 0,

            "three": f"{stats['three_pm']}-{stats['three_pa']}",
            "three_pct": (stats["three_pm"] / stats["three_pa"] * 100) if stats["three_pa"] > 0 else 0,

            "ft": f"{stats['ftm']}-{stats['fta']}",
            "ft_pct": (stats["ftm"] / stats["fta"] * 100) if stats["fta"] > 0 else 0
        })

    return players

#
def export_roster_season_report(team_id):

    team = get_team(team_id)
    players = team_player_season_stats(team_id)

    players = sorted(players, key=lambda p: p["ppg"], reverse=True)

    ppg_leader = max(players, key=lambda p: p["ppg"])
    rpg_leader = max(players, key=lambda p: p["rpg"])
    apg_leader = max(players, key=lambda p: p["apg"])

    def player_name(player_id):
        return get_player(player_id)["player_name"]

    def leader_text(player, stat_key, label):
        return f"{player_name(player['player_id'])} - {player[stat_key]:.1f} {label}"

    rows = ""

    for player in players:
        rows += f"""
        <tr>
            <td>{player_name(player["player_id"])}</td>
            <td>{player["gp"]}</td>
            <td>{player["mpg"]:.1f}</td>
            <td>{player["ppg"]:.1f}</td>
            <td>{player["rpg"]:.1f}</td>
            <td>{player["apg"]:.1f}</td>
            <td>{player["spg"]:.1f}</td>
            <td>{player["bpg"]:.1f}</td>
            <td>{player["topg"]:.1f}</td>
            <td>{player["fg"]}</td>
            <td>{player["fg_pct"]:.1f}%</td>
            <td>{player["three"]}</td>
            <td>{player["three_pct"]:.1f}%</td>
            <td>{player["ft"]}</td>
            <td>{player["ft_pct"]:.1f}%</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{team["team_name"]} Roster Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    padding: 30px;
}}

.container {{
    background: white;
    max-width: 1200px;
    margin: auto;
    padding: 30px;
    border-radius: 14px;
}}

h1 {{
    text-align: center;
    margin-bottom: 5px;
}}

.record {{
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}}

.leaders {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 18px;
    margin-bottom: 30px;
}}

.card {{
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}}

.card h3 {{
    margin: 0 0 10px 0;
}}

.table-wrap {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}}

th {{
    background: #222;
    color: white;
    padding: 8px;
    white-space: nowrap;
}}

td {{
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #ddd;
    white-space: nowrap;
}}

td:first-child {{
    text-align: left;
    font-weight: bold;
}}

@media print {{
    body {{
        background: white;
        padding: 0;
    }}

    .container {{
        max-width: none;
        padding: 10px;
    }}

    table {{
        font-size: 10px;
    }}
}}
</style>
</head>

<body>
<div class="container">

<h1>{team["team_name"]} Season Report</h1>
<div class="record">Record: {team_record(team_id)}</div>

<div class="leaders">
    <div class="card">
        <h3>PPG Leader</h3>
        <div>{leader_text(ppg_leader, "ppg", "PPG")}</div>
    </div>

    <div class="card">
        <h3>RPG Leader</h3>
        <div>{leader_text(rpg_leader, "rpg", "RPG")}</div>
    </div>

    <div class="card">
        <h3>APG Leader</h3>
        <div>{leader_text(apg_leader, "apg", "APG")}</div>
    </div>
</div>

<h2>Roster Season Stats</h2>

<div class="table-wrap">
<table>
<tr>
    <th>Player</th>
    <th>GP</th>
    <th>MPG</th>
    <th>PPG</th>
    <th>RPG</th>
    <th>APG</th>
    <th>SPG</th>
    <th>BPG</th>
    <th>TOPG</th>
    <th>FG</th>
    <th>FG%</th>
    <th>3FG</th>
    <th>3FG%</th>
    <th>FT</th>
    <th>FT%</th>
</tr>

{rows}

</table>
</div>

</div>
</body>
</html>
"""

    file_name = f"{team['team_abbr'].lower()}_roster_report.html"

    with open(file_name, "w") as f:
        f.write(html)

    print(f"Created {file_name}")


#-----------------------------------------------------------------
#player report
#
#
#
#
#
#
#
def export_player_report(player_id):
    player = get_player(player_id)

    player_games = [
        g for g in player_game_stats_data
        if g["player_id"] == player_id
    ]

    if len(player_games) == 0:
        print("No games found for this player.")
        return

    team = get_team(player_games[0]["team_id"])
    record = team_record(team["team_id"])
    gp = len(player_games)

    def total(key):
        return sum(g[key] for g in player_games)

    minutes = total("minutes")
    pts = total("pts")
    reb = total("reb")
    ast = total("ast")
    stl = total("stl")
    blk = total("blk")
    turnovers = total("to")
    pf = total("pf")

    fgm = total("fgm")
    fga = total("fga")
    three_pm = total("three_pm")
    three_pa = total("three_pa")
    ftm = total("ftm")
    fta = total("fta")

    two_pm = fgm - three_pm
    two_pa = fga - three_pa

    fg_pct = pct(fgm, fga)
    two_pct = pct(two_pm, two_pa)
    three_pct = pct(three_pm, three_pa)
    ft_pct = pct(ftm, fta)

    efg = ((fgm + 0.5 * three_pm) / fga * 100) if fga > 0 else 0
    ts = (pts / (2 * (fga + 0.44 * fta)) * 100) if (fga + fta) > 0 else 0
    ast_to = ast / turnovers if turnovers > 0 else ast

    possessions = fga + 0.44 * fta + turnovers
    offensive_rating = (pts / possessions * 100) if possessions > 0 else 0
    defensive_rating = 100 - ((stl + blk) / gp * 3)
    net_rating = offensive_rating - defensive_rating

    career_highs = {
        "minutes": max(g["minutes"] for g in player_games),
        "pts": max(g["pts"] for g in player_games),
        "reb": max(g["reb"] for g in player_games),
        "ast": max(g["ast"] for g in player_games),
        "stl": max(g["stl"] for g in player_games),
        "blk": max(g["blk"] for g in player_games),
    }

    def shooting_label(shooting_pct):
        if shooting_pct >= 60:
            return "Hot"
        elif shooting_pct >= 50:
            return "Warm"
        elif shooting_pct >= 40:
            return "Normal"
        elif shooting_pct >= 30:
            return "Chill"
        else:
            return "Cold"

    def shooting_class(shooting_pct):
        if shooting_pct >= 60:
            return "hot"
        elif shooting_pct >= 50:
            return "warm"
        elif shooting_pct >= 40:
            return "normal"
        elif shooting_pct >= 30:
            return "chill"
        else:
            return "cold"

    inside_label = shooting_label(two_pct)
    inside_class = shooting_class(two_pct)

    outside_label = shooting_label(three_pct)
    outside_class = shooting_class(three_pct)

    game_rows = ""

    player_games = sorted(player_games, key=lambda g: g["game_id"])

    for g in player_games:
        game_ts = (
            g["pts"] / (2 * (g["fga"] + 0.44 * g["fta"])) * 100
            if (g["fga"] + g["fta"]) > 0 else 0
        )

        game_efg = (
            (g["fgm"] + 0.5 * g["three_pm"]) / g["fga"] * 100
            if g["fga"] > 0 else 0
        )

        game_ast_to = g["ast"] / g["to"] if g["to"] > 0 else g["ast"]

        game_rows += f"""
        <tr>
            <td>{g["game_id"]}</td>
            <td>{g["minutes"]}</td>
            <td>{g["pts"]}</td>
            <td>{g["reb"]}</td>
            <td>{g["ast"]}</td>
            <td>{g["stl"]}</td>
            <td>{g["blk"]}</td>
            <td>{g["to"]}</td>
            <td>{g["fgm"]}-{g["fga"]}</td>
            <td>{pct(g["fgm"], g["fga"]):.1f}%</td>
            <td>{g["three_pm"]}-{g["three_pa"]}</td>
            <td>{pct(g["three_pm"], g["three_pa"]):.1f}%</td>
            <td>{g["ftm"]}-{g["fta"]}</td>
            <td>{game_efg:.1f}%</td>
            <td>{game_ts:.1f}%</td>
            <td>{game_ast_to:.2f}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{player["player_name"]} Player Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    padding: 30px;
    color: #222;
}}

.container {{
    background: white;
    max-width: 1250px;
    margin: auto;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}}

.header {{
    display: grid;
    grid-template-columns: 1fr 310px;
    gap: 25px;
    align-items: start;
}}

.player-title h1 {{
    margin-bottom: 5px;
}}

.meta {{
    color: #666;
    font-size: 15px;
}}

.card-grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
    margin: 25px 0;
}}

.card {{
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}}

.card h3 {{
    margin: 0;
    font-size: 13px;
    color: #666;
}}

.card div {{
    font-size: 22px;
    font-weight: bold;
    margin-top: 8px;
}}

h2 {{
    margin-top: 35px;
    border-bottom: 2px solid #222;
    padding-bottom: 8px;
}}

.shot-card {{
    background: #fafafa;
    border: 1px solid #ddd;
    border-radius: 14px;
    padding: 16px;
}}

.shot-title {{
    text-align: center;
    font-weight: bold;
    margin-bottom: 12px;
}}

.simple-court {{
    width: 260px;
    height: 230px;
    margin: auto;
    position: relative;
    border: 3px solid #222;
    border-top: none;
    border-radius: 0 0 130px 130px;
    background: white;
}}

.arc {{
    position: absolute;
    left: 35px;
    top: 55px;
    width: 190px;
    height: 150px;
    border: 3px solid #222;
    border-top: none;
    border-radius: 0 0 95px 95px;
}}

.paint {{
    position: absolute;
    left: 95px;
    top: 95px;
    width: 70px;
    height: 90px;
    border: 2px solid #222;
}}

.hoop {{
    position: absolute;
    left: 117px;
    top: 185px;
    width: 25px;
    height: 25px;
    border: 3px solid #222;
    border-radius: 50%;
}}

.shot-box {{
    position: absolute;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    border: 1px solid #999;
    font-size: 13px;
    font-weight: bold;
}}

.inside-box {{
    left: 72px;
    top: 112px;
    width: 115px;
}}

.outside-box {{
    left: 45px;
    top: 25px;
    width: 170px;
}}

.shot-box span {{
    display: block;
    font-size: 12px;
    margin-top: 4px;
}}

.hot {{
    background: #ffb3b3;
}}

.warm {{
    background: #ffd9b3;
}}

.normal {{
    background: #eeeeee;
}}

.chill {{
    background: #cce0ff;
}}

.cold {{
    background: #b3d9ff;
}}

.legend {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-top: 12px;
    font-size: 11px;
}}

.legend-item {{
    padding: 5px;
    border-radius: 6px;
    text-align: center;
    border: 1px solid #ddd;
}}

.table-wrap {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    margin-top: 15px;
}}

th {{
    background: #222;
    color: white;
    padding: 8px;
    white-space: nowrap;
}}

td {{
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #ddd;
    white-space: nowrap;
}}

.note {{
    font-size: 12px;
    color: #666;
    margin-top: 8px;
}}

@media print {{
    body {{
        background: white;
        padding: 0;
    }}

    .container {{
        box-shadow: none;
        max-width: none;
        padding: 10px;
    }}

    table {{
        font-size: 10px;
    }}
}}
</style>
</head>

<body>
<div class="container">

<div class="header">
    <div class="player-title">
        <h1>{player["player_name"]}</h1>
        <div class="meta">
            Team: {team["team_name"]} |
            Record: {record} |
            Games Played: {gp}
        </div>

        <h2>Career Highs</h2>
        <div class="card-grid">
            <div class="card"><h3>MIN</h3><div>{career_highs["minutes"]}</div></div>
            <div class="card"><h3>PTS</h3><div>{career_highs["pts"]}</div></div>
            <div class="card"><h3>REB</h3><div>{career_highs["reb"]}</div></div>
            <div class="card"><h3>AST</h3><div>{career_highs["ast"]}</div></div>
            <div class="card"><h3>STL</h3><div>{career_highs["stl"]}</div></div>
            <div class="card"><h3>BLK</h3><div>{career_highs["blk"]}</div></div>
        </div>
    </div>

    <div class="shot-card">
        <div class="shot-title">Shooting Profile</div>

        <div class="simple-court">
            <div class="arc"></div>
            <div class="paint"></div>
            <div class="hoop"></div>

            <div class="shot-box outside-box {outside_class}">
                Outside Arc
                <span>{three_pm}-{three_pa}</span>
                <span>{three_pct:.1f}% | {outside_label}</span>
            </div>

            <div class="shot-box inside-box {inside_class}">
                Inside Arc
                <span>{two_pm}-{two_pa}</span>
                <span>{two_pct:.1f}% | {inside_label}</span>
            </div>
        </div>

        <div class="legend">
            <div class="legend-item hot">Hot 60%+</div>
            <div class="legend-item warm">Warm 50-59%</div>
            <div class="legend-item normal">Normal 40-49%</div>
            <div class="legend-item chill">Chill 30-39%</div>
            <div class="legend-item cold">Cold &lt; 30%</div>
        </div>

        <div class="note">This uses actual 2PT and 3PT shooting data, not simulated shot locations.</div>
    </div>
</div>

<h2>Season Averages</h2>
<div class="card-grid">
    <div class="card"><h3>MPG</h3><div>{minutes / gp:.1f}</div></div>
    <div class="card"><h3>PPG</h3><div>{pts / gp:.1f}</div></div>
    <div class="card"><h3>RPG</h3><div>{reb / gp:.1f}</div></div>
    <div class="card"><h3>APG</h3><div>{ast / gp:.1f}</div></div>
    <div class="card"><h3>SPG</h3><div>{stl / gp:.1f}</div></div>
    <div class="card"><h3>BPG</h3><div>{blk / gp:.1f}</div></div>
</div>

<h2>Advanced Metrics</h2>
<div class="card-grid">
    <div class="card"><h3>FG%</h3><div>{fg_pct:.1f}%</div></div>
    <div class="card"><h3>2P%</h3><div>{two_pct:.1f}%</div></div>
    <div class="card"><h3>3P%</h3><div>{three_pct:.1f}%</div></div>
    <div class="card"><h3>eFG%</h3><div>{efg:.1f}%</div></div>
    <div class="card"><h3>TS%</h3><div>{ts:.1f}%</div></div>
    <div class="card"><h3>AST/TO</h3><div>{ast_to:.2f}</div></div>
</div>

<div class="card-grid">
    <div class="card"><h3>FT%</h3><div>{ft_pct:.1f}%</div></div>
    <div class="card"><h3>TOPG</h3><div>{turnovers / gp:.1f}</div></div>
    <div class="card"><h3>PFPG</h3><div>{pf / gp:.1f}</div></div>
    <div class="card"><h3>Off Rating</h3><div>{offensive_rating:.1f}</div></div>
    <div class="card"><h3>Def Rating</h3><div>{defensive_rating:.1f}</div></div>
    <div class="card"><h3>Net Rating</h3><div>{net_rating:.1f}</div></div>
</div>

<div class="note">
    Offensive Rating, Defensive Rating, and Net Rating are estimates because we do not have play-by-play or on-court lineup data yet.
</div>

<h2>Game Box Scores</h2>
<div class="table-wrap">
<table>
<tr>
    <th>Game</th>
    <th>MIN</th>
    <th>PTS</th>
    <th>REB</th>
    <th>AST</th>
    <th>STL</th>
    <th>BLK</th>
    <th>TO</th>
    <th>FG</th>
    <th>FG%</th>
    <th>3PT</th>
    <th>3PT%</th>
    <th>FT</th>
    <th>eFG%</th>
    <th>TS%</th>
    <th>AST/TO</th>
</tr>
{game_rows}
</table>
</div>

</div>
</body>
</html>
"""

    file_name = f"player_{player_id}_report.html"

    with open(file_name, "w") as f:
        f.write(html)

    print(f"Created {file_name}")
