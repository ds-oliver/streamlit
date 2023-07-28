import streamlit as st
import pandas as pd
import numpy as np
# 1_load_data_from_dbt.py
import sys
import os

# Add the scripts directory to the Python path
sys.path.append('/Users/hogan/Library/CloudStorage/Dropbox/Mac/Documents/GitHub/streamlit/scripts')

from chunk_and_save_data import load_data_from_db

data = load_data_from_db()
st.write(data)