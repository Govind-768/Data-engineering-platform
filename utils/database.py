from __future__ import annotations

import sqlite3
from pathlib import Path

from utils.helpers import project_path


WAREHOUSE_PATH = project_path("data", "warehouse", "slikk_warehouse.db")


def get_connection() -> sqlite3.Connection:
    WAREHOUSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(WAREHOUSE_PATH)


def execute_sql_file(sql_path: Path) -> None:
    with get_connection() as conn:
        conn.executescript(sql_path.read_text(encoding="utf-8"))
