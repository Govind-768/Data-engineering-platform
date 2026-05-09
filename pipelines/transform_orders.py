from __future__ import annotations

import pandas as pd

from utils.helpers import ensure_directories, project_path
from utils.logger import get_logger


logger = get_logger("transform_orders")


def transform_orders() -> pd.DataFrame:
    ensure_directories()
    orders = pd.read_csv(project_path("data", "processed", "orders_clean.csv"), parse_dates=["order_date"])
    payments = pd.read_csv(project_path("data", "raw", "payments.csv"), parse_dates=["payment_ts"])
    refunds = pd.read_csv(project_path("data", "raw", "refunds.csv"), parse_dates=["refund_ts"])

    payment_summary = payments.groupby("order_id", as_index=False).agg(
        payment_amount=("payment_amount", "sum"),
        payment_status=("payment_status", "last"),
    )
    refund_summary = refunds.groupby("order_id", as_index=False).agg(refund_amount=("refund_amount", "sum"))

    transformed = orders.merge(payment_summary, on="order_id", how="left").merge(
        refund_summary, on="order_id", how="left"
    )
    transformed["refund_amount"] = transformed["refund_amount"].fillna(0)
    transformed["payment_amount"] = transformed["payment_amount"].fillna(0)
    transformed["net_revenue"] = transformed["payment_amount"] - transformed["refund_amount"]
    transformed["is_completed"] = transformed["status"].eq("delivered")
    transformed["order_date_key"] = transformed["order_date"].dt.strftime("%Y%m%d").astype(int)
    transformed.to_csv(project_path("data", "processed", "orders_transformed.csv"), index=False)
    logger.info("Transformed %s orders", len(transformed))
    return transformed


if __name__ == "__main__":
    transform_orders()
