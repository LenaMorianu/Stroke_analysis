import pandas as pd

# Load and display column names
try:
    df = pd.read_csv('IHME-GBD_2023_DATA-53bc0df1-1.csv')
    print("Column names in your CSV:")
    print(df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
    print("\nData shape:", df.shape)
    print("\nData types:")
    print(df.dtypes)
except FileNotFoundError:
    print("CSV file not found!")
