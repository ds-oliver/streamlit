import streamlit as st
import pandas as pd
import numpy as np

# load these files
# df_2023-07-25_12-17-41_2022-2023.csv df_2023-07-25_11-44-56_2021-2022.csv df_2023-07-25_11-08-29_2020-2021.csv df_2023-07-25_10-32-44_2019-2020.csv df_2023-07-25_09-57-12_2018-2019.csv df_2023-07-25_09-57-10_2017-2018.csv

df_2022_2023 = pd.read_csv('/data/df_2023-07-25_12-17-41_2022-2023.csv')
df_2021_2022 = pd.read_csv('/data/df_2023-07-25_11-44-56_2021-2022.csv')
df_2020_2021 = pd.read_csv('/data/df_2023-07-25_11-08-29_2020-2021.csv')
df_2019_2020 = pd.read_csv('/data/df_2023-07-25_10-32-44_2019-2020.csv')
df_2018_2019 = pd.read_csv('/data/df_2023-07-25_09-57-12_2018-2019.csv')
df_2017_2018 = pd.read_csv('/data/df_2023-07-25_09-57-10_2017-2018.csv')

# create a list of dataframes
df_list = [df_2022_2023, df_2021_2022, df_2020_2021, df_2019_2020, df_2018_2019, df_2017_2018]

