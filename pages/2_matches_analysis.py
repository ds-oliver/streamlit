import streamlit as st
import pandas as pd
import numpy as np
import unidecode
import re
import uuid

# load these files
# df_2023-07-25_12-17-41_2022-2023.csv df_2023-07-25_11-44-56_2021-2022.csv df_2023-07-25_11-08-29_2020-2021.csv df_2023-07-25_10-32-44_2019-2020.csv df_2023-07-25_09-57-12_2018-2019.csv df_2023-07-25_09-57-10_2017-2018.csv

df_2022_2023 = pd.read_csv('data/df_2023-07-25_12-17-41_2022-2023.csv')
df_2021_2022 = pd.read_csv('data/df_2023-07-25_11-44-56_2021-2022.csv')
df_2020_2021 = pd.read_csv('data/df_2023-07-25_11-08-29_2020-2021.csv')
df_2019_2020 = pd.read_csv('data/df_2023-07-25_10-32-44_2019-2020.csv')
df_2018_2019 = pd.read_csv('data/df_2023-07-25_09-57-12_2018-2019.csv')
df_2017_2018 = pd.read_csv('data/df_2023-07-25_09-57-10_2017-2018.csv')

def clean_dataframes(df):
    drop_cols = ['score', 'match_report', 'notes']
    df = df.drop(drop_cols, axis=1)

    # reorder columns gameweek, home_team, home_score, home_xg, away_team, away_score, away_xg, date, season
    df = df[['gameweek', 'home_team', 'home_score', 'home_xg', 'away_team', 'away_score', 'away_xg', 'date', 'season']]

    # create a column for the winning_team, if draw then draw
    df['winning_team'] = np.where(df['home_score'] > df['away_score'], df['home_team'], np.where(df['home_score'] < df['away_score'], df['away_team'], 'draw'))

    # create a column for the losing_team, if draw then draw
    df['losing_team'] = np.where(df['home_score'] < df['away_score'], df['home_team'], np.where(df['home_score'] > df['away_score'], df['away_team'], 'draw'))

    # create match_id column which is applymap of home_team and away_team and season using uuid
    df['match_id'] = df[['home_team', 'away_team', 'season']].applymap(str).apply(lambda x: ''.join(x), axis=1).apply(lambda x: uuid.uuid5(uuid.NAMESPACE_DNS, x))

    return df

# create a list of dataframes
df_list = [df_2022_2023, df_2021_2022, df_2020_2021, df_2019_2020, df_2018_2019, df_2017_2018]

for df in df_list:
    df = clean_dataframes(df)

def main():
    """_summary_: This is the main function for the matches analysis page

    _description_: This page will be used to analyse the matches data

    _parameters_: None

    _returns_: None

    _example_: None
    """
    for df in df_list:
        df = clean_dataframes(df)

    # concatenate the dataframes
    df_all_seasons = pd.concat(df_list)