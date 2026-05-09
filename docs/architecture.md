# Architecture

This platform models a realistic first-version data stack for a quick-commerce fashion startup.

## Data Flow

1. Source-like CSV datasets are generated into `data/raw`.
2. Ingestion pipelines validate schema, remove duplicates, and add ingestion timestamps.
3. Processed datasets are written to `data/processed`.
4. Transformation pipelines create analytics-ready order and user records.
5. The warehouse loader creates a SQLite star schema in `data/warehouse`.
6. KPI SQL and Streamlit consume warehouse tables for reporting.
7. Airflow DAGs orchestrate daily sales, inventory sync, and campaign reporting.

## Layers

- Raw: immutable source extract simulation
- Processed: cleaned and validated data
- Warehouse: dimensional model for BI and analytics
- Monitoring: quality checks and alert-style output
- Analytics: SQL KPIs and executive dashboard

## Production Evolution

The local CSV and SQLite stack is intentionally simple for interview demonstration. At scale, raw files would live in object storage, ingestion would use APIs and streams, transformations would move into Spark or dbt, and the warehouse would run on Snowflake, BigQuery, Redshift, or Databricks SQL.
