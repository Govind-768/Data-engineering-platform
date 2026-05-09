from __future__ import annotations

import pandas as pd

from utils.database import execute_sql_file, get_connection
from utils.helpers import ensure_directories, project_path
from utils.logger import get_logger


logger = get_logger("load_warehouse")


def load_warehouse() -> None:
    ensure_directories()
    execute_sql_file(project_path("sql", "warehouse_schema.sql"))

    users = pd.read_csv(project_path("data", "processed", "users_transformed.csv"))
    products = pd.read_csv(project_path("data", "raw", "products.csv"))
    orders = pd.read_csv(project_path("data", "processed", "orders_transformed.csv"), parse_dates=["order_date"])
    payments = pd.read_csv(project_path("data", "raw", "payments.csv"))
    events = pd.read_csv(project_path("data", "processed", "events_clean.csv"))
    inventory = pd.read_csv(project_path("data", "processed", "inventory_clean.csv"))

    dim_time = pd.DataFrame({"date": pd.to_datetime(orders["order_date"]).dt.date.unique()})
    dim_time["date_key"] = pd.to_datetime(dim_time["date"]).dt.strftime("%Y%m%d").astype(int)
    dim_time["day"] = pd.to_datetime(dim_time["date"]).dt.day
    dim_time["month"] = pd.to_datetime(dim_time["date"]).dt.month
    dim_time["year"] = pd.to_datetime(dim_time["date"]).dt.year
    dim_time["week"] = pd.to_datetime(dim_time["date"]).dt.isocalendar().week.astype(int)

    campaigns = sorted(set(orders["campaign_id"]).union(set(events["campaign_id"])))
    dim_campaigns = pd.DataFrame(
        {
            "campaign_id": campaigns,
            "campaign_name": [campaign.replace("_", " ").title() for campaign in campaigns],
            "channel": ["paid_social" if "instagram" in campaign or "creator" in campaign else "owned" for campaign in campaigns],
            "spend": [75_000 + i * 18_000 for i, _ in enumerate(campaigns)],
        }
    )

    fact_campaign = (
        orders.groupby("campaign_id", as_index=False)
        .agg(gmv=("order_amount", "sum"), orders=("order_id", "nunique"))
        .merge(dim_campaigns[["campaign_id", "spend"]], on="campaign_id", how="left")
    )
    fact_campaign["roi"] = (fact_campaign["gmv"] - fact_campaign["spend"]) / fact_campaign["spend"]

    delivery = orders[["order_id", "city", "delivery_minutes", "status"]].copy()
    delivery["met_sla"] = delivery["delivery_minutes"] <= 60

    with get_connection() as conn:
        users.to_sql("dim_users", conn, if_exists="replace", index=False)
        products.to_sql("dim_products", conn, if_exists="replace", index=False)
        dim_time.to_sql("dim_time", conn, if_exists="replace", index=False)
        dim_campaigns.to_sql("dim_campaigns", conn, if_exists="replace", index=False)
        delivery.to_sql("dim_delivery", conn, if_exists="replace", index=False)
        orders.to_sql("fact_orders", conn, if_exists="replace", index=False)
        payments.to_sql("fact_payments", conn, if_exists="replace", index=False)
        events.to_sql("fact_events", conn, if_exists="replace", index=False)
        inventory.to_sql("fact_inventory_movements", conn, if_exists="replace", index=False)
        fact_campaign.to_sql("fact_campaign_performance", conn, if_exists="replace", index=False)
    logger.info("Loaded warehouse tables into %s", project_path("data", "warehouse", "data_warehouse.db"))


if __name__ == "__main__":
    load_warehouse()
