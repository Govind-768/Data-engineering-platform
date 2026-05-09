from __future__ import annotations

import pandas as pd

from utils.helpers import ensure_directories, project_path, require_columns
from utils.logger import get_logger


logger = get_logger("ingest_inventory")
REQUIRED_COLUMNS = [
    "inventory_id",
    "product_id",
    "stock_on_hand",
    "warehouse_city",
    "last_restock_date",
    "movement_type",
    "movement_quantity",
]


def ingest_inventory() -> pd.DataFrame:
    ensure_directories()
    source = project_path("data", "raw", "inventory.csv")
    target = project_path("data", "processed", "inventory_clean.csv")

    inventory = pd.read_csv(source, parse_dates=["last_restock_date"])
    require_columns(inventory, REQUIRED_COLUMNS, "inventory")
    inventory = inventory.drop_duplicates(subset=["inventory_id"]).copy()
    inventory = inventory[inventory["stock_on_hand"] >= 0]
    inventory["ingested_at"] = pd.Timestamp.utcnow()
    inventory.to_csv(target, index=False)
    logger.info("Ingested %s inventory rows into %s", len(inventory), target)
    return inventory


if __name__ == "__main__":
    ingest_inventory()
