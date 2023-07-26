import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv('all_seasons_combined_df_2023-07-25_12-50-09.csv')
    df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna('None'))
    drop_cols = ['Unnamed: 0', 'shirtnumber']
    df = df.drop(drop_cols, axis=1)
    return df

def process_data(df):
    df['year'] = df['season'].str[:4]
    df['season_gameweek'] = df['year'] + '_' + df['gameweek'].astype(str)
    df = df[['player', 'team', 'season_gameweek', 'minutes', 'position_1'] + [col for col in df.columns if col not in ['player', 'team', 'season_gameweek', 'minutes', 'position_1']]]
    return df

def plot_data(df1, selected_columns, selected_item, item_type):
    if item_type == 'player':
        st.line_chart(df1[df1['player'] == selected_item][selected_columns])
    elif item_type == 'team':
        st.line_chart(df1[df1['team'] == selected_item][selected_columns])


def filter_and_group_data(df1, player_or_team, season, gameweek, position_1):
    df1 = df1[(df1['season'] == season) & (df1['gameweek'] == gameweek) & (df1['position_1'] == position_1)]
    df1 = df1.groupby(['player', 'team']).sum().reset_index()
    return df1

def main():
    st.title('My first app')    
    st.write("Here's our first attempt at using data to create a table:")
    df = load_data()
    df1 = process_data(df)
    st.write(df1)
    
    player_or_team = st.radio(label='player or team?', options=['player', 'team'])
    season = st.selectbox(label='Select a season', options=df['season'].unique())
    gameweek = st.slider(label='Select a gameweek', min_value=1, max_value=38, value=1, step=1)

    df1 = filter_and_group_data(df1, player_or_team, season, gameweek)

    if player_or_team == 'player':
        player_name = st.selectbox(label='Select a player', options=df1['player'].unique())
        st.write(df1[df1['player'] == player_name])
        columns_to_chart = st.multiselect(label='What columns do you want to chart?', options=df1.columns)
        plot_data(df1, columns_to_chart, player_name, 'player')
    elif player_or_team == 'team':
        team_name = st.selectbox(label='Select a team', options=df['team'].unique())
        st.write(df1[df1['team'] == team_name])
        columns_to_chart = st.multiselect(label='What columns do you want to chart?', options=df1.columns)
        plot_data(df1, columns_to_chart, team_name, 'team')

if __name__ == "__main__":
    main()