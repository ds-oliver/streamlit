import streamlit as st
import pandas as pd
import numpy as np
import re
import uuid

# load these files
# df_2023-07-25_12-17-41_2022-2023.csv df_2023-07-25_11-44-56_2021-2022.csv df_2023-07-25_11-08-29_2020-2021.csv df_2023-07-25_10-32-44_2019-2020.csv df_2023-07-25_09-57-12_2018-2019.csv df_2023-07-25_09-57-10_2017-2018.csv

def clean_dataframes(df):
    """Description: This function cleans the dataframes by removing unnecessary columns, reordering columns, creating new columns and renaming columns.
    
        Arguments:
            df {dataframe} -- dataframe to be cleaned
        
        Returns:
            df {dataframe} -- cleaned dataframe

    """
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

    # ifna() 0
    df = df.fillna(0)

    return df


def show_head2head_analysis(df_all_seasons):
    # create a list of seasons
    season_list = df_all_seasons['season'].unique().tolist()

    # create a list of teams
    team_list = df_all_seasons['home_team'].unique().tolist()

    # create two selectboxes for the two teams
    team_selection1 = st.selectbox('Select first team', team_list)
    team_selection2 = st.selectbox('Select second team', [team for team in team_list if team != team_selection1])

    # ensure the two selected teams are not the same
    while team_selection1 == team_selection2:
        st.error("Please select two different teams.")
        team_selection2 = st.selectbox('Select second team', [team for team in team_list if team != team_selection1])

    # show message that by default all seasons are selected and show unique seasons values in this message
    st.info(f"By default, all seasons are selected. To filter by season, check the box below and select the season(s) you want to filter by. The seasons available are: {', '.join(map(str, reversed(season_list)))}")


    # add a toggle button to decide whether to filter by season or not
    filter_by_season = st.checkbox('Filter by season')

    if filter_by_season:
        # create a multiselect for seasons
        season_selection = st.multiselect('Select season(s)', season_list)
    else:
        season_selection = season_list  # if not filtered by season, include all seasons

    # select matches where the selected teams faced each other and in the selected seasons
    df_selected_teams_seasons = df_all_seasons[((df_all_seasons['home_team'] == team_selection1) & (df_all_seasons['away_team'] == team_selection2) | (df_all_seasons['home_team'] == team_selection2) & (df_all_seasons['away_team'] == team_selection1)) & (df_all_seasons['season'].isin(season_selection))]


    df_selected_teams_seasons['winner'] = np.where(df_selected_teams_seasons['home_score'] > df_selected_teams_seasons['away_score'], df_selected_teams_seasons['home_team'], df_selected_teams_seasons['away_team'])
    df_selected_teams_seasons['loser'] = np.where(df_selected_teams_seasons['home_score'] < df_selected_teams_seasons['away_score'], df_selected_teams_seasons['home_team'], df_selected_teams_seasons['away_team'])
    df_selected_teams_seasons.loc[df_selected_teams_seasons['home_score'] == df_selected_teams_seasons['away_score'], ['winner', 'loser']] = 'Draw'

    team1_stats = {
        'Wins': (df_selected_teams_seasons['winner'] == team_selection1).sum(),
        'Losses': (df_selected_teams_seasons['loser'] == team_selection1).sum(),
        'Draws': ((df_selected_teams_seasons['home_team'] == team_selection1) & (df_selected_teams_seasons['winner'] == 'Draw')).sum(),
        'Goals For': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection1, 'home_score'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection1, 'away_score'].sum(),
        'Goals Against': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection1, 'away_score'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection1, 'home_score'].sum(),
        # expected goals for and against using the _xg columns
        'xG For': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection1, 'home_xg'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection1, 'away_xg'].sum(),
        'xG Against': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection1, 'away_xg'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection1, 'home_xg'].sum(),
        # clean sheets are recorded when a team does not concede a goal in a match
        'Clean Sheets': ((df_selected_teams_seasons['home_team'] == team_selection1) & (df_selected_teams_seasons['away_score'] == 0)).sum() + ((df_selected_teams_seasons['away_team'] == team_selection1) & (df_selected_teams_seasons['home_score'] == 0)).sum(),
    }

    team2_stats = {
        'Wins': (df_selected_teams_seasons['winner'] == team_selection2).sum(),
        'Losses': (df_selected_teams_seasons['loser'] == team_selection2).sum(),
        'Draws': ((df_selected_teams_seasons['home_team'] == team_selection2) & (df_selected_teams_seasons['winner'] == 'Draw')).sum(),
        'Goals For': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection2, 'home_score'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection2, 'away_score'].sum(),
        'Goals Against': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection2, 'away_score'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection2, 'home_score'].sum(),
        # expected goals for and against using the _xg columns
        'xG For': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection2, 'home_xg'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection2, 'away_xg'].sum(),
        'xG Against': df_selected_teams_seasons.loc[df_selected_teams_seasons['home_team'] == team_selection2, 'away_xg'].sum() + df_selected_teams_seasons.loc[df_selected_teams_seasons['away_team'] == team_selection2, 'home_xg'].sum(),
        # clean sheets are recorded when a team does not concede a goal in a match
        'Clean Sheets': ((df_selected_teams_seasons['home_team'] == team_selection2) & (df_selected_teams_seasons['away_score'] == 0)).sum() + ((df_selected_teams_seasons['away_team'] == team_selection2) & (df_selected_teams_seasons['home_score'] == 0)).sum(),
    }

    for k, v in team2_stats.items():
        print(f"Key: {k}, Value: {v}, Type of value: {type(v)}, Type of corresponding value in team1_stats: {type(team1_stats[k])}")

    df_head2head = pd.DataFrame({team_selection1: team1_stats, team_selection2: team2_stats})

    # display the dataframe
    st.dataframe(df_head2head)


def main():
    """_summary_: main function to run the app

    _param_: None

    _return_: None

    """
    df_2022_2023 = pd.read_csv('data/df_2023-07-25_12-17-41_2022-2023.csv')
    df_2021_2022 = pd.read_csv('data/df_2023-07-25_11-44-56_2021-2022.csv')
    df_2020_2021 = pd.read_csv('data/df_2023-07-25_11-08-29_2020-2021.csv')
    df_2019_2020 = pd.read_csv('data/df_2023-07-25_10-32-44_2019-2020.csv')
    df_2018_2019 = pd.read_csv('data/df_2023-07-25_09-57-12_2018-2019.csv')
    df_2017_2018 = pd.read_csv('data/df_2023-07-25_09-57-10_2017-2018.csv')

    df_list = [df_2022_2023, df_2021_2022, df_2020_2021, df_2019_2020, df_2018_2019, df_2017_2018]

    df_list_cleaned = [clean_dataframes(df) for df in df_list]

    # concatenate the cleaned dataframes
    df_all_seasons = pd.concat(df_list_cleaned)

    show_head2head_analysis(df_all_seasons) 


if __name__ == "__main__":
    main()