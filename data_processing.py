import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def filter_data(df, act_values):
    return df[df['act'].isin(act_values)]
