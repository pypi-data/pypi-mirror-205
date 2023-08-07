import pandas as pd


def sort_rows_by_month(df: pd.DataFrame) -> pd.DataFrame:
    df.index = pd.to_datetime(df.index, format='%b %Y')
    df = df.sort_index(ascending=True)
    df.index = df.index.strftime('%b %Y')
    return df
