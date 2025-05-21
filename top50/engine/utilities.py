import pandas as pd
import os


# Eikon API Key
APP_KEY = '6d34900852224c0ea4ef375cd542d8359fc6a5c2'

df_Settings = pd.DataFrame()
dfConfiguration = pd.DataFrame()

def read_Settings():
    global df_Settings
    df_Settings = pd.read_csv("Settings.csv")
    df_Settings.set_index("Field", inplace=True)
    return df_Settings


def write_Settings():
    global df_Settings
    df_Settings.to_csv("Settings.csv")
    return


def readconfiguration():
    global dfConfiguration
    current_directory = os.getcwd()
    config_path = os.path.join('top50_improved', 'configuration.csv')  # or specify a full path if needed
    full_path = os.path.join(current_directory, config_path)
    try:
        df = pd.read_csv(full_path)
        print(df)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{full_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

