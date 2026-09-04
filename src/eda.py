import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# RETAIL SALES - EXPLORATORY DATA ANALYSIS
# ==========================================

print("=" * 70)
print("RETAIL SALES EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# ------------------------------------------
# 1. LOAD CLEANED DATA
# ------------------------------------------

df = pd.read_csv("outputs/cleaned_retail_sales.csv")

df["Date"] = pd.to_datetime(df["Date"])

print("\nDataset loaded successfully.")
print("Shape:", df.shape)


# ------------------------------------------
# 2. CREATE OUTPUT FOLDER FOR CHARTS
# ------------------------------------------

os.makedirs("outputs/charts", exist_ok=True)


# ==========================================
# 3. KEY PERFORMANCE INDICATORS
# ==========================================

total_revenue = df["Revenue"].sum()
total_sales = df["Total_Sales"].sum()
total_units = df["Units_Sold"].sum()
total_stores = df["Store_ID"].nunique()
total_products = df["Product_ID"].nunique()
total_categories = df["Product_Category"].nunique()

average_revenue = df["Revenue"].mean()

print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

print(f"Total Revenue       : {total_revenue:,.2f}")
print(f"Total Sales         : {total_sales:,.2f}")
print(f"Total Units Sold    : {total_units:,}")
print(f"Total Stores        : {total_stores}")
print(f"Total Products      : {total_products}")
print(f"Total Categories    : {total_categories}")
print(f"Average Revenue     : {average_revenue:,.2f}")


# ==========================================
# 4. YEARLY REVENUE
# ==========================================

yearly_revenue = (
    df.groupby("Year")["Revenue"]
      .sum()
      .sort_index()
)

print("\n" + "=" * 70)
print("YEARLY REVENUE")
print("=" * 70)

print(yearly_revenue)

plt.figure(figsize=(8, 5))

yearly_revenue.plot(kind="bar")

plt.title("Yearly Revenue")
plt.xlabel("Year")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    "outputs/charts/yearly_revenue.png",
    dpi=300
)

plt.show()


# ==========================================
# 5. MONTHLY REVENUE TREND
# ==========================================

monthly_revenue = (
    df.groupby("Year_Month")["Revenue"]
      .sum()
)

monthly_revenue.index = pd.to_datetime(
    monthly_revenue.index
)

print("\n" + "=" * 70)
print("MONTHLY REVENUE")
print("=" * 70)

print(monthly_revenue)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_revenue_trend.png",
    dpi=300
)

plt.show()


# ==========================================
# 6. REVENUE BY STORE
# ==========================================

store_revenue = (
    df.groupby("Store_Location")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("REVENUE BY STORE")
print("=" * 70)

print(store_revenue)

plt.figure(figsize=(10, 6))

store_revenue.plot(kind="bar")

plt.title("Revenue by Store")
plt.xlabel("Store Location")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/revenue_by_store.png",
    dpi=300
)

plt.show()


# ==========================================
# 7. REVENUE BY REGION
# ==========================================

region_revenue = (
    df.groupby("Region")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("REVENUE BY REGION")
print("=" * 70)

print(region_revenue)

plt.figure(figsize=(8, 5))

region_revenue.plot(kind="bar")

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    "outputs/charts/revenue_by_region.png",
    dpi=300
)

plt.show()


# ==========================================
# 8. REVENUE BY PRODUCT CATEGORY
# ==========================================

category_revenue = (
    df.groupby("Product_Category")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("REVENUE BY PRODUCT CATEGORY")
print("=" * 70)

print(category_revenue)

plt.figure(figsize=(9, 6))

category_revenue.plot(kind="bar")

plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/revenue_by_category.png",
    dpi=300
)

plt.show()


# ==========================================
# 9. TOP 10 PRODUCTS
# ==========================================

top_products = (
    df.groupby("Product_ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

print(top_products)


# ==========================================
# 10. TOP 10 BRANDS
# ==========================================

top_brands = (
    df.groupby("Brand")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\n" + "=" * 70)
print("TOP 10 BRANDS BY REVENUE")
print("=" * 70)

print(top_brands)


# ==========================================
# 11. CUSTOMER TYPE ANALYSIS
# ==========================================

customer_revenue = (
    df.groupby("Customer_Type")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("REVENUE BY CUSTOMER TYPE")
print("=" * 70)

print(customer_revenue)


# ==========================================
# 12. PAYMENT MODE ANALYSIS
# ==========================================

payment_revenue = (
    df.groupby("Payment_Mode")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("REVENUE BY PAYMENT MODE")
print("=" * 70)

print(payment_revenue)


# ==========================================
# 13. PROMOTION ANALYSIS
# ==========================================

promotion_analysis = (
    df.groupby("Promotion_Applied")
      .agg(
          Revenue=("Revenue", "sum"),
          Units_Sold=("Units_Sold", "sum"),
          Average_Revenue=("Revenue", "mean"),
          Transactions=("Revenue", "count")
      )
)

print("\n" + "=" * 70)
print("PROMOTION ANALYSIS")
print("=" * 70)

print(promotion_analysis)


# ==========================================
# 14. HOLIDAY ANALYSIS
# ==========================================

holiday_analysis = (
    df.groupby("Holiday_Flag")
      .agg(
          Revenue=("Revenue", "sum"),
          Units_Sold=("Units_Sold", "sum"),
          Transactions=("Revenue", "count")
      )
)

print("\n" + "=" * 70)
print("HOLIDAY ANALYSIS")
print("=" * 70)

print(holiday_analysis)


# ==========================================
# 15. MONTHLY SEASONALITY
# ==========================================

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly_seasonality = (
    df.groupby("Month_Name")["Revenue"]
      .sum()
      .reindex(month_order)
)

print("\n" + "=" * 70)
print("MONTHLY SEASONALITY")
print("=" * 70)

print(monthly_seasonality)

plt.figure(figsize=(12, 6))

monthly_seasonality.plot(kind="bar")

plt.title("Revenue by Month")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_seasonality.png",
    dpi=300
)

plt.show()


# ==========================================
# 16. STORE PERFORMANCE SUMMARY
# ==========================================

store_summary = (
    df.groupby("Store_ID")
      .agg(
          Revenue=("Revenue", "sum"),
          Units_Sold=("Units_Sold", "sum"),
          Average_Rating=("Store_Rating", "mean"),
          Average_Stock=("Stock_On_Hand", "mean"),
          Transactions=("Store_ID", "count")
      )
      .sort_values("Revenue", ascending=False)
)

print("\n" + "=" * 70)
print("STORE PERFORMANCE SUMMARY")
print("=" * 70)

print(store_summary)


# ==========================================
# 17. SAVE ANALYSIS TABLES
# ==========================================

yearly_revenue.to_csv(
    "outputs/yearly_revenue.csv"
)

store_revenue.to_csv(
    "outputs/store_revenue.csv"
)

region_revenue.to_csv(
    "outputs/region_revenue.csv"
)

category_revenue.to_csv(
    "outputs/category_revenue.csv"
)

top_products.to_csv(
    "outputs/top_products.csv"
)

top_brands.to_csv(
    "outputs/top_brands.csv"
)

store_summary.to_csv(
    "outputs/store_summary.csv"
)


# ==========================================
# COMPLETED
# ==========================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nCharts saved in:")
print("outputs/charts/")

print("\nAnalysis tables saved in:")
print("outputs/")