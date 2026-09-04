import pandas as pd
import os

# ==========================================
# RETAIL SALES DATA - DATA CLEANING
# ==========================================

print("=" * 60)
print("RETAIL SALES DATA CLEANING")
print("=" * 60)

# ------------------------------------------
# 1. LOAD DATA
# ------------------------------------------

input_file = "data/Retail_Sales_Data_Unlox.csv"

df = pd.read_csv(input_file)

print("\nOriginal dataset shape:")
print(df.shape)


# ------------------------------------------
# 2. REMOVE EXTRA SPACES FROM COLUMN NAMES
# ------------------------------------------

df.columns = df.columns.str.strip()


# ------------------------------------------
# 3. REMOVE EXTRA SPACES FROM TEXT COLUMNS
# ------------------------------------------

text_columns = df.select_dtypes(include="object").columns

for column in text_columns:
    df[column] = df[column].str.strip()


# ------------------------------------------
# 4. CONVERT DATE COLUMN
# ------------------------------------------

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# ------------------------------------------
# 5. CHECK MISSING VALUES
# ------------------------------------------

print("\nMissing values before cleaning:")

print(df.isnull().sum().sum())


# ------------------------------------------
# 6. CHECK DUPLICATES
# ------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate rows:")
print(duplicates)


# ------------------------------------------
# 7. REMOVE DUPLICATES IF ANY
# ------------------------------------------

if duplicates > 0:
    df = df.drop_duplicates()


# ------------------------------------------
# 8. VALIDATE NUMERICAL VALUES
# ------------------------------------------

print("\nChecking numerical values...")

print("Negative Units Sold:",
      (df["Units_Sold"] < 0).sum())

print("Negative Unit Price:",
      (df["Unit_Price"] < 0).sum())

print("Negative Revenue:",
      (df["Revenue"] < 0).sum())

print("Invalid Discount:",
      ((df["Discount_Percentage"] < 0) |
       (df["Discount_Percentage"] > 100)).sum())

print("Invalid Store Rating:",
      ((df["Store_Rating"] < 0) |
       (df["Store_Rating"] > 5)).sum())


# ------------------------------------------
# 9. CREATE DATE FEATURES
# ------------------------------------------

df["Year"] = df["Date"].dt.year

df["Month"] = df["Date"].dt.month

df["Month_Name"] = df["Date"].dt.month_name()

df["Quarter"] = df["Date"].dt.quarter

df["Day"] = df["Date"].dt.day

df["Day_Name"] = df["Date"].dt.day_name()

df["Week"] = df["Date"].dt.isocalendar().week.astype(int)


# ------------------------------------------
# 10. CREATE YEAR-MONTH COLUMN
# ------------------------------------------

df["Year_Month"] = df["Date"].dt.to_period("M").astype(str)


# ------------------------------------------
# 11. CHECK FINANCIAL CALCULATIONS
# ------------------------------------------

calculated_sales = (
    df["Unit_Price"] * df["Units_Sold"]
)

sales_difference = (
    df["Total_Sales"] - calculated_sales
).abs()

print("\nIncorrect Total Sales calculations:")
print((sales_difference > 0.01).sum())


calculated_revenue = (
    df["Total_Sales"] *
    (1 - df["Discount_Percentage"] / 100)
)

revenue_difference = (
    df["Revenue"] - calculated_revenue
).abs()

print("\nIncorrect Revenue calculations:")
print((revenue_difference > 0.01).sum())


# ------------------------------------------
# 12. CREATE OUTPUT DIRECTORY
# ------------------------------------------

os.makedirs("outputs", exist_ok=True)


# ------------------------------------------
# 13. SAVE CLEANED DATA
# ------------------------------------------

output_file = "outputs/cleaned_retail_sales.csv"

df.to_csv(output_file, index=False)


# ------------------------------------------
# 14. FINAL INFORMATION
# ------------------------------------------

print("\n" + "=" * 60)
print("CLEANING COMPLETED")
print("=" * 60)

print("\nFinal dataset shape:")
print(df.shape)

print("\nDate range:")
print(df["Date"].min(), "to", df["Date"].max())

print("\nCleaned dataset saved to:")
print(output_file)

print("\nData cleaning completed successfully!")