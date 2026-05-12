import pandas as pd

#creates the playoffs file
def clean_standings(standings, team_stats):
    #merge rows if they have common TeamID/TEAM_ID
    playoff = standings.merge(
        team_stats,
        left_on="TeamID",
        right_on="TEAM_ID",
        how="inner"
    )

    #keep only the 16 playoff teams
    playoff = playoff[0:16]

    #correct the ranks
    playoff.iloc[15,7] = 7 #change Portland Trail Blazers to 7th seed
    playoff.iloc[13,7] = 8 #change Phoenix Suns to 8th seed

    #remove redundant or insignificant stats
    playoff = playoff.drop(columns=['TEAM_ID', 'GP', 'W', 'L', 'W_PCT', 'EliminatedConference',
                                    'EliminatedDivision', 'ClinchedConferenceTitle', 'ClinchedDivisionTitle',
                                    'ClinchIndicator', 'LeagueRank', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'PostAS', 'GP_RANK'])

    return playoff

#creates the matchups file
def clean_matchups(game_logs, playoff):
    #split dataframe into home and away teams
    away_df = game_logs[game_logs["MATCHUP"].str.contains("@")].copy()
    home_df = game_logs[game_logs["MATCHUP"].str.contains("vs.")].copy()

    #extract abbreviations of the opponent for each row
    away_df["OPP_ABBR"] = away_df["MATCHUP"].str.split().str[-1]
    home_df["OPP_ABBR"] = home_df["MATCHUP"].str.split().str[-1]

    #combine the home and away dataframes
    matchups = home_df.merge(
        away_df,
        left_on=["GAME_DATE", "OPP_ABBR", "TEAM_ABBREVIATION"],
        right_on=["GAME_DATE", "TEAM_ABBREVIATION", "OPP_ABBR"],
        suffixes=("_HOME", "_AWAY")
    )

    #remove teams that are not in the 2025-26 NBA playoffs
    matchups = matchups[
        matchups["TEAM_NAME_HOME"].isin(playoff["TEAM_NAME"]) &
        matchups["TEAM_NAME_AWAY"].isin(playoff["TEAM_NAME"])
    ]

    return matchups

def main():
    #team standings queried from nba api
    standings = pd.read_csv('raw/standings_25_26.csv')

    #team stats queried from nba api
    team_stats = pd.read_csv('raw/team_stats_25_26.csv')

    #game logs
    game_logs = pd.read_csv('raw/game_logs_25_26.csv')

    playoff = clean_standings(standings, team_stats)
    matchups = clean_matchups(game_logs, playoff)

    playoff.to_csv('processed/playoff_25_26.csv', index=False)
    matchups.to_csv('processed/matchups_25_26.csv', index=False)

    print('Data cleaned')

    # print dataframes for debugging
    print(playoff.to_string(index=False))
    print(matchups.to_string(index=False))

if __name__ == "__main__":
    main()