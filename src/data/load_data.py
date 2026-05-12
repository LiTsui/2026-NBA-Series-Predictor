from nba_api.stats.endpoints import leaguestandings, leaguedashteamstats, leaguegamefinder
import time

'''
Use to load data in every single one of the playoffs
'''

# load standings, team stats, game logs from each season in the NBA
def load(season):

    # get league standings
    standings = leaguestandings.LeagueStandings(season=season)
    standings_df = standings.get_data_frames()[0]
    standings_df.to_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/raw/standings/standings_{season[2:4]}_{season[-2:]}.csv', index=False)

    # get team stats
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Advanced'
    )
    team_stats_df = team_stats.get_data_frames()[0]
    team_stats_df.to_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/raw/team_stats/team_stats_{season[2:4]}_{season[-2:]}.csv', index=False)

    # game logs for each game in the season (according to team)
    games = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable='Regular Season',
        player_or_team_abbreviation='T' #team
    )
    games_df = games.get_data_frames()[0]
    games_df.to_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/raw/game_logs/game_logs_{season[2:4]}_{season[-2:]}.csv', index=False)

# load all data for all seasons from 1996 to 2025 where 1996 is the start of the play by play era
def main():
    for i in range(1996, 2026):
        season = f'{i}-{str(i + 1)[-2:]}' # follow format 2000-01, 2009-10

        print(f'Loading {season}')

        load(season)

        print('Raw data saved')

        time.sleep(5)  # necessary to avoid time out

if __name__ == '__main__':
    main()