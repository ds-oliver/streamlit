import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    list_of_files = ['specific-csvs/fdr-pts-vs.csv', 'specific-csvs/fdr_best.csv']

    # load the dataframes
    df_fdr_pts_vs = pd.read_csv(list_of_files[0])
    df_fdr_best = pd.read_csv(list_of_files[1])

    # drop rank from df_fdr_pts_vs
    df_fdr_pts_vs = df_fdr_pts_vs.drop(['Rank', 'Sum'], axis=1)

    # drop code from df_fdr_best
    df_fdr_best = df_fdr_best.drop('Code', axis=1)

    # make sure team names are sorted alphabetically
    df_fdr_pts_vs = df_fdr_pts_vs.sort_values('Team')
    df_fdr_best = df_fdr_best.sort_values('Team')

    # set index to Team for both dataframes
    df_fdr_pts_vs = df_fdr_pts_vs.set_index('Team')
    df_fdr_best = df_fdr_best.set_index('Team')

    return df_fdr_pts_vs, df_fdr_best

def clean_pts_vs(df_fdr_pts_vs):
    # the expected points value is in the string value 'NOT (6.6)', so we need to extract the value between the brackets and convert it to a float, this should be done for all columns
    # copy the df
    df_fdr_xfpts = df_fdr_pts_vs.copy()

    for col in df_fdr_xfpts.columns:
        df_fdr_xfpts[col] = df_fdr_xfpts[col].str.extract(r'\((.*?)\)', expand=False).astype(float)

    return df_fdr_xfpts

def colorcode_pts_vs(df_fdr_xfpts, df_fdr_best):
    # df_fdr_best holds the team names and df_fdr_xfpts holds the expected points values that each indexed team will score against the team in the column, we need to compare the values in each column and color code the values in df_fdr_xfpts based on whether they are the highest value in the column or not
    # we will create a brand new dataframe to hold the color coded values
    df_fdr_color = df_fdr_xfpts.copy()

    # loop through each column in df_fdr_xfpts
    for col in df_fdr_xfpts.columns:
        # loop through each row in df_fdr_xfpts
        for index, row in df_fdr_xfpts.iterrows():
            # if the value in the row is equal to the max value in the column, then color code it green
            if row[col] == df_fdr_xfpts[col].max():
                df_fdr_color.loc[index, col] = 'background-color: #00FF00'
            # otherwise, color code it red
            else:
                df_fdr_color.loc[index, col] = 'background-color: #FF0000'

    return df_fdr_color


def show_tables(df_fdr_color):
    # slider for gameweeks which are represented by columns in the dataframe
    gameweek = st.slider('Gameweek', 1, 38, 1)

    # filter the dataframes by gameweek by truncating columns depending on slider selection
    df_fdr_color = df_fdr_color.iloc[:, :gameweek + 1]

    # set default slider value to 6 until it is changed

    # format text labels for the dataframes
    st.markdown('### xFPts Points vs')
    st.markdown('#### Gameweek(s): ' + str(gameweek))


    # show the dataframes
    st.write(df_fdr_color)


# main
def main():
    # load the dataframes
    df_fdr_pts_vs, df_fdr_best = load_data()

    # show the dataframes
    show_tables(df_fdr_color)

if __name__ == "__main__":
    main()
