import streamlit as st
import pandas as pd
import numpy as np

st.title('My first app')    

st.write("Here's our first attempt at using data to create a table:")

df = pd.read_csv('/Users/hogan/Library/CloudStorage/Dropbox/Mac/Documents/GitHub/streamlit/all_seasons_combined_df_2023-07-25_12-50-09.csv')

st.write(df)

# plot the data

# columns_to_chart = st.multiselect(
#     label='What columns do you want to chart?',
#     options=df.columns)

# st.line_chart(df[columns_to_chart])

# select a player or team

player_or_team = st.radio(
    label='Player or Team?',
    options=['Player', 'Team'])
