import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==========================================
# STORE SEGMENTATION USING K-MEANS
# ==========================================

print("=" * 70)
print("STORE SEGMENTATION")
print("=" * 70)

# Load cleaned data
df = pd.read_csv("outputs/cleaned_retail_sales.csv")

# ------------------------------------------
# 1. CREATE STORE-LEVEL FEATURES
# ------------------------------------------

store_features = (
    df.groupby("Store_ID")
      .agg(
          Total_Revenue=("Revenue", "sum"),
          Total_Units_Sold=("Units_Sold", "sum"),
          Average_Revenue=("Revenue", "mean"),
          Average_Discount=("Discount_Percentage", "mean"),
          Average_Rating=("Store_Rating", "mean"),
          Average_Stock=("Stock_On_Hand", "mean"),
          Transactions=("Store_ID", "count")
      )
)

print("\nStore-level features:")
print(store_features)


# ------------------------------------------
# 2. SELECT FEATURES FOR CLUSTERING
# ------------------------------------------

features = [
    "Total_Revenue",
    "Total_Units_Sold",
    "Average_Revenue",
    "Average_Discount",
    "Average_Rating",
    "Average_Stock",
    "Transactions"
]

X = store_features[features]


# ------------------------------------------
# 3. STANDARDIZE FEATURES
# ------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ------------------------------------------
# 4. TEST DIFFERENT NUMBERS OF CLUSTERS
# ------------------------------------------

print("\n" + "=" * 70)
print("SILHOUETTE SCORES")
print("=" * 70)

for k in range(2, 6):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    score = silhouette_score(X_scaled, labels)

    print(f"K = {k}  →  Silhouette Score = {score:.4f}")


# ------------------------------------------
# 5. CREATE FINAL K-MEANS MODEL
# ------------------------------------------

kmeans = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

store_features["Cluster"] = kmeans.fit_predict(X_scaled)


# ------------------------------------------
# 6. DISPLAY CLUSTER RESULTS
# ------------------------------------------

print("\n" + "=" * 70)
print("STORE CLUSTERS")
print("=" * 70)

print(store_features.sort_values(
    "Total_Revenue",
    ascending=False
))


# ------------------------------------------
# 7. CLUSTER SUMMARY
# ------------------------------------------

cluster_summary = (
    store_features
    .groupby("Cluster")
    .agg(
        Stores=("Total_Revenue", "count"),
        Average_Revenue=("Total_Revenue", "mean"),
        Average_Units=("Total_Units_Sold", "mean"),
        Average_Discount=("Average_Discount", "mean"),
        Average_Rating=("Average_Rating", "mean"),
        Average_Stock=("Average_Stock", "mean"),
        Average_Transactions=("Transactions", "mean")
    )
)

print("\n" + "=" * 70)
print("CLUSTER SUMMARY")
print("=" * 70)

print(cluster_summary)


# ------------------------------------------
# 8. SAVE RESULTS
# ------------------------------------------

store_features.to_csv(
    "outputs/store_segments.csv"
)

cluster_summary.to_csv(
    "outputs/cluster_summary.csv"
)

print("\n" + "=" * 70)
print("STORE SEGMENTATION COMPLETED!")
print("=" * 70)

print("\nSaved:")
print("outputs/store_segments.csv")
print("outputs/cluster_summary.csv")