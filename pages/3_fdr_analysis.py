import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    list_of_files = ['specific-csvs/fdr-pts-vs.csv', 'specific-csvs/fdr_best.csv']

    # load the dataframes
    df_fdr_pts_vs = pd.read_csv(list_of_files[0])
    df_fdr_best = pd.read_csv(list_of_files[1])

    return df_fdr_pts_vs, df_fdr_best

def show_tables(df_fdr_pts_vs, df_fdr_best):
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
    