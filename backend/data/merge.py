import pandas as pd

df1 = pd.read_csv("raw/merged.csv", sep=";")
df2 = pd.read_csv("raw/severe_synthetic_600.csv", sep=";")

merged_df = pd.concat([df1, df2], ignore_index=True)

merged_df.to_csv("raw/mergedData.csv", index=False, sep=";")

print("Merged successfully")
print("Shape:", merged_df.shape)