from datetime import timedelta

import numpy as np
import pandas as pd
import sqlalchemy
import os
from sqlalchemy import create_engine

base_dir = '/home/saiks/Datasets/'
# Bets
df_betting_odds = pd.read_csv(base_dir + 'betting-odds/E0.csv')
df_betting_odds = df_betting_odds[['Date', 'Time', 'HomeTeam', 'AwayTeam', 'B365H',	'B365D', 'B365A']]

# Premier League games
df_games_premiere_league = pd.read_csv(base_dir + 'games-premier-league/df_full_premierleague.csv')
df_games_premiere_league = df_games_premiere_league[['date', 'home_team', 'away_team', 'result_full',
                                                     'goal_home_ft', 'goal_away_ft']]

# Transfers
columns = ['club_name', 'player_name', 'position', 'club_involved_name', 'transfer_movement',
           'transfer_period', 'year', 'season']
df_transfers = pd.DataFrame(columns=columns)
for filename in os.listdir(base_dir + "transfers/data/2021"):
    df = pd.read_csv(base_dir + "transfers/data/2021/" + filename)
    df = df[columns]
    df_transfers = pd.concat([df_transfers, df], axis=0)

# Check which teams need to be renamed
df1 = pd.Series(pd.concat([df_betting_odds['HomeTeam'], df_betting_odds['HomeTeam']], axis=0).drop_duplicates(), name="Team1")
df1 = df1.reindex(df1.values)
df1 = pd.DataFrame(df1.index, index=df1.index, columns=['Team1'])
df2 = pd.Series(pd.concat([df_games_premiere_league['home_team'], df_games_premiere_league['away_team']], axis=0).drop_duplicates(), name="Team2")
df2 = df2.reindex(df2.values)
df2 = pd.DataFrame(df2.index, index=df2.index, columns=['Team2'])
df = pd.concat([df2, df1], axis=1)

# Rename teams in df_betting_odds
print("Rename following teams from df_betting_odds to be aligned with the ones in df_games_premiere_league: ")
print(df[df.Team2.isna()]['Team1'].values)
teams_remap = {'West Ham': 'West Ham United', 'West Brom': 'West Bromwich Albion', 'Tottenham': 'Tottenham Hotspur',
               'Brighton': 'Brighton and Hove Albion', 'Leeds': 'Leeds United', 'Man United': 'Manchester United',
               'Newcastle': 'Newcastle United', 'Leicester': 'Leicester City', 'Wolves': 'Wolverhampton Wanderers',
               'Man City': 'Manchester City'}
df_betting_odds.replace(teams_remap, inplace=True)

df_betting_odds.columns = [c.lower() for c in df_betting_odds.columns]
df_games_premiere_league.columns = [c.lower() for c in df_games_premiere_league.columns]
df_transfers.columns = [c.lower() for c in df_transfers.columns]

################################################################
# Create dfs in the structure of the football db schema tables #
################################################################

engine = create_engine('postgresql://saiks2022:saiks2022@saiks:5432/football')
engine.execute("Truncate contract, user_bet, bet, result, match, platformUser, player, team, stadium;")

# df_stadium = pd.DataFrame(columns=['id_stadium', 'full_name', 'capacity'])

df_team = pd.DataFrame(columns=['id_team', 'id_stadium', 'club', 'shorthand'])
df_team['id_team'] = np.arange(0, len(df2))
df_team['id_stadium'] = np.nan
df_team['club'] = df2.values
df_team['shorthand'] = np.nan
print("Insert into table team")
df_team.to_sql("team", engine, if_exists="append", index=False)

df_player = pd.DataFrame(columns=['id_player', 'name', 'kit', 'country'])
df_player['name'] = df_transfers['player_name']
df_player['id_player'] = np.arange(0, len(df_player))
df_player['kit'] = np.nan
df_player['country'] = np.nan
print("Insert into table player")
df_player.to_sql("player", engine, if_exists="append", index=False)

df_contract = df_transfers.merge(df_player, left_on='player_name',
                                 right_on="name").merge(df_team, left_on="club_name", right_on="club")
df_contract = df_contract[df_contract.transfer_movement == 'in']
df_contract = df_contract[['id_player', 'id_team', 'transfer_period', 'season', 'position', 'year']]
print("Insert into table contract")
df_contract.to_sql("contract", engine, if_exists="append", index=False)

df_match = df_games_premiere_league.merge(df_team, left_on="home_team", right_on="club")\
    .merge(df_team[['id_team', 'club']], left_on="away_team", right_on="club")
df_match.rename(columns={'id_team_x': 'id_home', 'id_team_y': 'id_away', 'date': 'date_time'}, inplace=True)
df_match['id_match'] = np.arange(0, len(df_match))
df_match['attendance'] = np.nan
print("Insert into table match")
df_match[['id_match', 'id_home', 'id_away', 'id_stadium', 'date_time', 'attendance']]\
    .to_sql("match", engine, if_exists="append", index=False)

df_result = df_match[['id_match', 'goal_home_ft', 'goal_away_ft']].copy()
df_result.rename(columns={'goal_home_ft': 'home', 'goal_away_ft': 'away'}, inplace=True)
print("Insert into table result")
df_result.to_sql('result', engine, if_exists="append", index=False)

# df_score = pd.DataFrame(columns=['id_score', 'id_match', 'id_team', 'goals'])

df_platformuser = pd.DataFrame(columns=['id_user', 'name'])
df_platformuser['id_user'] = ['000000', '000001', '000002']
df_platformuser['name'] = ['Nino', 'Bogdan', 'Filip']
print("Insert into table platformUser")
df_platformuser.to_sql('platformUser', engine, if_exists="append", index=False)

df_betting_odds['date'] = pd.to_datetime(df_betting_odds['date'])
df_match['date_time'] = pd.to_datetime(df_match['date_time'])
df_bet = df_match.merge(df_betting_odds, left_on=['date_time', 'home_team', 'away_team'],
                        right_on=['date', 'hometeam', 'awayteam'])
df_bet['id_bet'] = np.arange(0, len(df_bet))
df_bet.rename(columns={'b365h': 'home_win_odds', 'b365d': 'draw_odds', 'b365a': 'away_win_odds',
                       'date_time': 'bet_offered'}, inplace=True)
df_bet['betting_provider'] = 'b365'
df_bet['bet_offered'] = df_bet['date'] - timedelta(hours=32)
df_bet = df_bet[['id_bet', 'id_match', 'bet_offered', 'home_win_odds', 'draw_odds',
                 'away_win_odds', 'betting_provider']]
print("Insert into table bet")
df_bet.to_sql('bet', engine, if_exists="append", index=False)

df_user_bet = pd.DataFrame(columns=['id_user', 'id_bet', 'tip', 'tip_timestamp'])
