import json
import pandas as pd

"""
Utility methods for extracting meaningful dataframes from dataset JSON files
"""

def path_to_pd(path: str) -> pd.DataFrame:
    # To get past 'trailing data' issue (not all in one entry)
    data = []
    with open(path, encoding='utf-8', mode='r') as f:
        for line in f:
            data.append(line)

    return pd.DataFrame(data)

def top_k_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return df of top k countries and their viewage
    """
    raise Exception('no impl')

if __name__ == "__main__":
    file_name = "sample_tiny.json"
    df = path_to_pd(f'./data/{file_name}')

    print(df.describe())