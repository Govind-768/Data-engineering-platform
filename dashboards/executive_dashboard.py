from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "data" / "warehouse" / "data_warehouse.db"


@st.cache_data
def read_sql(query: str) -> pd.DataFrame:
    with sqlite3.connect(WAREHOUSE) as conn:
        return pd.read_sql_query(query, conn)


st.set_page_config(page_title="Executive Dashboard", page_icon="📊", layout="wide")
st.title("Executive Dashboard")

if not WAREHOUSE.exists():
    st.warning("Warehouse database not found. Run `python main.py` first.")
    st.stop()

kpis = read_sql(
    """
    SELECT
        SUM(order_amount) AS gmv,
        SUM(net_revenue) AS net_revenue,
        AVG(order_amount) AS aov,
        COUNT(DISTINCT order_id) AS orders,
        100.0 * SUM(CASE WHEN refund_amount > 0 THEN 1 ELSE 0 END) / COUNT(*) AS refund_pct
    FROM fact_orders
    """
)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("GMV", f"Rs {kpis.loc[0, 'gmv']:,.0f}")
col2.metric("Net Revenue", f"Rs {kpis.loc[0, 'net_revenue']:,.0f}")
col3.metric("AOV", f"Rs {kpis.loc[0, 'aov']:,.0f}")
col4.metric("Orders", f"{int(kpis.loc[0, 'orders']):,}")
col5.metric("Refund %", f"{kpis.loc[0, 'refund_pct']:.2f}%")

daily = read_sql(
    """
    SELECT DATE(order_date) AS order_day, SUM(order_amount) AS gmv, COUNT(*) AS orders
    FROM fact_orders
    GROUP BY DATE(order_date)
    ORDER BY order_day
    """
)
top_products = read_sql(
    """
    SELECT p.product_name, p.category, SUM(o.order_amount) AS gmv
    FROM fact_orders o
    JOIN dim_products p ON o.product_id = p.product_id
    GROUP BY p.product_name, p.category
    ORDER BY gmv DESC
    LIMIT 10
    """
)
city = read_sql(
    """
    SELECT city, COUNT(*) AS orders, SUM(order_amount) AS gmv
    FROM fact_orders
    GROUP BY city
    ORDER BY gmv DESC
    """
)
campaign = read_sql(
    """
    SELECT campaign_id, gmv, spend, roi
    FROM fact_campaign_performance
    ORDER BY roi DESC
    """
)
inventory = read_sql(
    """
    SELECT p.category, SUM(i.stock_on_hand) AS stock_on_hand,
           SUM(CASE WHEN i.stock_on_hand < 20 THEN 1 ELSE 0 END) AS low_stock_skus
    FROM fact_inventory_movements i
    JOIN dim_products p ON i.product_id = p.product_id
    GROUP BY p.category
    """
)

left, right = st.columns(2)
left.plotly_chart(px.line(daily, x="order_day", y="gmv", title="Daily GMV"), use_container_width=True)
right.plotly_chart(px.bar(city, x="city", y="gmv", title="GMV by City"), use_container_width=True)

left, right = st.columns(2)
left.plotly_chart(px.bar(top_products, x="gmv", y="product_name", color="category", title="Top Products", orientation="h"), use_container_width=True)
right.plotly_chart(px.bar(campaign, x="campaign_id", y="roi", title="Campaign ROI"), use_container_width=True)

st.plotly_chart(px.bar(inventory, x="category", y=["stock_on_hand", "low_stock_skus"], barmode="group", title="Inventory Health"), use_container_width=True)
