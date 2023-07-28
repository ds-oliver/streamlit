import pandas as pd
import numpy as np
import streamlit as st
import logging
import sys
import os
import time
import datetime

# Set up logging
def set_up_logs():
    """
    This function sets up the log file for the streamlit app.
    """
    # Set up the log file
    log_file_name = "streamlit_app_logs.log"
    log_file_path = os.path.join(os.getcwd(), log_file_name)
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s %(message)s')

    LOG_FILE_PATH = log_file_path

    return log_file_path, LOG_FILE_PATH

# Log the start of the app
def log_start_of_app(log_file_path):
    """
    This function logs the start of the streamlit app.
    """
    app_start_time = None
    app_end_time = None
    # log start time
    app_start_time = datetime.datetime.now()
    # Log the start of the app
    logging.info("Streamlit app started")

    return app_start_time, app_end_time

# Log the end of the app
def log_end_of_app(log_file_path, app_start_time):
    """
    This function logs the end of the streamlit app.
    """
    # log end time
    app_end_time = datetime.datetime.now()
    # Log the end of the app
    logging.info("Streamlit app ended")

    # log time elapsed
    time_elapsed = app_end_time - app_start_time
    logging.info("Time elapsed: {}".format(time_elapsed))

# Log the start of the function
def log_start_of_function(function_name):
    """
    This function logs the start of the function.
    """
    if function_start_time is not None and function_end_time is not None:
        function_start_time = None
        function_end_time = None
    else:
        # log start time
        function_start_time = datetime.datetime.now()
        # Log the start of the function
        logging.info("Function {} started".format(function_name))

    return function_start_time, function_end_time

# Log the end of the function
def log_end_of_function(function_name, function_start_time):
    """
    This function logs the end of the function.
    """
    # log end time
    function_end_time = datetime.datetime.now()
    # log time elapsed
    time_elapsed = function_end_time - function_start_time
    # Log the end of the function
    logging.info("Function {} ended".format(function_name))

# Log the start of the script
def log_start_of_script(script_name):
    """
    This function logs the start of the script.
    """
    script_start_time = None
    script_end_time = None

    script_start_time = datetime.datetime.now()
    # Log the start of the script
    logging.info("Script {} started".format(script_name))

    return script_start_time, script_end_time

# Log the end of the script
def log_end_of_script(script_name, script_start_time):
    """
    This function logs the end of the script.
    """
    # log end time
    script_end_time = datetime.datetime.now()

    # log time elapsed
    time_elapsed = script_end_time - script_start_time
    # Log the end of the script
    logging.info("Script {} ended".format(script_name))
