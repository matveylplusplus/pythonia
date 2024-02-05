import pandas as pd

df = pd.read_csv("artists.csv")

# print(df.to_string())
subdf = df.loc[df["artist_type"] == "Solo"]
print(subdf.to_string())
print(subdf.iloc[0]["artist_name"])
print(subdf.iloc[1]["artist_name"])
print(subdf.iloc[3]["artist_name"])
