import streamlit as st
import pandas as pd
import numpy as np

st.title('My first app')    

st.write("Here's our first attempt at using data to create a table:")

df = pd.read_csv('all_seasons_combined_df_2023-07-25_12-50-09.csv')

df = df.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x.fillna('None'))

drop_cols = ['Unnamed: 0', 'shirtnumber']

df1 = df.drop(drop_cols, axis=1)

# keep first four numbers of season column

df1['year'] = df1['season'].str[:4]

# create season_gameweek column

df1['season_gameweek'] = df1['year'] + '_' + df1['gameweek'].astype(str)

st.write(df)

# plot the data

# columns_to_chart = st.multiselect(
#     label='What columns do you want to chart?',
#     options=df.columns)

# st.line_chart(df[columns_to_chart])

# select a player or team

player_or_team = st.radio(
    label='player or team?',
    options=['player', 'team'])

if player_or_team == 'player':
    player_name = st.selectbox(
        label='Select a player',
        options=df['player'].unique())

    st.write(df[df['player'] == player_name])

    # plot the data

    columns_to_chart = st.multiselect(
        label='What columns do you want to chart?',
        options=df.columns)

    st.line_chart(df[df['player'] == player_name][columns_to_chart])

elif player_or_team == 'team':
    team_name = st.selectbox(
        label='Select a team',
        options=df['team'].unique())

    st.write(df[df['team'] == team_name])

    # plot the data

    columns_to_chart = st.multiselect(
        label='What columns do you want to chart?',
        options=df.columns)

    st.line_chart(df[df['team'] == team_name][columns_to_chart])