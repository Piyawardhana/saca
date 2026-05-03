import pandas as pd

df = pd.read_csv("../raw/New folder/validation-data.csv")

# Fix if data is in one column
if len(df.columns) == 1:
    df = df[df.columns[0]].str.split(",", expand=True)

# Assign column names
df.columns = ['instruction', 'input', 'output', 'specialty', 'urgency', 'confidence', 'id']

# Keep only relevant columns
df_clean = df[['input', 'output', 'specialty', 'urgency', 'confidence', 'id']]

# Lowercase
df_clean['input'] = df_clean['input'].str.lower()
df_clean['output'] = df_clean['output'].str.lower()

# Strip spaces
df_clean = df_clean.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Remove duplicates & nulls
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.dropna()

# Save
df_clean.to_csv("cleanedValidationData.csv", index=False, sep=";")

# Debug prints
print(df.head())
print(df.columns)