
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from src import analysis, forecasting, insights, visuals
from src.cleaning import clean_sales

CLEAN_PATH = ROOT / "data" / "processed" / "clean_sales.csv"

st.set_page_config(
    page_title="Sales Analytics Pro",
    page_icon="📊",
    layout="wide"
)

# ---------- Custom design ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1120, #111c32);
    color: #f8fafc;
}
[data-testid="stSidebar"] {
    background-color: #111827;
}
[data-testid="stMetric"] {
    background: #1e293b;
    padding: 18px;
    border: 1px solid #334155;
    border-radius: 12px;
}
[data-testid="stMetricLabel"] {
    color: #cbd5e1;
}
[data-testid="stMetricValue"] {
    color: #60a5fa;
}
h1, h2, h3 {
    color: #f8fafc;
}
div[data-testid="stTabs"] button {
    color: #93c5fd;
}
</style>
""", unsafe_allow_html=True)


# ---------- Header ----------
st.title("📊 Sales Analytics Pro")
st.caption("SMART SALES INTELLIGENCE • Understand. Analyse. Forecast.")
st.divider()


# ---------- Load data ----------
@st.cache_data
def load_default():
    return pd.read_csv(
        CLEAN_PATH,
        parse_dates=["order_date", "month_start"]
    )


uploaded = st.sidebar.file_uploader(
    "Upload sales CSV",
    type=["csv"]
)

if uploaded is not None:
    try:
        data = clean_sales(pd.read_csv(uploaded))
    except Exception as error:
        st.error(f"Could not process this CSV: {error}")
        st.stop()
elif CLEAN_PATH.exists():
    data = load_default()
else:
    st.error("Sales data not found. Run python run_pipeline.py first.")
    st.stop()


# ---------- Sidebar filters ----------
st.sidebar.title("⚙️ Dashboard Controls")

min_day = data["order_date"].min().date()
max_day = data["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_day, max_day),
    min_value=min_day,
    max_value=max_day
)

regions = sorted(data["region"].dropna().unique())
categories = sorted(data["category"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select regions",
    regions,
    default=regions
)

selected_categories = st.sidebar.multiselect(
    "Select categories",
    categories,
    default=categories
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = min_day, max_day

df = data[
    data["order_date"].between(
        pd.Timestamp(start),
        pd.Timestamp(end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    )
    & data["region"].isin(selected_regions)
    & data["category"].isin(selected_categories)
]

if df.empty:
    st.warning("No sales found. Please change your filters.")
    st.stop()


# ---------- KPI cards ----------
kpis = analysis.kpi_summary(df)

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"${kpis['total_revenue']:,.0f}")
c2.metric("🛒 Total Orders", f"{kpis['total_orders']:,}")
c3.metric("📦 Units Sold", f"{kpis['units_sold']:,}")
c4.metric("👥 Customers", f"{kpis['unique_customers']:,}")

st.divider()


# ---------- Dashboard tabs ----------
overview, products, forecast, customers = st.tabs([
    "📈 Overview",
    "🏆 Products & Regions",
    "🔮 Forecast",
    "👥 Insights & Customers"
])

with overview:
    st.subheader("Revenue Performance")
    monthly = analysis.monthly_revenue(df)
    st.pyplot(visuals.revenue_trend_fig(monthly))

    st.subheader("Sales Activity")
    matrix = analysis.weekday_month_matrix(df)
    st.pyplot(visuals.heatmap_fig(matrix))

with products:
    left, right = st.columns(2)

    with left:
        st.subheader("Top Products")
        top = analysis.top_products(df, 10)
        st.pyplot(visuals.top_products_fig(top))

    with right:
        st.subheader("Regional Sales")
        region_data = analysis.revenue_by(df, "region")
        st.pyplot(
            visuals.share_donut_fig(
                region_data, "region", "Revenue by Region"
            )
        )

    st.subheader("Category Performance")
    category_data = analysis.revenue_by(df, "category")
    st.pyplot(
        visuals.share_donut_fig(
            category_data, "category", "Revenue by Category"
        )
    )

    st.dataframe(top, use_container_width=True)

with forecast:
    st.subheader("Predict Future Revenue")
    series = analysis.monthly_series(df)

    if len(series) < 24:
        st.info("Select at least 24 months of sales history for forecasting.")
    else:
        months = st.slider("Months to predict", 3, 12, 6)

        try:
            forecast_df, model_name = forecasting.forecast_future(
                series, months
            )

            st.pyplot(
                visuals.forecast_fig(series, forecast_df, model_name)
            )

            st.caption(f"Forecast model: {model_name}")
            st.dataframe(
                forecast_df.round(2),
                use_container_width=True
            )
        except Exception as error:
            st.warning(f"Forecast could not be generated: {error}")

with customers:
    st.subheader("Automatic Business Insights")

    for line in insights.generate_insights(df):
        st.info(f"💡 {line}")

    st.subheader("Customer Segments")

    if df["customer_id"].nunique() < 8:
        st.info("Select more data to display customer segments.")
    else:
        segments = analysis.rfm_table(df)["segment"].value_counts()
        st.bar_chart(segments)

    st.subheader("Filtered Sales Records")
    st.dataframe(df.head(100), use_container_width=True)

# ---------- Download ----------
st.divider()

st.download_button(
    "⬇️ Download Filtered Sales CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales.csv",
    mime="text/csv"
)

st.caption("Smart Sales Analysis & Visualization System | Team Project")
