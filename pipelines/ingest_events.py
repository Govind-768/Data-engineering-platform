from __future__ import annotations

import pandas as pd

from utils.helpers import ensure_directories, project_path, require_columns
from utils.logger import get_logger


logger = get_logger("ingest_events")
REQUIRED_COLUMNS = [
    "event_id",
    "user_id",
    "product_id",
    "event_type",
    "event_ts",
    "session_id",
    "device",
    "campaign_id",
]


def ingest_events() -> pd.DataFrame:
    ensure_directories()
    source = project_path("data", "raw", "events.csv")
    target = project_path("data", "processed", "events_clean.csv")

    events = pd.read_csv(source, parse_dates=["event_ts"])
    require_columns(events, REQUIRED_COLUMNS, "events")
    events = events.drop_duplicates(subset=["event_id"]).copy()
    events = events.dropna(subset=["user_id", "event_type", "event_ts"])
    events["ingested_at"] = pd.Timestamp.utcnow()
    events.to_csv(target, index=False)
    logger.info("Ingested %s event rows into %s", len(events), target)
    return events


if __name__ == "__main__":
    ingest_events()
