-- Revenue aggregation by day.
SELECT
    DATE(order_date) AS order_day,
    COUNT(DISTINCT order_id) AS orders,
    SUM(order_amount) AS gmv,
    SUM(net_revenue) AS net_revenue,
    AVG(order_amount) AS average_order_value
FROM fact_orders
GROUP BY DATE(order_date)
ORDER BY order_day;

-- Repeat user logic.
SELECT
    COUNT(*) AS total_users,
    SUM(CASE WHEN is_repeat_user = 1 THEN 1 ELSE 0 END) AS repeat_users,
    ROUND(100.0 * SUM(CASE WHEN is_repeat_user = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_user_pct
FROM dim_users;

-- Refund metrics.
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN refund_amount > 0 THEN 1 ELSE 0 END) AS refunded_orders,
    ROUND(100.0 * SUM(CASE WHEN refund_amount > 0 THEN 1 ELSE 0 END) / COUNT(DISTINCT order_id), 2) AS refund_pct,
    SUM(refund_amount) AS total_refunds
FROM fact_orders;

-- Product performance.
SELECT
    p.category,
    p.product_name,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(o.quantity) AS units_sold,
    SUM(o.order_amount) AS gmv
FROM fact_orders o
JOIN dim_products p ON o.product_id = p.product_id
GROUP BY p.category, p.product_name
ORDER BY gmv DESC
LIMIT 20;

-- Inventory summary.
SELECT
    p.category,
    COUNT(*) AS sku_count,
    SUM(i.stock_on_hand) AS stock_on_hand,
    SUM(CASE WHEN i.stock_on_hand < 20 THEN 1 ELSE 0 END) AS low_stock_skus
FROM fact_inventory_movements i
JOIN dim_products p ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY low_stock_skus DESC;
