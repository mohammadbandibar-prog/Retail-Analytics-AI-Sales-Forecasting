import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Analytics & AI Sales Forecasting",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "outputs/cleaned_retail_sales.csv"
    )


@st.cache_data
def load_forecast():
    return pd.read_csv(
        "outputs/revenue_forecast.csv"
    )


df = load_data()
forecast_df = load_forecast()

df["Date"] = pd.to_datetime(df["Date"])
forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Retail Analytics")

st.sidebar.markdown(
    """
    ### Dashboard Navigation

    Use the sections below to explore the
    retail analytics and forecasting system.
    """
)

page = st.sidebar.radio(
    "Select Section",
    [
        "Executive Overview",
        "Revenue Analysis",
        "Store Analysis",
        "Product Analysis",
        "Customer & Promotion",
        "Revenue Forecast",
        "AI Business Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Retail Analytics & AI-Powered "
    "Sales Forecasting System"
)

# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.title("🏪 Retail Analytics & AI Sales Forecasting")

    st.markdown(
        """
        **Executive Overview**

        Analyze retail performance, identify sales patterns,
        understand store and product performance, and forecast
        future revenue.
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_revenue = df["Revenue"].sum()
    total_sales = df["Total_Sales"].sum()
    total_units = df["Units_Sold"].sum()
    total_stores = df["Store_ID"].nunique()
    total_products = df["Product_ID"].nunique()
    total_categories = df["Product_Category"].nunique()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Revenue",
        f"₹{total_revenue / 1e9:.2f} B"
    )

    col2.metric(
        "🛒 Total Sales",
        f"₹{total_sales / 1e9:.2f} B"
    )

    col3.metric(
        "📦 Units Sold",
        f"{total_units:,}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "🏪 Total Stores",
        f"{total_stores}"
    )

    col5.metric(
        "📱 Total Products",
        f"{total_products}"
    )

    col6.metric(
        "🏷️ Categories",
        f"{total_categories}"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MONTHLY REVENUE TREND
    # --------------------------------------------------------

    st.subheader("📈 Monthly Revenue Trend")

    monthly_revenue = (
        df.groupby(
            df["Date"].dt.to_period("M")
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["Date"] = (
        monthly_revenue["Date"].dt.to_timestamp()
    )

    fig = px.line(
        monthly_revenue,
        x="Date",
        y="Revenue",
        markers=True,
        title="Monthly Revenue"
    )

    fig.update_layout(
        yaxis_title="Revenue (₹)",
        xaxis_title="Month",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # STORE + CATEGORY
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏪 Revenue by Store")

        store_revenue = (
            df.groupby("Store_Location")["Revenue"]
            .sum()
            .reset_index()
            .sort_values(
                "Revenue",
                ascending=False
            )
        )

        fig_store = px.bar(
            store_revenue,
            x="Store_Location",
            y="Revenue",
            title="Revenue by Store"
        )

        fig_store.update_layout(
            xaxis_title="Store",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig_store,
            use_container_width=True
        )

    with col2:

        st.subheader("📦 Revenue by Category")

        category_revenue = (
            df.groupby("Product_Category")["Revenue"]
            .sum()
            .reset_index()
            .sort_values(
                "Revenue",
                ascending=False
            )
        )

        fig_category = px.bar(
            category_revenue,
            x="Product_Category",
            y="Revenue",
            title="Revenue by Product Category"
        )

        fig_category.update_layout(
            xaxis_title="Category",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    st.markdown("---")

    st.caption(
        "Retail Analytics & AI-Powered Sales Forecasting System | "
        "Data Period: January 2023 – December 2024"
    )


# ============================================================
# REVENUE ANALYSIS
# ============================================================

if page == "Revenue Analysis":

    st.title("📈 Revenue Analysis")

    st.markdown(
        """
        Analyze revenue trends across years, months, quarters,
        and seasonal patterns.
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # YEARLY REVENUE
    # --------------------------------------------------------

    yearly_revenue = (
        df.groupby("Year")["Revenue"]
        .sum()
        .reset_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📅 Revenue by Year")

        fig_year = px.bar(
            yearly_revenue,
            x="Year",
            y="Revenue",
            title="Yearly Revenue"
        )

        fig_year.update_layout(
            xaxis_title="Year",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(
            fig_year,
            use_container_width=True
        )

    # --------------------------------------------------------
    # YEAR-OVER-YEAR GROWTH
    # --------------------------------------------------------

    with col2:

        st.subheader("📊 Year-over-Year Growth")

        if len(yearly_revenue) >= 2:

            first_year_revenue = yearly_revenue.iloc[0]["Revenue"]
            last_year_revenue = yearly_revenue.iloc[-1]["Revenue"]

            growth = (
                (last_year_revenue - first_year_revenue)
                / first_year_revenue
            ) * 100

            st.metric(
                "Revenue Growth",
                f"{growth:.2f}%"
            )

            if growth >= 0:
                st.success(
                    f"Revenue increased by {growth:.2f}%."
                )
            else:
                st.warning(
                    f"Revenue decreased by {abs(growth):.2f}%."
                )

    st.markdown("---")

    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    st.subheader("📆 Monthly Revenue")

    monthly_revenue = (
        df.groupby(
            df["Date"].dt.to_period("M")
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["Date"] = (
        monthly_revenue["Date"].dt.to_timestamp()
    )

    fig_month = px.line(
        monthly_revenue,
        x="Date",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_month.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

    # --------------------------------------------------------
    # MONTHLY SEASONALITY
    # --------------------------------------------------------

    st.subheader("🌦️ Monthly Seasonality")

    seasonality = (
        df.groupby("Month_Name")["Revenue"]
        .sum()
        .reset_index()
    )

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

    seasonality["Month_Name"] = pd.Categorical(
        seasonality["Month_Name"],
        categories=month_order,
        ordered=True
    )

    seasonality = seasonality.sort_values(
        "Month_Name"
    )

    fig_season = px.bar(
        seasonality,
        x="Month_Name",
        y="Revenue",
        title="Revenue by Month"
    )

    fig_season.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_season,
        use_container_width=True
    )

    # --------------------------------------------------------
    # QUARTERLY REVENUE
    # --------------------------------------------------------

    st.subheader("📊 Quarterly Revenue")

    quarterly_revenue = (
        df.groupby(
            ["Year", "Quarter"]
        )["Revenue"]
        .sum()
        .reset_index()
    )

    quarterly_revenue["Period"] = (
        quarterly_revenue["Year"].astype(str)
        + " "
        + quarterly_revenue["Quarter"].astype(str)
    )

    fig_quarter = px.bar(
        quarterly_revenue,
        x="Period",
        y="Revenue",
        title="Quarterly Revenue"
    )

    fig_quarter.update_layout(
        xaxis_title="Period",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_quarter,
        use_container_width=True
    )

    # --------------------------------------------------------
    # REVENUE INSIGHTS
    # --------------------------------------------------------

    highest_month = seasonality.loc[
        seasonality["Revenue"].idxmax()
    ]

    lowest_month = seasonality.loc[
        seasonality["Revenue"].idxmin()
    ]

    st.markdown("---")

    st.subheader("💡 Revenue Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"**Highest Revenue Month:** "
            f"{highest_month['Month_Name']} "
            f"with ₹{highest_month['Revenue'] / 1e9:.2f}B."
        )

    with col2:

        st.info(
            f"**Lowest Revenue Month:** "
            f"{lowest_month['Month_Name']} "
            f"with ₹{lowest_month['Revenue'] / 1e9:.2f}B."
        )

    st.markdown("---")

    st.caption(
        "Revenue Analysis | Data Period: January 2023 – December 2024"
    )
    # ============================================================
# STORE ANALYSIS
# ============================================================

if page == "Store Analysis":

    st.title("🏪 Store Analysis")

    st.markdown(
        """
        Analyze store-level performance and identify groups of
        stores with similar business characteristics.
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # STORE PERFORMANCE
    # --------------------------------------------------------

    store_performance = (
        df.groupby("Store_Location")
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Total_Units=("Units_Sold", "sum"),
            Transactions=("Store_ID", "count"),
            Average_Rating=("Store_Rating", "mean"),
            Average_Stock=("Stock_On_Hand", "mean")
        )
        .reset_index()
        .sort_values(
            "Total_Revenue",
            ascending=False
        )
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    best_store = store_performance.iloc[0]
    worst_store = store_performance.iloc[-1]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏆 Best Store",
        best_store["Store_Location"]
    )

    col2.metric(
        "💰 Highest Store Revenue",
        f"₹{best_store['Total_Revenue'] / 1e9:.2f} B"
    )

    col3.metric(
        "📉 Lowest Store Revenue",
        f"₹{worst_store['Total_Revenue'] / 1e9:.2f} B"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # REVENUE BY STORE
    # --------------------------------------------------------

    st.subheader("💰 Revenue by Store")

    fig_revenue = px.bar(
        store_performance,
        x="Store_Location",
        y="Total_Revenue",
        title="Total Revenue by Store",
        text_auto=".2s"
    )

    fig_revenue.update_layout(
        xaxis_title="Store",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

    # --------------------------------------------------------
    # UNITS + TRANSACTIONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📦 Units Sold by Store")

        fig_units = px.bar(
            store_performance,
            x="Store_Location",
            y="Total_Units",
            title="Units Sold"
        )

        fig_units.update_layout(
            xaxis_title="Store",
            yaxis_title="Units Sold"
        )

        st.plotly_chart(
            fig_units,
            use_container_width=True
        )

    with col2:

        st.subheader("🛒 Transactions by Store")

        fig_transactions = px.bar(
            store_performance,
            x="Store_Location",
            y="Transactions",
            title="Transactions"
        )

        fig_transactions.update_layout(
            xaxis_title="Store",
            yaxis_title="Transactions"
        )

        st.plotly_chart(
            fig_transactions,
            use_container_width=True
        )

    # --------------------------------------------------------
    # STORE RATING + STOCK
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("⭐ Average Store Rating")

        fig_rating = px.bar(
            store_performance,
            x="Store_Location",
            y="Average_Rating",
            title="Average Store Rating"
        )

        fig_rating.update_layout(
            xaxis_title="Store",
            yaxis_title="Rating"
        )

        st.plotly_chart(
            fig_rating,
            use_container_width=True
        )

    with col2:

        st.subheader("📦 Average Stock on Hand")

        fig_stock = px.bar(
            store_performance,
            x="Store_Location",
            y="Average_Stock",
            title="Average Stock"
        )

        fig_stock.update_layout(
            xaxis_title="Store",
            yaxis_title="Average Stock"
        )

        st.plotly_chart(
            fig_stock,
            use_container_width=True
        )

    # --------------------------------------------------------
    # STORE PERFORMANCE TABLE
    # --------------------------------------------------------

    st.subheader("📋 Store Performance Details")

    display_store = store_performance.copy()

    display_store["Total_Revenue"] = (
        display_store["Total_Revenue"]
        .map(lambda x: f"₹{x / 1e9:.2f} B")
    )

    display_store["Average_Rating"] = (
        display_store["Average_Rating"]
        .round(2)
    )

    display_store["Average_Stock"] = (
        display_store["Average_Stock"]
        .round(2)
    )

    st.dataframe(
        display_store,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ========================================================
    # K-MEANS STORE SEGMENTATION
    # ========================================================

    st.subheader("🧩 Store Segmentation")

    st.markdown(
        """
        Stores are grouped using **K-Means clustering** based on
        revenue, units sold, transactions, discounts, ratings,
        and stock levels.
        """
    )

    # Load segmentation results
    try:

        segments = pd.read_csv(
            "outputs/store_segments.csv"
        )

        cluster_summary = pd.read_csv(
            "outputs/cluster_summary.csv"
        )

        # ----------------------------------------------------
        # Add Store Location
        # ----------------------------------------------------

        store_locations = (
            df[
                ["Store_ID", "Store_Location"]
            ]
            .drop_duplicates()
        )

        segments = segments.merge(
            store_locations,
            on="Store_ID",
            how="left"
        )

        # ----------------------------------------------------
        # Cluster Count
        # ----------------------------------------------------

        cluster_counts = (
            segments["Cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster_counts.columns = [
            "Cluster",
            "Stores"
        ]

        fig_cluster = px.bar(
            cluster_counts,
            x="Cluster",
            y="Stores",
            title="Number of Stores in Each Segment",
            text_auto=True
        )

        fig_cluster.update_layout(
            xaxis_title="Cluster",
            yaxis_title="Number of Stores"
        )

        st.plotly_chart(
            fig_cluster,
            use_container_width=True
        )

        # ----------------------------------------------------
        # Segment Table
        # ----------------------------------------------------

        st.subheader("🏪 Store Segment Membership")

        segment_display = segments[
            [
                "Store_ID",
                "Store_Location",
                "Total_Revenue",
                "Total_Units_Sold",
                "Average_Revenue",
                "Average_Discount",
                "Average_Rating",
                "Average_Stock",
                "Transactions",
                "Cluster"
            ]
        ].sort_values(
            "Cluster"
        )

        st.dataframe(
            segment_display,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Cluster Summary
        # ----------------------------------------------------

        st.subheader("📊 Segment Summary")

        st.dataframe(
            cluster_summary,
            use_container_width=True
        )

        # ----------------------------------------------------
        # Segment Insights
        # ----------------------------------------------------

        cluster_revenue = (
            segments.groupby("Cluster")["Total_Revenue"]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        highest_cluster = cluster_revenue.index[0]
        lowest_cluster = cluster_revenue.index[-1]

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"**Higher-performing segment:** "
                f"Cluster {highest_cluster}"
            )

        with col2:

            st.warning(
                f"**Relatively lower-performing segment:** "
                f"Cluster {lowest_cluster}"
            )

    except FileNotFoundError:

        st.error(
            "Store segmentation files were not found. "
            "Please run store_segmentation.py first."
        )

    st.markdown("---")

    st.caption(
        "Store Analysis & Segmentation | "
        "Retail Analytics & AI Sales Forecasting System"
    )

    # =========================================================
# PRODUCT ANALYSIS
# =========================================================

if page == "Product Analysis":

    st.title("📦 Product Analysis")
    st.markdown(
        "Analyze product, category, and brand-level revenue and sales performance."
    )

    # -----------------------------------------------------
    # Category Filter
    # -----------------------------------------------------

    categories = ["All"] + sorted(df["Product_Category"].unique().tolist())

    selected_category = st.selectbox(
        "Select Product Category",
        categories
    )

    if selected_category != "All":
        product_df = df[
            df["Product_Category"] == selected_category
        ].copy()
    else:
        product_df = df.copy()

    # -----------------------------------------------------
    # KPI Calculations
    # -----------------------------------------------------

    total_revenue = product_df["Revenue"].sum()
    total_units = product_df["Units_Sold"].sum()
    total_products = product_df["Product_ID"].nunique()
    total_brands = product_df["Brand"].nunique()

    # -----------------------------------------------------
    # KPI Cards
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

    col2.metric(
        "Units Sold",
        f"{total_units:,.0f}"
    )

    col3.metric(
        "Products",
        f"{total_products:,}"
    )

    col4.metric(
        "Brands",
        f"{total_brands:,}"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # Category Performance
    # -----------------------------------------------------

    st.subheader("📊 Category Performance")

    category_performance = (
        product_df
        .groupby("Product_Category")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum"),
            Transactions=("Product_ID", "count")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_category_revenue = px.bar(
            category_performance,
            x="Product_Category",
            y="Revenue",
            title="Revenue by Product Category",
            text_auto=".2s"
        )

        fig_category_revenue.update_layout(
            xaxis_title="Product Category",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_category_revenue,
            use_container_width=True
        )

    with col2:

        fig_category_units = px.bar(
            category_performance,
            x="Product_Category",
            y="Units_Sold",
            title="Units Sold by Product Category",
            text_auto=".2s"
        )

        fig_category_units.update_layout(
            xaxis_title="Product Category",
            yaxis_title="Units Sold"
        )

        st.plotly_chart(
            fig_category_units,
            use_container_width=True
        )

    # -----------------------------------------------------
    # Category Table
    # -----------------------------------------------------

    st.subheader("📋 Category Performance Table")

    category_display = category_performance.copy()

    category_display["Revenue"] = category_display[
        "Revenue"
    ].round(0)

    st.dataframe(
        category_display,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # Top 10 Products
    # -----------------------------------------------------

    st.subheader("🏆 Top 10 Products by Revenue")

    top_products = (
        product_df
        .groupby(
            ["Product_ID", "Product_Category"]
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig_top_products = px.bar(
        top_products.sort_values("Revenue"),
        x="Revenue",
        y="Product_ID",
        orientation="h",
        title="Top 10 Products by Revenue",
        text_auto=".2s"
    )

    fig_top_products.update_layout(
        xaxis_title="Revenue",
        yaxis_title="Product ID"
    )

    st.plotly_chart(
        fig_top_products,
        use_container_width=True
    )

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # Brand Performance
    # -----------------------------------------------------

    st.subheader("🏷️ Brand Performance")

    brand_performance = (
        product_df
        .groupby("Brand")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum")
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig_brands = px.bar(
        brand_performance.sort_values("Revenue"),
        x="Revenue",
        y="Brand",
        orientation="h",
        title="Top 10 Brands by Revenue",
        text_auto=".2s"
    )

    fig_brands.update_layout(
        xaxis_title="Revenue",
        yaxis_title="Brand"
    )

    st.plotly_chart(
        fig_brands,
        use_container_width=True
    )

    # -----------------------------------------------------
    # Product Insights
    # -----------------------------------------------------

    st.subheader("💡 Product Insights")

    best_category = category_performance.iloc[0]

    top_product = top_products.iloc[0]

    top_brand = brand_performance.iloc[0]

    st.success(
        f"🏆 **Best Product Category:** "
        f"{best_category['Product_Category']} "
        f"with revenue of "
        f"₹{best_category['Revenue']:,.0f}."
    )

    st.info(
        f"📦 **Top Product:** "
        f"{top_product['Product_ID']} "
        f"generated revenue of "
        f"₹{top_product['Revenue']:,.0f}."
    )

    st.warning(
        f"🏷️ **Top Brand:** "
        f"{top_brand['Brand']} "
        f"generated revenue of "
        f"₹{top_brand['Revenue']:,.0f}."
    )

    st.caption(
        "Product Analysis | Data Period: January 2023 – December 2024"
    )
# =========================================================
# CUSTOMER & PROMOTION ANALYSIS
# =========================================================

if page == "Customer & Promotion":

    st.title("👥 Customer & Promotion Analysis")
    st.markdown(
        "Analyze customer behavior, payment preferences, promotions, and holiday sales."
    )

    # -----------------------------------------------------
    # Customer Type Performance
    # -----------------------------------------------------

    customer_performance = (
        df.groupby("Customer_Type")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum"),
            Transactions=("Customer_Type", "count")
        )
        .reset_index()
    )

    # -----------------------------------------------------
    # Payment Performance
    # -----------------------------------------------------

    payment_performance = (
        df.groupby("Payment_Mode")
        .agg(
            Revenue=("Revenue", "sum"),
            Transactions=("Payment_Mode", "count")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    # -----------------------------------------------------
    # Promotion Performance
    # -----------------------------------------------------

    promotion_performance = (
        df.groupby("Promotion_Applied")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum"),
            Transactions=("Promotion_Applied", "count")
        )
        .reset_index()
    )

    promotion_performance["Revenue_Per_Transaction"] = (
        promotion_performance["Revenue"]
        / promotion_performance["Transactions"]
    )

    # -----------------------------------------------------
    # Holiday Performance
    # -----------------------------------------------------

    holiday_performance = (
        df.groupby("Holiday_Flag")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum"),
            Transactions=("Holiday_Flag", "count")
        )
        .reset_index()
    )

    holiday_performance["Revenue_Per_Transaction"] = (
        holiday_performance["Revenue"]
        / holiday_performance["Transactions"]
    )

    # -----------------------------------------------------
    # KPI Cards
    # -----------------------------------------------------

    total_revenue = df["Revenue"].sum()

    returning_revenue = customer_performance.loc[
        customer_performance["Customer_Type"] == "Returning",
        "Revenue"
    ].sum()

    new_revenue = customer_performance.loc[
        customer_performance["Customer_Type"] == "New",
        "Revenue"
    ].sum()

    returning_share = (
        returning_revenue / total_revenue * 100
    )

    promotion_revenue = promotion_performance.loc[
        promotion_performance["Promotion_Applied"] == "Yes",
        "Revenue"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Returning Customer Revenue",
        f"₹{returning_revenue:,.0f}"
    )

    col2.metric(
        "New Customer Revenue",
        f"₹{new_revenue:,.0f}"
    )

    col3.metric(
        "Returning Revenue Share",
        f"{returning_share:.1f}%"
    )

    col4.metric(
        "Promotion Revenue",
        f"₹{promotion_revenue:,.0f}"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # Customer Analysis
    # -----------------------------------------------------

    st.subheader("👥 Customer Type Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig_customer_revenue = px.bar(
            customer_performance,
            x="Customer_Type",
            y="Revenue",
            title="Revenue by Customer Type",
            text_auto=".2s"
        )

        fig_customer_revenue.update_layout(
            xaxis_title="Customer Type",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_customer_revenue,
            use_container_width=True
        )

    with col2:

        fig_customer_pie = px.pie(
            customer_performance,
            names="Customer_Type",
            values="Revenue",
            title="Customer Revenue Distribution"
        )

        st.plotly_chart(
            fig_customer_pie,
            use_container_width=True
        )

    st.dataframe(
        customer_performance,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # Payment Mode
    # -----------------------------------------------------

    st.subheader("💳 Payment Mode Analysis")

    fig_payment = px.bar(
        payment_performance,
        x="Payment_Mode",
        y="Revenue",
        title="Revenue by Payment Mode",
        text_auto=".2s"
    )

    fig_payment.update_layout(
        xaxis_title="Payment Mode",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

    st.dataframe(
        payment_performance,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # Promotion Analysis
    # -----------------------------------------------------

    st.subheader("🎯 Promotion Analysis")

    col1, col2 = st.columns(2)

    with col1:

        fig_promotion = px.bar(
            promotion_performance,
            x="Promotion_Applied",
            y="Revenue",
            title="Revenue: Promotion vs No Promotion",
            text_auto=".2s"
        )

        fig_promotion.update_layout(
            xaxis_title="Promotion Applied",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_promotion,
            use_container_width=True
        )

    with col2:

        fig_promotion_rpt = px.bar(
            promotion_performance,
            x="Promotion_Applied",
            y="Revenue_Per_Transaction",
            title="Revenue per Transaction",
            text_auto=".2s"
        )

        fig_promotion_rpt.update_layout(
            xaxis_title="Promotion Applied",
            yaxis_title="Revenue per Transaction"
        )

        st.plotly_chart(
            fig_promotion_rpt,
            use_container_width=True
        )

    st.dataframe(
        promotion_performance,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # Holiday Analysis
    # -----------------------------------------------------

    st.subheader("📅 Holiday Sales Analysis")

    holiday_display = holiday_performance.copy()

    holiday_display["Holiday_Status"] = holiday_display[
        "Holiday_Flag"
    ].map({
        0: "Non-Holiday",
        1: "Holiday"
    })

    fig_holiday = px.bar(
        holiday_display,
        x="Holiday_Status",
        y="Revenue",
        title="Revenue: Holiday vs Non-Holiday",
        text_auto=".2s"
    )

    fig_holiday.update_layout(
        xaxis_title="Period",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_holiday,
        use_container_width=True
    )

    st.dataframe(
        holiday_display[
            [
                "Holiday_Status",
                "Revenue",
                "Units_Sold",
                "Transactions",
                "Revenue_Per_Transaction"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # Business Insights
    # -----------------------------------------------------

    st.subheader("💡 Customer & Promotion Insights")

    if returning_share > 50:

        st.success(
            f"🔄 Returning customers contribute "
            f"{returning_share:.1f}% of total revenue, "
            f"indicating strong repeat-customer contribution."
        )

    else:

        st.info(
            f"🆕 New customers contribute significantly to revenue "
            f"with {100 - returning_share:.1f}% of total revenue."
        )

    highest_payment = payment_performance.iloc[0]

    st.info(
        f"💳 **Leading Payment Mode:** "
        f"{highest_payment['Payment_Mode']} generated "
        f"₹{highest_payment['Revenue']:,.0f} in revenue."
    )

    promotion_yes = promotion_performance[
        promotion_performance["Promotion_Applied"] == "Yes"
    ]

    promotion_no = promotion_performance[
        promotion_performance["Promotion_Applied"] == "No"
    ]

    if not promotion_yes.empty and not promotion_no.empty:

        promo_yes_rpt = promotion_yes[
            "Revenue_Per_Transaction"
        ].iloc[0]

        promo_no_rpt = promotion_no[
            "Revenue_Per_Transaction"
        ].iloc[0]

        if promo_yes_rpt > promo_no_rpt:

            st.success(
                "🎯 Transactions with promotions generated "
                "higher average revenue per transaction."
            )

        else:

            st.warning(
                "🎯 Transactions without promotions generated "
                "higher average revenue per transaction."
            )

    st.caption(
        "Customer & Promotion Analysis | "
        "Data Period: January 2023 – December 2024"
    )

    # =========================================================
# REVENUE FORECAST
# =========================================================

if page == "Revenue Forecast":

    st.title("📈 Revenue Forecast")

    st.markdown(
        "Forecast future monthly revenue using the seasonal-naive "
        "time-series forecasting model."
    )

    # -----------------------------------------------------
    # Prepare Historical Revenue
    # -----------------------------------------------------

    monthly_revenue = (
        df.groupby("Year_Month")["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["Year_Month"] = pd.to_datetime(
        monthly_revenue["Year_Month"]
    )

    monthly_revenue = monthly_revenue.sort_values(
        "Year_Month"
    )

    # -----------------------------------------------------
    # Load Forecast
    # -----------------------------------------------------

    forecast_file = "outputs/revenue_forecast.csv"

    try:

        forecast_df = pd.read_csv(
            forecast_file
        )

        forecast_df["Date"] = pd.to_datetime(
            forecast_df["Date"]
        )

        # -------------------------------------------------
        # KPI Calculations
        # -------------------------------------------------

        forecast_values = forecast_df[
            "Forecast_Revenue"
        ]

        total_forecast = forecast_values.sum()

        average_forecast = forecast_values.mean()

        highest_forecast = forecast_values.max()

        lowest_forecast = forecast_values.min()

        # -------------------------------------------------
        # KPI Cards
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "12-Month Forecast",
            f"₹{total_forecast:,.0f}"
        )

        col2.metric(
            "Average Monthly Forecast",
            f"₹{average_forecast:,.0f}"
        )

        col3.metric(
            "Highest Forecast",
            f"₹{highest_forecast:,.0f}"
        )

        col4.metric(
            "Lowest Forecast",
            f"₹{lowest_forecast:,.0f}"
        )

        st.markdown("---")

        # -------------------------------------------------
        # Historical Revenue
        # -------------------------------------------------

        st.subheader("📊 Historical Monthly Revenue")

        fig_history = px.line(
            monthly_revenue,
            x="Year_Month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue — January 2023 to December 2024"
        )

        fig_history.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_history,
            use_container_width=True
        )

        # -------------------------------------------------
        # Future Forecast
        # -------------------------------------------------

        st.subheader("🔮 Future Revenue Forecast")

        fig_forecast = px.line(
            forecast_df,
            x="Date",
            y="Forecast_Revenue",
            markers=True,
            title="12-Month Revenue Forecast"
        )

        fig_forecast.update_layout(
            xaxis_title="Forecast Month",
            yaxis_title="Forecast Revenue"
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )

        # -------------------------------------------------
        # Historical + Forecast Combined Chart
        # -------------------------------------------------

        st.subheader("📈 Historical vs Future Revenue")

        historical_chart = monthly_revenue[
            ["Year_Month", "Revenue"]
        ].copy()

        historical_chart = historical_chart.rename(
            columns={
                "Year_Month": "Date",
                "Revenue": "Revenue_Value"
            }
        )

        historical_chart["Type"] = "Historical"

        future_chart = forecast_df[
            ["Date", "Forecast_Revenue"]
        ].copy()

        future_chart = future_chart.rename(
            columns={
                "Forecast_Revenue": "Revenue_Value"
            }
        )

        future_chart["Type"] = "Forecast"

        combined_chart = pd.concat(
            [
                historical_chart,
                future_chart
            ],
            ignore_index=True
        )

        fig_combined = px.line(
            combined_chart,
            x="Date",
            y="Revenue_Value",
            color="Type",
            markers=True,
            title="Historical Revenue and Future Forecast"
        )

        fig_combined.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_combined,
            use_container_width=True
        )

        # -------------------------------------------------
        # Forecast Table
        # -------------------------------------------------

        st.subheader("📋 Forecast Details")

        forecast_display = forecast_df.copy()

        forecast_display["Forecast_Revenue"] = (
            forecast_display["Forecast_Revenue"]
            .round(0)
        )

        forecast_display["Date"] = (
            forecast_display["Date"]
            .dt.strftime("%B %Y")
        )

        forecast_display = forecast_display.rename(
            columns={
                "Date": "Forecast Month",
                "Forecast_Revenue": "Forecast Revenue"
            }
        )

        st.dataframe(
            forecast_display,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # Model Performance
        # -------------------------------------------------

        st.subheader("📏 Forecast Model Performance")

        col1, col2, col3 = st.columns(3)

        mae = 44524409.81
        rmse = 50478857.91
        mape = 2.60

        col1.metric(
            "MAE",
            f"₹{mae:,.0f}"
        )

        col2.metric(
            "RMSE",
            f"₹{rmse:,.0f}"
        )

        col3.metric(
            "MAPE",
            f"{mape:.2f}%"
        )

        st.info(
            "The seasonal-naive forecasting model achieved "
            "a MAPE of 2.60% on the six-month test period."
        )

        # -------------------------------------------------
        # Forecast Insights
        # -------------------------------------------------

        st.subheader("💡 Forecast Insights")

        highest_month = forecast_df.loc[
            forecast_df["Forecast_Revenue"].idxmax()
        ]

        lowest_month = forecast_df.loc[
            forecast_df["Forecast_Revenue"].idxmin()
        ]

        st.success(
            f"📈 **Highest Forecast:** "
            f"{highest_month['Date'].strftime('%B %Y')} "
            f"with expected revenue of "
            f"₹{highest_month['Forecast_Revenue']:,.0f}."
        )

        st.warning(
            f"📉 **Lowest Forecast:** "
            f"{lowest_month['Date'].strftime('%B %Y')} "
            f"with expected revenue of "
            f"₹{lowest_month['Forecast_Revenue']:,.0f}."
        )

        st.info(
            "🔄 The model uses the previous year's corresponding "
            "monthly revenue as the forecast baseline, allowing "
            "the forecast to preserve recurring seasonal patterns."
        )

        st.caption(
            "Revenue Forecast | Forecast Horizon: 12 Months | "
            "Model: Seasonal Naive"
        )

    except FileNotFoundError:

        st.error(
            "Forecast file not found. "
            "Please run src/sales_forecasting.py first."
        )

        # =========================================================
# AI BUSINESS INSIGHTS
# =========================================================

if page == "AI Business Insights":

    st.title("🤖 AI Business Insights")

    st.markdown(
        "Key data-driven insights generated from revenue, "
        "store, product, customer, promotion, holiday, "
        "and forecasting analysis."
    )

    st.markdown("---")

    # =====================================================
    # REVENUE INSIGHTS
    # =====================================================

    st.subheader("💰 Revenue Insights")

    yearly_revenue = (
        df.groupby("Year")["Revenue"]
        .sum()
        .sort_index()
    )

    if len(yearly_revenue) >= 2:

        latest_year = yearly_revenue.index[-1]
        previous_year = yearly_revenue.index[-2]

        latest_revenue = yearly_revenue.iloc[-1]
        previous_revenue = yearly_revenue.iloc[-2]

        growth = (
            (latest_revenue - previous_revenue)
            / previous_revenue
            * 100
        )

        if growth >= 0:

            st.success(
                f"📈 Revenue increased by **{growth:.2f}%** "
                f"from {previous_year} to {latest_year}."
            )

        else:

            st.warning(
                f"📉 Revenue decreased by **{abs(growth):.2f}%** "
                f"from {previous_year} to {latest_year}."
            )

    # =====================================================
    # STORE INSIGHTS
    # =====================================================

    st.subheader("🏪 Store Insights")

    store_insights = (
        df.groupby("Store_Location")
        .agg(
            Revenue=("Revenue", "sum"),
            Units_Sold=("Units_Sold", "sum"),
            Transactions=("Store_ID", "count")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    best_store = store_insights.iloc[0]
    lowest_store = store_insights.iloc[-1]

    st.success(
        f"🏆 **Top Performing Store:** "
        f"{best_store['Store_Location']} generated "
        f"₹{best_store['Revenue']:,.0f} revenue."
    )

    st.info(
        f"📊 **Lowest Revenue Store:** "
        f"{lowest_store['Store_Location']} generated "
        f"₹{lowest_store['Revenue']:,.0f} revenue."
    )

    # =====================================================
    # PRODUCT INSIGHTS
    # =====================================================

    st.subheader("📦 Product Insights")

    category_revenue = (
        df.groupby("Product_Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = category_revenue.index[0]
    best_category_revenue = category_revenue.iloc[0]

    lowest_category = category_revenue.index[-1]
    lowest_category_revenue = category_revenue.iloc[-1]

    st.success(
        f"📦 **Best Product Category:** "
        f"{best_category} generated "
        f"₹{best_category_revenue:,.0f} revenue."
    )

    st.info(
        f"📊 **Lowest Revenue Category:** "
        f"{lowest_category} generated "
        f"₹{lowest_category_revenue:,.0f} revenue."
    )

    # =====================================================
    # TOP PRODUCT
    # =====================================================

    product_revenue = (
        df.groupby("Product_ID")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_revenue.index[0]
    top_product_revenue = product_revenue.iloc[0]

    st.info(
        f"🏆 **Top Product:** "
        f"{top_product} generated "
        f"₹{top_product_revenue:,.0f} revenue."
    )

    # =====================================================
    # CUSTOMER INSIGHTS
    # =====================================================

    st.subheader("👥 Customer Insights")

    customer_revenue = (
        df.groupby("Customer_Type")["Revenue"]
        .sum()
    )

    total_revenue = df["Revenue"].sum()

    returning_revenue = customer_revenue.get(
        "Returning",
        0
    )

    returning_share = (
        returning_revenue
        / total_revenue
        * 100
    )

    st.success(
        f"🔄 Returning customers contribute "
        f"**{returning_share:.1f}%** of total revenue."
    )

    st.info(
        "💡 Customer retention and loyalty strategies "
        "can be important because returning customers "
        "contribute a major share of revenue."
    )

    # =====================================================
    # PROMOTION INSIGHTS
    # =====================================================

    st.subheader("🎯 Promotion Insights")

    promotion = (
        df.groupby("Promotion_Applied")
        .agg(
            Revenue=("Revenue", "sum"),
            Transactions=("Promotion_Applied", "count")
        )
        .reset_index()
    )

    promotion["Revenue_Per_Transaction"] = (
        promotion["Revenue"]
        / promotion["Transactions"]
    )

    promo_yes = promotion[
        promotion["Promotion_Applied"] == "Yes"
    ]

    promo_no = promotion[
        promotion["Promotion_Applied"] == "No"
    ]

    if not promo_yes.empty and not promo_no.empty:

        yes_value = promo_yes[
            "Revenue_Per_Transaction"
        ].iloc[0]

        no_value = promo_no[
            "Revenue_Per_Transaction"
        ].iloc[0]

        if yes_value > no_value:

            st.success(
                "🎯 Promotional transactions generated "
                "higher revenue per transaction than "
                "non-promotional transactions."
            )

        else:

            st.warning(
                "🎯 Non-promotional transactions generated "
                "higher revenue per transaction than "
                "promotional transactions."
            )

    # =====================================================
    # HOLIDAY INSIGHTS
    # =====================================================

    st.subheader("📅 Holiday Insights")

    holiday = (
        df.groupby("Holiday_Flag")
        .agg(
            Revenue=("Revenue", "sum"),
            Transactions=("Holiday_Flag", "count")
        )
        .reset_index()
    )

    holiday["Revenue_Per_Transaction"] = (
        holiday["Revenue"]
        / holiday["Transactions"]
    )

    holiday_yes = holiday[
        holiday["Holiday_Flag"] == 1
    ]

    holiday_no = holiday[
        holiday["Holiday_Flag"] == 0
    ]

    if not holiday_yes.empty and not holiday_no.empty:

        yes_value = holiday_yes[
            "Revenue_Per_Transaction"
        ].iloc[0]

        no_value = holiday_no[
            "Revenue_Per_Transaction"
        ].iloc[0]

        if yes_value > no_value:

            st.success(
                "🎉 Holiday transactions generated "
                "higher revenue per transaction than "
                "non-holiday transactions."
            )

        else:

            st.info(
                "📅 Non-holiday transactions generated "
                "higher revenue per transaction than "
                "holiday transactions."
            )

    # =====================================================
    # FORECAST INSIGHTS
    # =====================================================

    st.subheader("🔮 Forecast Insights")

    try:

        forecast_df = pd.read_csv(
            "outputs/revenue_forecast.csv"
        )

        forecast_df["Date"] = pd.to_datetime(
            forecast_df["Date"]
        )

        highest_forecast = forecast_df.loc[
            forecast_df["Forecast_Revenue"].idxmax()
        ]

        lowest_forecast = forecast_df.loc[
            forecast_df["Forecast_Revenue"].idxmin()
        ]

        total_forecast = forecast_df[
            "Forecast_Revenue"
        ].sum()

        st.success(
            f"📈 **Highest Forecast Month:** "
            f"{highest_forecast['Date'].strftime('%B %Y')} "
            f"with expected revenue of "
            f"₹{highest_forecast['Forecast_Revenue']:,.0f}."
        )

        st.warning(
            f"📉 **Lowest Forecast Month:** "
            f"{lowest_forecast['Date'].strftime('%B %Y')} "
            f"with expected revenue of "
            f"₹{lowest_forecast['Forecast_Revenue']:,.0f}."
        )

        st.info(
            f"🔮 **Expected Revenue for Next 12 Months:** "
            f"₹{total_forecast:,.0f}"
        )

        st.caption(
            "Forecast Model: Seasonal Naive | "
            "Evaluation MAPE: 2.60%"
        )

    except FileNotFoundError:

        st.error(
            "Forecast file not found. "
            "Run src/sales_forecasting.py first."
        )

    # =====================================================
    # BUSINESS RECOMMENDATIONS
    # =====================================================

    st.markdown("---")

    st.subheader("🚀 Business Recommendations")

    st.markdown(
        """
        ### 1. 🏪 Improve lower-performing stores
        Analyze customer demand, inventory, and operational
        efficiency at stores generating comparatively lower revenue.

        ### 2. 📦 Prioritize high-performing products
        Maintain sufficient stock for products and categories
        generating high revenue.

        ### 3. 👥 Strengthen customer retention
        Returning customers contribute a major share of revenue.
        Loyalty programs and personalized offers can support retention.

        ### 4. 🎯 Optimize promotional campaigns
        Evaluate promotions using revenue per transaction instead
        of total revenue alone.

        ### 5. 📅 Plan for seasonal demand
        Historical monthly patterns can help plan inventory and
        marketing campaigns.

        ### 6. 🔮 Use forecasting for planning
        Revenue forecasts can support inventory, purchasing,
        staffing, and promotional decisions.
        """
    )

    st.success(
        "✅ The dashboard combines historical analytics, "
        "customer behavior, store performance, product analysis, "
        "and revenue forecasting to support data-driven retail decisions."
    )

    st.caption(
        "AI Business Insights | Retail Analytics & "
        "AI-Powered Sales Forecasting System"
    )
    