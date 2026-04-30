# Rec League Basketball Analytics Project

## Overview

This project simulates a full basketball analytics workflow for a men's recreational league, designed to mirror how real analytics teams transform raw data into meaningful insights. Instead of manually reviewing box scores, this system ingests structured game data and automatically generates player, team, and league-level reports.

The goal is to bridge the gap between raw statistics and decision-making by building a repeatable pipeline that aggregates, analyzes, and visualizes performance data. This includes everything from basic stat tracking to more advanced efficiency metrics and player-level breakdowns.

By combining data modeling, analytical logic, and HTML-based reporting, this project demonstrates how data can be turned into clear, actionable insights for coaches, players, and analysts.

---

## Core Concept

Raw stats → Structured data → Aggregated insights → Visual reports

---

## Project Structure

data.py         # Stores all data (teams, players, games, stats)
gen_stats.py    # Generates sample data (one-time use)
reports.py      # All report generation logic (HTML output)
main.py         # Entry point for running reports
README.md       # Documentation

---

## Data Model

Core Entities:
- teams
- players
- games
- player_game_stats

Each stat record links:
game_id + team_id + player_id

---

## Reports

### Game Report
- Final score
- Team stats
- Player box scores

### Team Overview Report
- Offensive & defensive metrics
- Shooting efficiency
- Turnover trends

### League Leaders Report
- Top 5 players by key stats
- Filters for games played & attempts

### Roster Season Report
- Team-level player breakdown
- Leaders and averages

### Player Report (Advanced)

Includes:
- Player profile (team, record, GP)
- Career highs
- Season averages
- Advanced metrics:
  - FG%, 2P%, 3P%
  - eFG%, TS%
  - AST/TO
  - Offensive / Defensive / Net Rating (estimated)

#### Shooting Profile
- Inside Arc vs Outside Arc visualization
- Uses real 2PT and 3PT data
- Color-coded efficiency:
  - Hot (60%+)
  - Warm (50–59%)
  - Normal (40–49%)
  - Chill (30–39%)
  - Cold (<30%)

---

## Key Concepts

- Aggregation: sum(stats) ÷ games
- Filtering: minimum games & attempts
- Efficiency metrics: TS%, eFG%
- Possession-based estimates for ratings

---

## Output Format

Reports are generated in HTML:
- Clean visual layout
- Easy to open/share
- Printable

---

## How to Run

In main.py:

from reports import export_player_report

export_player_report(1)

---

## Future Improvements

- Real shot tracking (true shot charts)
- Advanced metrics (PER, usage rate)
- Trend analysis over time
- Database integration
- Interactive dashboard (Streamlit)

---

## Goal

Demonstrate:
- Data modeling
- Analytical thinking
- Report generation
- Turning raw data into insights
