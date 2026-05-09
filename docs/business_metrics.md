# Business Metrics

## GMV

Gross merchandise value before refunds.

```sql
SUM(order_amount)
```

## Net Revenue

Successful payment value after refunds.

```sql
SUM(payment_amount) - SUM(refund_amount)
```

## Average Order Value

```sql
SUM(order_amount) / COUNT(DISTINCT order_id)
```

## Repeat User Percentage

Percentage of users with more than one order.

```sql
repeat_users / total_users
```

## Conversion Rate

Purchase events divided by commerce-intent events such as product views, add-to-cart, checkout, and purchases.

## Refund Percentage

Orders with refund value greater than zero divided by total orders.

## Delivery SLA

Percentage of deliveries completed within the business target of 60 minutes.

## Campaign ROI

```sql
(campaign_gmv - campaign_spend) / campaign_spend
```

## Inventory Health

Tracks stock on hand, movement quantity, and low-stock SKUs by category and city.

## Dashboard KPIs

The executive dashboard reports:

* GMV
* Net Revenue
* Average Order Value
* Refund Percentage
* Campaign ROI
* Repeat Users
* Inventory Health
* Product Performance
* City-wise Revenue

## Monitoring Validation

Metrics are validated using:

* duplicate checks
* freshness checks
* null checks
* schema validation