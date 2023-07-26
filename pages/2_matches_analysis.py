import streamlit as st
import pandas as pd
import numpy as np
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

# concatenate the dataframes
df_all_seasons = pd.concat(df_list)

def show_head2head_analysis():
    """_summary_: This is the function to show the head2head analysis

    _description_: This function will be used to show the head2head analysis

    _parameters_: None

    _returns_: None

    _example_: None
    """
    # create a list of seasons
    season_list = df_all_seasons['season'].unique().tolist()

    # create a list of teams
    team_list = df_all_seasons['home_team'].unique().tolist()

    # create a multiselect for teams
    team_selection = st.multiselect('Select teams', team_list)

    # create a multiselect for seasons
    season_selection = st.multiselect('Select seasons', season_list)

    # create a dataframe of the selected teams
    df_selected_teams = df_all_seasons[df_all_seasons['home_team'].isin(team_selection)]

    # create a dataframe of the selected seasons
    df_selected_seasons = df_all_seasons[df_all_seasons['season'].isin(season_selection)]

    # create a dataframe of the selected teams and seasons
    df_selected_teams_seasons = df_all_seasons[df_all_seasons['home_team'].isin(team_selection) & df_all_seasons['season'].isin(season_selection)]

    # create a dataframe of the head2head
    df_head2head = df_selected_teams_seasons.groupby(['home_team', 'away_team']).agg({'home_team': 'count', 'winning_team': 'count', 'losing_team': 'count'}).rename(columns={'home_team': 'total_matches', 'winning_team': 'total_wins', 'losing_team': 'total_losses'}).reset_index()

    # create a dataframe of the home wins
    df_home_wins = df_selected_teams_seasons[df_selected_teams_seasons['winning_team'] == df_selected_teams_seasons['home_team']].groupby(['home_team', 'away_team']).agg({'home_team': 'count'}).rename(columns={'home_team': 'home_wins'}).reset_index()

    # create a dataframe of the away wins
    df_away_wins = df_selected_teams_seasons[df_selected_teams_seasons['winning_team'] == df_selected_teams_seasons['away_team']].groupby(['home_team', 'away_team']).agg({'away_team': 'count'}).rename(columns={'away_team': 'away_wins'}).reset_index()

    # create a dataframe of the draws
    df_draws = df_selected_teams_seasons[df_selected_teams_seasons['winning_team'] == 'draw'].groupby(['home_team', 'away_team']).agg({'winning_team': 'count'}).rename(columns={'winning_team': 'draws'}).reset_index()

    # merge the dataframes
    df_head2head = df_head2head.merge(df_home_wins, how='left', on=['home_team', 'away_team']).merge(df_away_wins, how='left', on=['home_team', 'away_team']).merge(df_draws, how='left', on=['home_team', 'away_team'])

    # fill the NaN values with 0
    df_head2head = df_head2head.fillna(0)

    # create a column for the total goals
    df_head2head['total_goals'] = df_head2head['home_wins'] + df_head2head['away_wins'] + df_head2head['draws']

    # create a column for the home win percentage
    df_head2head['home_win_percentage'] = df_head2head['home_wins'] / df_head2head['total_matches']

    # create a column for the away win percentage
    df_head2head['away_win_percentage'] = df_head2head['away_wins'] / df_head2head['total_matches']

    # create a column for the draw percentage
    df_head2head['draw_percentage'] = df_head2head['draws'] / df_head2head['total_matches']

    # create a column for the home goals scored
    df_head2head['home_goals_scored'] = df_selected_teams_seasons.groupby(['home_team', 'away_team']).agg({'home_score': 'sum'}).rename(columns={'home_score': 'home_goals_scored'}).reset_index()['home_goals_scored']

    # create a column for the away goals scored
    df_head2head['away_goals_scored'] = df_selected_teams_seasons.groupby(['home_team', 'away_team']).agg({'away_score': 'sum'}).rename(columns={'away_score': 'away_goals_scored'}).reset_index()['away_goals_scored']

    # create a column for the home goals conceded
    df_head2head['home_goals_conceded'] = df_selected_teams_seasons.groupby(['home_team', 'away_team']).agg({'away_score': 'sum'}).rename(columns={'away_score': 'home_goals_conceded'}).reset_index()['home_goals_conceded']

    # create a column for the away goals conceded
    df_head2head['away_goals_conceded'] = df_selected_teams_seasons.groupby(['home_team', 'away_team']).agg({'home_score': 'sum'}).rename(columns={'home_score': 'away_goals_conceded'}).reset_index()['away_goals_conceded']

    # create a column for the total goals scored
    df_head2head['total_goals_scored'] = df_head2head['home_goals_scored'] + df_head2head['away_goals_scored']

    # create a column for the total goals conceded
    df_head2head['total_goals_conceded'] = df_head2head['home_goals_conceded'] + df_head2head['away_goals_conceded']

    # create a column for the goal difference
    df_head2head['goal_difference'] = df_head2head['total_goals_scored'] - df_head2head['total_goals_conceded']

    # create a column for the average goals scored
    df_head2head['average_goals_scored'] = df_head2head['total_goals_scored'] / df_head2head['total_matches']

    # create a column for the average goals conceded
    df_head2head['average_goals_conceded'] = df_head2head['total_goals_conceded'] / df_head2head['total_matches']




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

    # two 