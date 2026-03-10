import pandas as pd


def clean_dataframe(df):

    df = df.copy()

    df.columns = [col.strip() for col in df.columns]

    df.drop_duplicates(inplace=True)

    df.fillna("Unknown", inplace=True)

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    for col in df.columns:
        if "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except:
                pass

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    return df