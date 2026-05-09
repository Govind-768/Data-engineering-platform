-- GMV, revenue, AOV, refund percentage, and completion rate.
SELECT
    ROUND(SUM(order_amount), 2) AS gmv,
    ROUND(SUM(net_revenue), 2) AS net_revenue,
    ROUND(AVG(order_amount), 2) AS average_order_value,
    ROUND(100.0 * SUM(CASE WHEN refund_amount > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS refund_percentage,
    ROUND(100.0 * SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS order_completion_rate
FROM fact_orders;

-- Conversion rate from app engagement to purchase.
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN event_type IN ('product_view', 'add_to_cart', 'checkout', 'purchase') THEN 1 ELSE 0 END), 0),
        2
    ) AS conversion_rate
FROM fact_events;

-- Repeat user percentage.
SELECT
    ROUND(100.0 * SUM(CASE WHEN is_repeat_user = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_user_percentage
FROM dim_users;

-- Top products.
SELECT
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.order_amount), 2) AS gmv
FROM fact_orders o
JOIN dim_products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY gmv DESC
LIMIT 10;

-- Delivery SLA.
SELECT
    ROUND(100.0 * SUM(CASE WHEN met_sla = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS delivery_sla_pct,
    ROUND(AVG(delivery_minutes), 2) AS avg_delivery_minutes
FROM dim_delivery;

-- Campaign ROI.
SELECT
    campaign_id,
    ROUND(gmv, 2) AS gmv,
    ROUND(spend, 2) AS spend,
    ROUND(roi, 2) AS roi
FROM fact_campaign_performance
ORDER BY roi DESC;
