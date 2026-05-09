from __future__ import annotations

from monitoring.data_quality_checks import run_data_quality_checks
from pipelines.ingest_events import ingest_events
from pipelines.ingest_inventory import ingest_inventory
from pipelines.ingest_orders import ingest_orders
from pipelines.load_warehouse import load_warehouse
from pipelines.transform_orders import transform_orders
from pipelines.transform_users import transform_users
from scripts.generate_sample_data import main as generate_sample_data
from utils.helpers import ensure_directories
from utils.logger import get_logger


logger = get_logger("main")


def main() -> None:
    ensure_directories()
    logger.info("Starting Data Engineering Platform local run")
    generate_sample_data()
    ingest_orders()
    ingest_inventory()
    ingest_events()
    transform_orders()
    transform_users()
    load_warehouse()
    run_data_quality_checks()
    logger.info("Finished local data platform run")


if __name__ == "__main__":
    main()
