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

# Create dfs in the structure of the football db schema tables
df_team = pd.DataFrame(columns=['id_team', 'id_stadium', 'club', 'shorthand'])
df_team['id_team'] = np.arange(0, len(df2))
df_team['id_stadium'] = np.nan
df_team['club'] = df2.values
df_team['shorthand'] = np.nan

engine = create_engine('postgresql://saiks2022:saiks2022@saiks:5432/football')
df_team.to_sql("team", engine, if_exists="append", index=False)
