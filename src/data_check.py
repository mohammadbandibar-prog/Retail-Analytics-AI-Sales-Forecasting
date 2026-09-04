import pandas as pd

# Load dataset
df = pd.read_csv("data/Retail_Sales_Data_Unlox.csv")

# Dataset shape
print("\n" + "=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# Column names
print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

# First 5 rows
print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head())

# Data types
print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

# Missing values
print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

# Duplicate rows
print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)
print(df.duplicated().sum())

# Basic statistics
print("\n" + "=" * 60)
print("NUMERICAL SUMMARY")
print("=" * 60)
print(df.describe())

# Date information
print("\n" + "=" * 60)
print("DATE INFORMATION")
print("=" * 60)

df["Date"] = pd.to_datetime(df["Date"])

print("Minimum Date:", df["Date"].min())
print("Maximum Date:", df["Date"].max())

# Unique values
print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

print("Stores:", df["Store_ID"].nunique())
print("Products:", df["Product_ID"].nunique())
print("Categories:", df["Product_Category"].nunique())
print("Brands:", df["Brand"].nunique())
print("Regions:", df["Region"].nunique())

print("\nData inspection completed successfully!")