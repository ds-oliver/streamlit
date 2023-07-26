import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    list_of_files = ['specific-csvs/fdr-pts-vs.csv', 'specific-csvs/fdr_best.csv']

    # load the dataframes
    df_fdr_pts_vs = pd.read_csv(list_of_files[0])
    df_fdr_best = pd.read_csv(list_of_files[1])

    return df_fdr_pts_vs, df_fdr_best

