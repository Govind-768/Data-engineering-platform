from __future__ import annotations

import pandas as pd

from utils.helpers import ensure_directories, project_path, require_columns
from utils.logger import get_logger


logger = get_logger("ingest_orders")
REQUIRED_COLUMNS = [
    "order_id",
    "user_id",
    "product_id",
    "quantity",
    "order_amount",
    "order_date",
    "city",
    "delivery_minutes",
    "status",
    "campaign_id",
]


def ingest_orders() -> pd.DataFrame:
    ensure_directories()
    source = project_path("data", "raw", "orders.csv")
    target = project_path("data", "processed", "orders_clean.csv")

    orders = pd.read_csv(source, parse_dates=["order_date"])
    require_columns(orders, REQUIRED_COLUMNS, "orders")
    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    orders = orders[orders["order_amount"] >= 0]
    orders["ingested_at"] = pd.Timestamp.utcnow()
    orders.to_csv(target, index=False)
    logger.info("Ingested %s cleaned orders into %s", len(orders), target)
    return orders


if __name__ == "__main__":
    ingest_orders()
