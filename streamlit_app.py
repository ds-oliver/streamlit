import streamlit as st
import pandas as pd
import numpy as np

st.title('My first app')    

st.write("Here's our first attempt at using data to create a table:")

df = pd.read_csv('/Users/hogan/dev/fbref/scripts/rfx_scrape/match_results_project/premierleague/test/output_files/csv_files/all_seasons_combined_df_2023-07-24_14-08-09.csv')

st.write(df)

# plot the data

st.line_chart(df)

