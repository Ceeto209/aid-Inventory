import pandas as pd

def read_csv(file_path):
    return pd.read_csv(file_path)

def extract_characters_from_csv(file_path, column_name):
    df = read_csv(file_path)
    return df[column_name].tolist()

def extract_items_to_delete_from_csv(file_path, column_name):
    df = pd.read_csv(file_path)
    return df[column_name].tolist()
