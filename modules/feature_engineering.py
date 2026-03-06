
def create_features(df):

    if "Revenue" in df.columns and "Cost" in df.columns:
        df["Profit"] = df["Revenue"] - df["Cost"]

    return df
