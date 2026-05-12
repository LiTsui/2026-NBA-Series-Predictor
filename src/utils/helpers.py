#creates the regular_season_matchups file which keeps only regular_season_matchups between teams that are in the playoffs
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

def get_winner(high, low):
    return high