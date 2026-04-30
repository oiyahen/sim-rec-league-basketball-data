import random


def get_team_players(team_id, players_data):
    return [p for p in players_data if p["team_id"] == team_id]


def choose_players(team_id, players_data):
    roster = get_team_players(team_id, players_data)

    core_players = roster[:4]
    bench_players = roster[4:]

    number_of_players = random.randint(5, min(len(roster), 8))

    selected = core_players.copy()

    while len(selected) < number_of_players and bench_players:
        player = random.choice(bench_players)

        if player not in selected:
            selected.append(player)

    return selected


def split_points(total_points, players):
    points_left = total_points
    stat_lines = []

    for i, player in enumerate(players):
        players_left = len(players) - i

        if players_left == 1:
            pts = points_left
        else:
            max_pts = min(18, points_left)

            if max_pts <= 0:
                pts = 0
            else:
                pts = random.randint(0, max_pts)

            points_left -= pts

        if pts == 0:
            fgm = 0
            fga = random.randint(1, 6)
            three_pm = 0
            three_pa = random.randint(0, min(4, fga))
            ftm = 0
            fta = random.randint(0, 3)
        else:
            fgm = pts // 2
            fga = fgm + random.randint(2, 7)

            three_pm = random.randint(0, min(3, fgm))
            three_pa = three_pm + random.randint(0, 4)

            ftm = max(0, pts - (fgm * 2))
            fta = ftm + random.randint(0, 3)

        stat_lines.append({
            "game_id": None,
            "team_id": player["team_id"],
            "player_id": player["player_id"],
            "minutes": random.randint(10, 38),
            "pts": pts,
            "reb": random.randint(1, 10),
            "ast": random.randint(0, 6),
            "fgm": fgm,
            "fga": fga,
            "three_pm": three_pm,
            "three_pa": three_pa,
            "ftm": ftm,
            "fta": fta,
            "to": random.randint(0, 5),
            "pf": random.randint(0, 5),
            "stl": random.randint(0, 3),
            "blk": random.randint(0, 2)
        })

    return stat_lines


def generate_game_stats(games_data, players_data):
    all_stats = []

    for game in games_data:
        game_id = game["game_id"]

        team_a_id = game["team_a_id"]
        team_b_id = game["team_b_id"]

        team_a_score = game["team_a_score"]
        team_b_score = game["team_b_score"]

        team_a_players = choose_players(team_a_id, players_data)
        team_b_players = choose_players(team_b_id, players_data)

        team_a_stats = split_points(team_a_score, team_a_players)
        team_b_stats = split_points(team_b_score, team_b_players)

        for stat in team_a_stats + team_b_stats:
            stat["game_id"] = game_id
            all_stats.append(stat)

    return all_stats


# ONLY runs when you run this file directly
if __name__ == "__main__":
    from data import games_data, players_data

    generated_stats = generate_game_stats(games_data, players_data)

    print("player_game_stats_data = [")

    for stat in generated_stats:
        print(f"    {stat},")

    print("]")
