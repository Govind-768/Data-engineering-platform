from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from utils.helpers import project_path
from utils.logger import get_logger


logger = get_logger("data_quality")


@dataclass
class QualityCheckResult:
    dataset: str
    check: str
    passed: bool
    details: str


def check_required_columns(dataset: str, frame: pd.DataFrame, columns: list[str]) -> QualityCheckResult:
    missing = sorted(set(columns) - set(frame.columns))
    return QualityCheckResult(dataset, "schema", not missing, f"Missing columns: {missing}" if missing else "Schema valid")


def check_nulls(dataset: str, frame: pd.DataFrame, columns: list[str]) -> QualityCheckResult:
    null_counts = frame[columns].isna().sum()
    failures = null_counts[null_counts > 0].to_dict()
    return QualityCheckResult(dataset, "required_nulls", not failures, str(failures) if failures else "No nulls")


def check_duplicates(dataset: str, frame: pd.DataFrame, key: str) -> QualityCheckResult:
    duplicate_count = int(frame.duplicated(subset=[key]).sum())
    return QualityCheckResult(dataset, "duplicates", duplicate_count == 0, f"{duplicate_count} duplicate {key} values")


def check_freshness(dataset: str, frame: pd.DataFrame, timestamp_col: str, max_age_days: int = 3) -> QualityCheckResult:
    latest_ts = pd.to_datetime(frame[timestamp_col]).max()
    age_days = (pd.Timestamp.now(tz=None) - latest_ts.tz_localize(None)).days
    return QualityCheckResult(dataset, "freshness", age_days <= max_age_days, f"Latest timestamp is {age_days} days old")


def run_data_quality_checks() -> list[QualityCheckResult]:
    datasets = {
        "orders": {
            "path": project_path("data", "processed", "orders_clean.csv"),
            "key": "order_id",
            "timestamp": "order_date",
            "required": ["order_id", "user_id", "product_id", "order_amount", "order_date"],
        },
        "events": {
            "path": project_path("data", "processed", "events_clean.csv"),
            "key": "event_id",
            "timestamp": "event_ts",
            "required": ["event_id", "user_id", "event_type", "event_ts", "session_id"],
        },
        "inventory": {
            "path": project_path("data", "processed", "inventory_clean.csv"),
            "key": "inventory_id",
            "timestamp": "last_restock_date",
            "required": ["inventory_id", "product_id", "stock_on_hand", "last_restock_date"],
        },
    }

    results: list[QualityCheckResult] = []
    for name, config in datasets.items():
        frame = pd.read_csv(config["path"])
        required = config["required"]
        results.extend(
            [
                check_required_columns(name, frame, required),
                check_nulls(name, frame, required),
                check_duplicates(name, frame, config["key"]),
                check_freshness(name, frame, config["timestamp"]),
            ]
        )

    for result in results:
        level = "INFO" if result.passed else "ERROR"
        message = f"{result.dataset}.{result.check}: {result.details}"
        getattr(logger, level.lower())(message)
        print(f"[{'PASS' if result.passed else 'ALERT'}] {message}")
    return results


if __name__ == "__main__":
    run_data_quality_checks()
