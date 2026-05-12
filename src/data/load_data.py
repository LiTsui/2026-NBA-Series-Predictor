from nba_api.stats.endpoints import leaguestandings, leaguedashteamstats, leaguegamefinder

season = "2025-26"

# get league standings
standings = leaguestandings.LeagueStandings(season=season)
standings_df = standings.get_data_frames()[0]
standings_df.to_csv("raw/standings_25_26.csv", index=False)

# get team stats
team_stats = leaguedashteamstats.LeagueDashTeamStats(
    season=season,
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Advanced"
)
team_stats_df = team_stats.get_data_frames()[0]
team_stats_df.to_csv("raw/team_stats_25_26.csv", index=False)

# game logs for each game in the 2025-26 season (according to team)
games = leaguegamefinder.LeagueGameFinder(
    season_nullable=season,
    season_type_nullable='Regular Season',
    player_or_team_abbreviation='T' #team
)
games_df = games.get_data_frames()[0]
games_df.to_csv("raw/game_logs_25_26.csv", index=False)
print('Raw data saved')