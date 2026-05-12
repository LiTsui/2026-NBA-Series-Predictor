import pandas as pd

'''
Use to compare stats in every single one of the playoffs
'''

def make_seed_matchup(playoff, conf, top_seed, low_seed):
    team1 = playoff[playoff['Conference'].str.contains(conf) & (playoff['PlayoffRank'] == top_seed)].iloc[0]
    team2 = playoff[playoff['Conference'].str.contains(conf) & (playoff['PlayoffRank'] == low_seed)].iloc[0]

    row = {
        'TEAM_NAME_HIGHER': team1['TEAM_NAME'],
        'TEAM_NAME_LOWER': team2['TEAM_NAME'],
        'CONFERENCE': conf,
        'SEED_HIGHER': team1['PlayoffRank'],
        'SEED_LOWER': team2['PlayoffRank'],
        'PointsPG_DIFF' : team1['PointsPG'] - team2['PointsPG'],
        'OppPointsPG_DIFF': team1['OppPointsPG'] - team2['OppPointsPG'],
        'DiffPointsPG_DIFF': team1['DiffPointsPG'] - team2['DiffPointsPG'],
        'E_OFF_RATING_DIFF': team1['E_OFF_RATING'] - team2['E_OFF_RATING'],
        'OFF_RATING_DIFF': team1['OFF_RATING'] - team2['OFF_RATING'],
        'E_DEF_RATING_DIFF': team1['E_DEF_RATING'] - team2['E_DEF_RATING'],
        'DEF_RATING_DIFF': team1['DEF_RATING'] - team2['DEF_RATING'],
        'E_NET_RATING_DIFF': team1['E_NET_RATING'] - team2['E_NET_RATING'],
        'NET_RATING_DIFF': team1['NET_RATING'] - team2['NET_RATING'],
        'AST_PCT_DIFF': team1['AST_PCT'] - team2['AST_PCT'],
        'AST_TO_DIFF': team1['AST_TO'] - team2['AST_TO'],
        'AST_RATIO_DIFF': team1['AST_RATIO'] - team2['AST_RATIO'],
        'OREB_PCT_DIFF': team1['OREB_PCT'] - team2['OREB_PCT'],
        'DREB_PCT_DIFF': team1['DREB_PCT'] - team2['DREB_PCT'],
        'REB_PCT_DIFF': team1['REB_PCT'] - team2['REB_PCT'],
        'TM_TOV_PCT_DIFF': team1['TM_TOV_PCT'] - team2['TM_TOV_PCT'],
        'EFG_PCT_DIFF': team1['EFG_PCT'] - team2['EFG_PCT'],
        'TS_PCT_DIFF': team1['TS_PCT'] - team2['TS_PCT'],
        'E_PACE_DIFF': team1['E_PACE'] - team2['E_PACE'],
        'PACE_DIFF': team1['PACE'] - team2['PACE'],
        'PIE_DIFF': team1['PIE'] - team2['PIE'],
    }

    return pd.DataFrame([row])

def build_round_matchups(playoff, round_name):
    rows = pd.DataFrame()

    pairings = None

    if round_name == 'round1':
        pairings = [
            ('West', 1, 8),
            ('West', 2, 7),
            ('West', 3, 6),
            ('West', 4, 5),
            ('East', 1, 8),
            ('East', 2, 7),
            ('East', 3, 6),
            ('East', 4, 5),
        ]

    for conf, high, low in pairings:
        rows = pd.concat([rows, make_seed_matchup(playoff, conf, high, low)])

    return rows

def build_next_round(playoff):
    # get winner from predict_series
    make_seed_matchup(playoff, 'next_round', 0, 0)
    None

def main():
    for i in range(1996, 2026):
        season = f'{str(i)[-2:]}_{str(i + 1)[-2:]}' # follow format 00_01, 09_10
        print(f'Creating Matchup Data for {i}-{str(i + 1)[-2:]}')
        playoff = pd.read_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/processed/playoff/playoff_{season}.csv')
        round1_matchups = build_round_matchups(playoff, 'round1')
        round1_matchups.to_csv(f'/Users/Sean/PycharmProjects/NBA_Series_Predictor/src/data/processed/round1_matchups/round1_matchups_{season}.csv', index=False)

        print(round1_matchups.to_string(index=False))

if __name__ == "__main__":
    main()