from nba_api.stats.endpoints import leaguegamefinder
from src.utils import helpers
import pandas as pd
import time

'''
Use to combine games in the playoffs and indicate which team won which matchups from 1996 to 2025. (Existing data to train off of) 
'''

for i in range(1996, 2026):
    season = f'{i}-{str(i + 1)[-2:]}'  # follow format 1996-97
    read_season = f'{str(i)[-2:]}_{str(i + 1)[-2:]}'

    print(f'Creating Matchup Data for {i}-{str(i + 1)[-2:]}')

    games = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        league_id_nullable='00',
        season_type_nullable='Playoffs'
    ).get_data_frames()[0]

    playoff = pd.read_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/processed/playoff/playoff_{read_season}.csv')
    round1 = pd.read_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/processed/round1_matchups/round1_matchups_{read_season}.csv')

    cleaned_matchups = helpers.clean_matchups(games, playoff)

    #print(cleaned_matchups.to_string(index=False))

    # need to figure out a way to figure out who won each matchup and the score for each matchup and return a new dataframe that shows the winner, loser, and score

    high = round1['TEAM_NAME_HIGHER']
    low = round1['TEAM_NAME_LOWER']

    time.sleep(5)
