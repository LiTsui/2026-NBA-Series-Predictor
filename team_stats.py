from nba_api.stats.endpoints import leaguestandings, leaguedashteamstats
import pandas as pd

'''
team_stats.py 

Contains the team statistics for each playoff team such as OFF_RATING, DEF_RATING, NET_RATING, etc. as well as standings
'''

#team standings queried from nba api
standings = leaguestandings.LeagueStandings(season='2025-26')
standings_df = standings.get_data_frames()[0]

#team stats queried from nba api
team_stats = leaguedashteamstats.LeagueDashTeamStats(season='2025-26')
team_stats_df = team_stats.get_data_frames()[0]

#merge rows if they have common TeamID/TEAM_ID
full_team_df = standings_df.merge(
    team_stats_df,
    left_on="TeamID",
    right_on="TEAM_ID",
    how="inner"
)

#removes teams that did not make the 2026 playoffs
playoff_df = full_team_df[0:16]

print(playoff_df.to_string(index=False))