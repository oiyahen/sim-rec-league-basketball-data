#function file

#p = player
#g = game
#t = team

from data import games_data, teams_data, players_data, player_game_stats_data

#game highs function
def print_game_highs(game_id):

    # get the game
    game = next(g for g in games_data if g["game_id"] == game_id)

    team_ids = [game["team_a_id"], game["team_b_id"]]

    def get_player_info(player_id):
        for player in players_data:
            if player["player_id"] == player_id:
                return player["player_name"], player["jersey_number"]

    def get_team_name(team_id):
        for team in teams_data:
            if team["team_id"] == team_id:
                return team["team_name"]

    for team_id in team_ids:

        team_stats = [
            p for p in player_game_stats_data
            if p["team_id"] == team_id and p["game_id"] == game_id
        ]

        top_scorer = max(team_stats, key=lambda p: p["pts"])
        top_rebounder = max(team_stats, key=lambda p: p["reb"])
        top_passer = max(team_stats, key=lambda p: p["ast"])

        scorer_name, scorer_num = get_player_info(top_scorer["player_id"])
        rebound_name, rebound_num = get_player_info(top_rebounder["player_id"])
        passer_name, passer_num = get_player_info(top_passer["player_id"])

        team_name = get_team_name(team_id)

        print(f"\n{team_name} Game Highs")
        print(f"Points: #{scorer_num} {scorer_name} - {top_scorer['pts']} pts")
        print(f"Rebounds: #{rebound_num} {rebound_name} - {top_rebounder['reb']} reb")
        print(f"Assists: #{passer_num} {passer_name} - {top_passer['ast']} ast")

#team box score function
def print_team_box_score(game_id):

    # get the game
    game = next(g for g in games_data if g["game_id"] == game_id)

    team_ids = [game["team_a_id"], game["team_b_id"]]

    def get_team_name(team_id):
        for team in teams_data:
            if team["team_id"] == team_id:
                return team["team_name"]

    for team_id in team_ids:

        team_stats = [
            p for p in player_game_stats_data
            if p["team_id"] == team_id and p["game_id"] == game_id
        ]

        total_points = sum(p["pts"] for p in team_stats)
        total_rebounds = sum(p["reb"] for p in team_stats)
        total_assists = sum(p["ast"] for p in team_stats)

        total_fgm = sum(p["fgm"] for p in team_stats)
        total_fga = sum(p["fga"] for p in team_stats)
        fg_pct = (total_fgm / total_fga * 100) if total_fga != 0 else 0

        total_three_pm = sum(p["three_pm"] for p in team_stats)
        total_three_pa = sum(p["three_pa"] for p in team_stats)
        three_pct = (total_three_pm / total_three_pa * 100) if total_three_pa != 0 else 0

        total_ftm = sum(p["ftm"] for p in team_stats)
        total_fta = sum(p["fta"] for p in team_stats)
        ft_pct = (total_ftm / total_fta * 100) if total_fta != 0 else 0

        total_to = sum(p["to"] for p in team_stats)
        total_pf = sum(p["pf"] for p in team_stats)
        total_stl = sum(p["stl"] for p in team_stats)
        total_blk = sum(p["blk"] for p in team_stats)

        team_name = get_team_name(team_id)

        print(f"\n{team_name} Box Score")
        print("Points:", total_points)
        print("Rebounds:", total_rebounds)
        print("Assists:", total_assists)
        print(f"FG: {total_fgm}-{total_fga}, {fg_pct:.1f}%")
        print(f"3FG: {total_three_pm}-{total_three_pa}, {three_pct:.1f}%")
        print(f"FT: {total_ftm}-{total_fta}, {ft_pct:.1f}%")
        print("Blocks:", total_blk)
        print("Steals:", total_stl)
        print("Fouls:", total_pf)
        print("Turnovers:", total_to)

#player box score function
def print_player_box_score(game_id):

    def get_player_info(player_id):
        for player in players_data:
            if player["player_id"] == player_id:
                return player["player_name"], player["jersey_number"]

    def get_team_name(team_id):
        for team in teams_data:
            if team["team_id"] == team_id:
                return team["team_name"]

    game_stats = [
        p for p in player_game_stats_data
        if p["game_id"] == game_id
    ]

    print(f"\nPlayer Box Score - Game {game_id}")

    for stat in game_stats:
        player_name, jersey_number = get_player_info(stat["player_id"])
        team_name = get_team_name(stat["team_id"])

        print(
            f"#{jersey_number} {player_name} ({team_name}) | "
            f"MIN: {stat['minutes']} | "
            f"PTS: {stat['pts']} | "
            f"REB: {stat['reb']} | "
            f"AST: {stat['ast']} | "
            f"FG: {stat['fgm']}-{stat['fga']} | "
            f"3FG: {stat['three_pm']}-{stat['three_pa']} | "
            f"FT: {stat['ftm']}-{stat['fta']} | "
            f"STL: {stat['stl']} | "
            f"BLK: {stat['blk']} | "
            f"TO: {stat['to']} | "
            f"PF: {stat['pf']}"
        )

#standings function
def print_standings():

    standings = {}

    for team in teams_data:
        standings[team["team_id"]] = {"wins": 0, "losses": 0}

    for game in games_data:

        team_a = game["team_a_id"]
        team_b = game["team_b_id"]

        score_a = game["team_a_score"]
        score_b = game["team_b_score"]

        if score_a is None or score_b is None:
            continue

        if score_a > score_b:
            standings[team_a]["wins"] += 1
            standings[team_b]["losses"] += 1
        else:
            standings[team_b]["wins"] += 1
            standings[team_a]["losses"] += 1

    sorted_teams = sorted(
        teams_data,
        key=lambda team: standings[team["team_id"]]["wins"],
        reverse=True
    )

    print("\nSeason Standings:")

    for team in sorted_teams:
        team_id = team["team_id"]
        team_name = team["team_name"]

        wins = standings[team_id]["wins"]
        losses = standings[team_id]["losses"]


        print(f"{team_name}: {wins}-{losses}")

        

def print_game_summary(game_id):

    # get game
    game = next(g for g in games_data if g["game_id"] == game_id)

    team_a_id = game["team_a_id"]
    team_b_id = game["team_b_id"]

    team_a_name = next(t["team_name"] for t in teams_data if t["team_id"] == team_a_id)
    team_b_name = next(t["team_name"] for t in teams_data if t["team_id"] == team_b_id)

    score_a = game["team_a_score"]
    score_b = game["team_b_score"]

    # get records (reuse standings logic)
    standings = {}
    for team in teams_data:
        standings[team["team_id"]] = {"wins": 0, "losses": 0}

    for g in games_data:
        if g["team_a_score"] is None or g["team_b_score"] is None:
            continue

        if g["team_a_score"] > g["team_b_score"]:
            standings[g["team_a_id"]]["wins"] += 1
            standings[g["team_b_id"]]["losses"] += 1
        else:
            standings[g["team_b_id"]]["wins"] += 1
            standings[g["team_a_id"]]["losses"] += 1

    record_a = f"{standings[team_a_id]['wins']}-{standings[team_a_id]['losses']}"
    record_b = f"{standings[team_b_id]['wins']}-{standings[team_b_id]['losses']}"

    print(f"\n{team_a_name} {score_a} - {score_b} {team_b_name}")
    print(f"({record_a}){' ' * 15}({record_b})")

    print("\n------------------------------")
    print("GAME HIGHS")

    for team_id, team_name in [(team_a_id, team_a_name), (team_b_id, team_b_name)]:
        team_stats = [
            p for p in player_game_stats_data
            if p["team_id"] == team_id and p["game_id"] == game_id
        ]

        top_scorer = max(team_stats, key=lambda p: p["pts"])
        top_rebounder = max(team_stats, key=lambda p: p["reb"])
        top_passer = max(team_stats, key=lambda p: p["ast"])

        scorer = next(p for p in players_data if p["player_id"] == top_scorer["player_id"])
        rebounder = next(p for p in players_data if p["player_id"] == top_rebounder["player_id"])
        passer = next(p for p in players_data if p["player_id"] == top_passer["player_id"])

        print(f"\n{team_name}")
        print(f"Points: #{scorer['jersey_number']} {scorer['player_name']} - {top_scorer['pts']} pts")
        print(f"Rebounds: #{rebounder['jersey_number']} {rebounder['player_name']} - {top_rebounder['reb']} reb")
        print(f"Assists: #{passer['jersey_number']} {passer['player_name']} - {top_passer['ast']} ast")

    # team stats
    team_a_stats = [p for p in player_game_stats_data if p["team_id"] == team_a_id and p["game_id"] == game_id]
    team_b_stats = [p for p in player_game_stats_data if p["team_id"] == team_b_id and p["game_id"] == game_id]

    def total(stat, key):
        return sum(p[key] for p in stat)

    print("\n------------------------------")
    print("TEAM STATS")

    def total(stats, key):
        return sum(p[key] for p in stats)

    def pct(made, attempts):
        return (made / attempts * 100) if attempts > 0 else 0

    # Team A totals
    fgm_a = total(team_a_stats, "fgm")
    fga_a = total(team_a_stats, "fga")
    three_pm_a = total(team_a_stats, "three_pm")
    three_pa_a = total(team_a_stats, "three_pa")
    ftm_a = total(team_a_stats, "ftm")
    fta_a = total(team_a_stats, "fta")

    # Team B totals
    fgm_b = total(team_b_stats, "fgm")
    fga_b = total(team_b_stats, "fga")
    three_pm_b = total(team_b_stats, "three_pm")
    three_pa_b = total(team_b_stats, "three_pa")
    ftm_b = total(team_b_stats, "ftm")
    fta_b = total(team_b_stats, "fta")

    print(f"Points:    {total(team_a_stats, 'pts')} | {total(team_b_stats, 'pts')}")
    print(f"Rebounds:  {total(team_a_stats, 'reb')} | {total(team_b_stats, 'reb')}")
    print(f"Assists:   {total(team_a_stats, 'ast')} | {total(team_b_stats, 'ast')}")
    print(f"FG:        {fgm_a}-{fga_a} ({pct(fgm_a, fga_a):.1f}%) | {fgm_b}-{fga_b} ({pct(fgm_b, fga_b):.1f}%)")
    print(f"3FG:       {three_pm_a}-{three_pa_a} ({pct(three_pm_a, three_pa_a):.1f}%) | {three_pm_b}-{three_pa_b} ({pct(three_pm_b, three_pa_b):.1f}%)")
    print(f"FT:        {ftm_a}-{fta_a} ({pct(ftm_a, fta_a):.1f}%) | {ftm_b}-{fta_b} ({pct(ftm_b, fta_b):.1f}%)")
    print(f"Steals:    {total(team_a_stats, 'stl')} | {total(team_b_stats, 'stl')}")
    print(f"Blocks:    {total(team_a_stats, 'blk')} | {total(team_b_stats, 'blk')}")
    print(f"Turnovers: {total(team_a_stats, 'to')} | {total(team_b_stats, 'to')}")
    print(f"Fouls:     {total(team_a_stats, 'pf')} | {total(team_b_stats, 'pf')}")

    print("\n------------------------------")
    print("PLAYER BOX SCORES\n")

    def format_player_line(stat):
        player = next(p for p in players_data if p["player_id"] == stat["player_id"])

        return (
            f"#{player['jersey_number']} {player['player_name']} | "
            f"MIN {stat['minutes']} | "
            f"PTS {stat['pts']} | "
            f"REB {stat['reb']} | "
            f"AST {stat['ast']} | "
            f"FG {stat['fgm']}-{stat['fga']} | "
            f"3FG {stat['three_pm']}-{stat['three_pa']} | "
            f"FT {stat['ftm']}-{stat['fta']} | "
            f"STL {stat['stl']} | "
            f"BLK {stat['blk']} | "
            f"TO {stat['to']} | "
            f"PF {stat['pf']}"
        )

    print(f"{team_a_name:<80} | {team_b_name}")

    max_len = max(len(team_a_stats), len(team_b_stats))

    for i in range(max_len):

        left = ""
        right = ""

        if i < len(team_a_stats):
            left = format_player_line(team_a_stats[i])

        if i < len(team_b_stats):
            right = format_player_line(team_b_stats[i])

        print(f"{left:<80} | {right}")
