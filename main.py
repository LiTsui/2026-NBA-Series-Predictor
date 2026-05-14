from nba_api.stats.endpoints import commonplayoffseries

new = commonplayoffseries.CommonPlayoffSeries(season='1996-97')
new_df = new.get_data_frames()[0]
print(new_df.to_string(index=False))