import streamlit as st
import pandas as pd
import numpy as np
import re
import uuid

@st.cache_data
def load_player_data():
    player_df = pd.read_csv('data/all_seasons_combined_df_2023-07-25_12-50-09.csv')
    player_df = player_df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna('None'))
    drop_cols = ['Unnamed: 0', 'shirtnumber']
    player_df = player_df.drop(drop_cols, axis=1)
    return player_df

@st.cache_data
def process_player_data(player_df):
    player_df['year'] = player_df['season'].str[:4]
    player_df = player_df.rename(columns={'season': 'season_long', 'year': 'season', 'position_1': 'position'})

    conditions = [
        (player_df['home'] == True),
        (player_df['home'] == False)
    ]

    choices_team = [player_df['team'], player_df['opponent']]
    choices_opponent = [player_df['opponent'], player_df['team']]

    player_df['home_team'] = np.select(conditions, choices_team)
    player_df['away_team'] = np.select(conditions, choices_opponent)

    # create merge_key which is home_team + away_team + year
    player_df['matchup_merge_key'] = player_df.apply(lambda row: '_'.join(sorted([row['home_team'], row['away_team']])), axis=1)

    # create season_merge_key which is sorted home_team + away_team + season
    player_df['season_merge_key'] = player_df.apply(lambda row: '_'.join(sorted([row['home_team'], row['away_team']] + [row['season']])), axis=1)


    # player_df['season_merge_key'] = player_df['matchup_merge_key'] + player_df['season']

    player_df['season_gameweek'] = player_df['season'] + '_' + player_df['gameweek'].astype(str)
    cols_order = ['player', 'team', 'season_gameweek', 'minutes', 'position'] + [col for col in player_df.columns if col not in ['player', 'team', 'season_gameweek', 'minutes', 'position']]
    player_df = player_df[cols_order]

    return player_df

@st.cache_data
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

    df['matchup_merge_key'] = df[['home_team', 'away_team']].applymap(str).apply(lambda x: ''.join(x), axis=1).apply(lambda x: uuid.uuid5(uuid.NAMESPACE_DNS, x))
    df['season_merge_key'] = df[['home_team', 'away_team', 'season']].applymap(str).apply(lambda x: ''.join(x), axis=1).apply(lambda x: uuid.uuid5(uuid.NAMESPACE_DNS, x))

    # ifna() 0
    df = df.fillna(0)

    return df

@st.cache_data(allow_output_mutation=True)
def get_top_players(team, player_df, stat, top=5):
    """
    Get the top players from a team for a given statistic.

    Parameters:
    team (str): The team to get players from.
    player_df (DataFrame): The player data.
    stat (str): The statistic to rank players by.
    top (int): The number of top players to return.

    Returns:
    DataFrame: A DataFrame with the top players and their stats.
    """
    # check if team column exists in player_df
    if 'team' not in player_df.columns:
        raise ValueError('team column not in player_df')
    else:
        # Filter dataframe based on team
        player_df_team = player_df[player_df['team'] == team]

        # Top players by matchup
        top_players_matchup = player_df_team.groupby(['player']).agg({stat: 'sum'}).sort_values(by=stat, ascending=False).head(top)

        # Top players by season
        top_players_season = player_df_team.groupby(['player']).agg({stat: 'sum'}).sort_values(by=stat, ascending=False).head(top)

    return top_players_matchup, top_players_season



@st.cache_data(allow_output_mutation=True)
def get_teams_stats(df, team1, team2):
    """
    Get the stats for two teams for a specific matchup_merge_key.

    Parameters:
    df (DataFrame): The DataFrame to get the stats from.
    team1 (str): The first team to get stats for.
    team2 (str): The second team to get stats for.

    Returns:
    dict, dict: Two dictionaries with the statistics for the two teams.
    """
    # Initialize stats dictionaries
    stats_team1 = {
        'total_games': 0,
        'total_wins': 0,
        'total_losses': 0,
        'total_goals_scored': 0,
        'total_goals_conceded': 0,
        'xG For': 0,
        'xG Against': 0,
        'Clean Sheets': 0
    }
    stats_team2 = {
        'total_games': 0,
        'total_wins': 0,
        'total_losses': 0,
        'total_goals_scored': 0,
        'total_goals_conceded': 0,
        'xG For': 0,
        'xG Against': 0,
        'Clean Sheets': 0
    }

    # Filter df for games with team1 and team2
    df_filtered = df[(df['home_team'].isin([team1, team2])) & (df['away_team'].isin([team1, team2]))]

    for index, row in df_filtered.iterrows():
        if row['home_team'] == team1:
            stats_team1['total_games'] += 1
            stats_team1['total_goals_scored'] += row['home_score']
            stats_team1['total_goals_conceded'] += row['away_score']
            stats_team1['xG For'] += row['home_xg']
            stats_team1['xG Against'] += row['away_xg']
            if row['away_score'] == 0:
                stats_team1['Clean Sheets'] += 1
            if row['winning_team'] == team1:
                stats_team1['total_wins'] += 1
            elif row['winning_team'] == 'draw':
                continue
            else:
                stats_team1['total_losses'] += 1
                
        if row['home_team'] == team2:
            stats_team2['total_games'] += 1
            stats_team2['total_goals_scored'] += row['home_score']
            stats_team2['total_goals_conceded'] += row['away_score']
            stats_team2['xG For'] += row['home_xg']
            stats_team2['xG Against'] += row['away_xg']
            if row['away_score'] == 0:
                stats_team2['Clean Sheets'] += 1
            if row['winning_team'] == team2:
                stats_team2['total_wins'] += 1
            elif row['winning_team'] == 'draw':
                continue
            else:
                stats_team2['total_losses'] += 1

    return stats_team1, stats_team2

def show_head2head_analysis(df_all_seasons, player_df):
    # Create a list of teams
    team_list = sorted(df_all_seasons['home_team'].unique().tolist())

    # Create two selectboxes for the two teams
    team_selection1 = st.selectbox('Select Primary Team', team_list)
    team_selection2 = st.selectbox('Select Opponent', [team for team in team_list if team != team_selection1])

    # Apply the filter for both teams in all seasons
    df_filtered = df_all_seasons[(df_all_seasons['home_team'].isin([team_selection1, team_selection2])) & 
                                 (df_all_seasons['away_team'].isin([team_selection1, team_selection2]))]

    # Apply the statistics function to the filtered DataFrame
    team1_stats, team2_stats = get_teams_stats(df_filtered, team_selection1, team_selection2)

    # Convert the dictionaries to a DataFrame for visualization
    df_stats = pd.DataFrame({team_selection1: team1_stats, team_selection2: team2_stats})

    # Display the DataFrame
    st.dataframe(df_stats)

    stat_list = [col for col in player_df.columns if (player_df[col].dtype == 'float64' or player_df[col].dtype == 'int64')]

    default_stats = ['npxg', 'sca', 'gca']
    default_stats = [stat for stat in default_stats if stat in stat_list]

    # Let the user select a stat
    selected_stats = st.multiselect('Select player stat', stat_list, default=default_stats)

    # If no stat is selected, use the default stats
    if not selected_stats:
        selected_stats = default_stats
        
    st.dataframe(player_df)


# Get top 5 players for each team
    for stat in selected_stats:
        top5_team1, top5_season_team1 = get_top_players(team_selection1, player_df, stat, top=5)
        top5_team2, top5_season_team2 = get_top_players(team_selection2, player_df, stat, top=5)

        # Display the top 5 players
        st.subheader(f'Top 5 {team_selection1} players by {stat}:')
        st.dataframe(top5_team1)
        st.subheader(f'Top 5 {team_selection2} players by {stat}:')
        st.dataframe(top5_team2)

def main():
    # Load and process player data
    player_df = load_player_data()
    player_df = process_player_data(player_df)

    # Load and clean match data
    df_1992_2016 = pd.read_csv('data/historical_matches_reports-1992-2016.csv')
    df_2022_2023 = pd.read_csv('data/df_2023-07-25_12-17-41_2022-2023.csv')
    df_2021_2022 = pd.read_csv('data/df_2023-07-25_11-44-56_2021-2022.csv')
    df_2020_2021 = pd.read_csv('data/df_2023-07-25_11-08-29_2020-2021.csv')
    df_2019_2020 = pd.read_csv('data/df_2023-07-25_10-32-44_2019-2020.csv')
    df_2018_2019 = pd.read_csv('data/df_2023-07-25_09-57-12_2018-2019.csv')
    df_2017_2018 = pd.read_csv('data/df_2023-07-25_09-57-10_2017-2018.csv')

    df_all_seasons = pd.concat([df_2022_2023, df_2021_2022, df_2020_2021, df_2019_2020, df_2018_2019, df_2017_2018, df_1992_2016])
    df_all_seasons = clean_dataframes(df_all_seasons)

    # Show head to head analysis
    show_head2head_analysis(df_all_seasons, player_df)

if __name__ == "__main__":
    main()