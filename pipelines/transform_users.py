from __future__ import annotations

import pandas as pd

from utils.helpers import ensure_directories, project_path
from utils.logger import get_logger


logger = get_logger("transform_users")


def transform_users() -> pd.DataFrame:
    ensure_directories()
    users = pd.read_csv(project_path("data", "raw", "users.csv"), parse_dates=["signup_date"])
    orders = pd.read_csv(project_path("data", "processed", "orders_clean.csv"), parse_dates=["order_date"])
    events = pd.read_csv(project_path("data", "processed", "events_clean.csv"), parse_dates=["event_ts"])

    order_features = orders.groupby("user_id", as_index=False).agg(
        lifetime_orders=("order_id", "nunique"),
        lifetime_gmv=("order_amount", "sum"),
        last_order_date=("order_date", "max"),
    )
    event_features = events.groupby("user_id", as_index=False).agg(
        sessions=("session_id", "nunique"),
        last_event_ts=("event_ts", "max"),
    )

    transformed = users.merge(order_features, on="user_id", how="left").merge(
        event_features, on="user_id", how="left"
    )
    transformed["lifetime_orders"] = transformed["lifetime_orders"].fillna(0).astype(int)
    transformed["lifetime_gmv"] = transformed["lifetime_gmv"].fillna(0)
    transformed["sessions"] = transformed["sessions"].fillna(0).astype(int)
    transformed["is_repeat_user"] = transformed["lifetime_orders"] > 1
    transformed.to_csv(project_path("data", "processed", "users_transformed.csv"), index=False)
    logger.info("Transformed %s users", len(transformed))
    return transformed


if __name__ == "__main__":
    transform_users()
