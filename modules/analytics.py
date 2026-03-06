
def compute_kpis(df):

    kpis = {}

    if "Revenue" in df.columns:
        kpis["Total Revenue"] = float(df["Revenue"].sum())

    if "Profit" in df.columns:
        kpis["Total Profit"] = float(df["Profit"].sum())

    if "Customer_ID" in df.columns:
        kpis["Customers"] = int(df["Customer_ID"].nunique())

    return kpis
