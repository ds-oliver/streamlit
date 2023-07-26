import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    list_of_files = ['specific-csvs/fdr-pts-vs.csv', 'specific-csvs/fdr_best.csv']

    # load the dataframes
    df_fdr_pts_vs = pd.read_csv(list_of_files[0])
    df_fdr_best = pd.read_csv(list_of_files[1])

    # drop rank from df_fdr_pts_vs
    df_fdr_pts_vs = df_fdr_pts_vs.drop('Rank', axis=1)

    # drop code from df_fdr_best
    df_fdr_best = df_fdr_best.drop('Code', axis=1)

    # set index to Team for both dataframes
    df_fdr_pts_vs = df_fdr_pts_vs.set_index('Team')
    df_fdr_best = df_fdr_best.set_index('Team')

    return df_fdr_pts_vs, df_fdr_best

def show_tables(df_fdr_pts_vs, df_fdr_best):
    # slider for gameweeks which are represented by columns in the dataframe
    gameweek = st.slider('Gameweek', 1, 38, 1)

    # filter the dataframes by gameweek by truncating columns depending on slider selection
    df_fdr_pts_vs = df_fdr_pts_vs.iloc[:, :gameweek + 1]
    df_fdr_best = df_fdr_best.iloc[:, :gameweek + 1]

    # show the dataframes
    st.write(df_fdr_pts_vs)
    st.write(df_fdr_best)

# main
def main():
    # load the dataframes
    df_fdr_pts_vs, df_fdr_best = load_data()

    # show the dataframes
    show_tables(df_fdr_pts_vs, df_fdr_best)

if __name__ == "__main__":
    main()
