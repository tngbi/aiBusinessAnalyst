
import pandas as pd

def load_excel(file):
    df = pd.read_excel(file)
    return df
