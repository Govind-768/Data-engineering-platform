DROP TABLE IF EXISTS dim_users;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_time;
DROP TABLE IF EXISTS dim_campaigns;
DROP TABLE IF EXISTS dim_delivery;
DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS fact_payments;
DROP TABLE IF EXISTS fact_events;
DROP TABLE IF EXISTS fact_inventory_movements;
DROP TABLE IF EXISTS fact_campaign_performance;

CREATE TABLE dim_users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    city TEXT,
    signup_date TEXT,
    acquisition_channel TEXT,
    age_group TEXT,
    lifetime_orders INTEGER,
    lifetime_gmv REAL,
    last_order_date TEXT,
    sessions INTEGER,
    last_event_ts TEXT,
    is_repeat_user INTEGER
);

CREATE TABLE dim_products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price REAL,
    cost REAL
);

CREATE TABLE dim_time (
    date_key INTEGER PRIMARY KEY,
    date TEXT,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    week INTEGER
);

CREATE TABLE dim_campaigns (
    campaign_id TEXT PRIMARY KEY,
    campaign_name TEXT,
    channel TEXT,
    spend REAL
);

CREATE TABLE dim_delivery (
    order_id TEXT PRIMARY KEY,
    city TEXT,
    delivery_minutes INTEGER,
    status TEXT,
    met_sla INTEGER
);

CREATE TABLE fact_orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    order_amount REAL,
    order_date TEXT,
    city TEXT,
    delivery_minutes INTEGER,
    status TEXT,
    campaign_id TEXT,
    ingested_at TEXT,
    payment_amount REAL,
    payment_status TEXT,
    refund_amount REAL,
    net_revenue REAL,
    is_completed INTEGER,
    order_date_key INTEGER
);

CREATE TABLE fact_payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT,
    payment_method TEXT,
    payment_status TEXT,
    payment_amount REAL,
    payment_ts TEXT
);

CREATE TABLE fact_events (
    event_id TEXT PRIMARY KEY,
    user_id TEXT,
    product_id TEXT,
    event_type TEXT,
    event_ts TEXT,
    session_id TEXT,
    device TEXT,
    campaign_id TEXT,
    ingested_at TEXT
);

CREATE TABLE fact_inventory_movements (
    inventory_id TEXT PRIMARY KEY,
    product_id TEXT,
    stock_on_hand INTEGER,
    warehouse_city TEXT,
    last_restock_date TEXT,
    movement_type TEXT,
    movement_quantity INTEGER,
    ingested_at TEXT
);

CREATE TABLE fact_campaign_performance (
    campaign_id TEXT PRIMARY KEY,
    gmv REAL,
    orders INTEGER,
    spend REAL,
    roi REAL
);
