import pandas as pd

def clean_and_hybrid(raw_data):
    df = pd.DataFrame(raw_data)
    df.dropna(inplace=True)
    df = df[df["voltage"] > 0]
    df = df[df["current"] > 0]
    df["calc_power"]   = df["voltage"] * df["current"]
    df["hybrid_power"] = (df["calc_power"] + df["api_power"]) / 2
    return df