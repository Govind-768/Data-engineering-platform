from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
try:
    from faker import Faker
except ModuleNotFoundError:
    Faker = None

from utils.helpers import ensure_directories, project_path
from utils.logger import get_logger


if Faker:
    fake = Faker("en_IN")
    Faker.seed(42)
else:
    fake = None
random.seed(42)
np.random.seed(42)
logger = get_logger("sample_data")


CITIES = ["Bengaluru", "Mumbai", "Delhi", "Pune", "Hyderabad", "Chennai"]
CATEGORIES = ["streetwear", "sneakers", "denim", "ethnic", "accessories", "athleisure"]
CAMPAIGNS = ["instagram_drop", "creator_collab", "first_order", "festive_flash", "app_push"]
FIRST_NAMES = ["Aarav", "Anaya", "Kabir", "Isha", "Riya", "Vivaan", "Meera", "Arjun"]
LAST_NAMES = ["Sharma", "Singh", "Patel", "Rao", "Nair", "Mehta", "Kapoor", "Das"]
STYLE_WORDS = ["Nova", "Flux", "Core", "Rush", "Muse", "Edge", "Pop", "Wave"]


def fake_name() -> str:
    if fake:
        return fake.name()
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def fake_word() -> str:
    if fake:
        return fake.word()
    return random.choice(STYLE_WORDS)


def make_users(count: int = 1_000) -> pd.DataFrame:
    start = datetime.now() - timedelta(days=180)
    return pd.DataFrame(
        {
            "user_id": [f"U{i:05d}" for i in range(1, count + 1)],
            "name": [fake_name() for _ in range(count)],
            "city": np.random.choice(CITIES, count),
            "signup_date": [start + timedelta(days=random.randint(0, 180)) for _ in range(count)],
            "acquisition_channel": np.random.choice(
                ["instagram", "referral", "google", "campus", "influencer"], count
            ),
            "age_group": np.random.choice(["18-21", "22-25", "26-30", "31-35"], count),
        }
    )


def make_products(count: int = 250) -> pd.DataFrame:
    products = []
    for i in range(1, count + 1):
        category = random.choice(CATEGORIES)
        price = round(random.uniform(399, 4999), 2)
        products.append(
            {
                "product_id": f"P{i:04d}",
                "product_name": f"{category.title()} {fake_word().title()}",
                "category": category,
                "brand": random.choice(["Slikk Lab", "Campus Club", "Metro Muse", "Drop Culture"]),
                "price": price,
                "cost": round(price * random.uniform(0.42, 0.68), 2),
            }
        )
    return pd.DataFrame(products)


def make_orders(users: pd.DataFrame, products: pd.DataFrame, count: int = 5_000) -> pd.DataFrame:
    rows = []
    now = datetime.now()
    for i in range(1, count + 1):
        product = products.sample(1).iloc[0]
        quantity = random.choices([1, 2, 3], weights=[0.76, 0.19, 0.05])[0]
        order_date = now - timedelta(days=random.randint(0, 90), minutes=random.randint(0, 1440))
        status = random.choices(
            ["delivered", "cancelled", "failed", "returned"],
            weights=[0.84, 0.06, 0.04, 0.06],
        )[0]
        rows.append(
            {
                "order_id": f"O{i:06d}",
                "user_id": users.sample(1).iloc[0]["user_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "order_amount": round(product["price"] * quantity, 2),
                "order_date": order_date,
                "city": random.choice(CITIES),
                "delivery_minutes": random.randint(18, 110),
                "status": status,
                "campaign_id": random.choice(CAMPAIGNS),
            }
        )
    return pd.DataFrame(rows)


def make_inventory(products: pd.DataFrame) -> pd.DataFrame:
    rows = []
    now = datetime.now()
    for _, product in products.iterrows():
        stock = random.randint(0, 250)
        rows.append(
            {
                "inventory_id": f"I{len(rows) + 1:05d}",
                "product_id": product["product_id"],
                "stock_on_hand": stock,
                "warehouse_city": random.choice(CITIES),
                "last_restock_date": now - timedelta(days=random.randint(0, 30)),
                "movement_type": random.choice(["restock", "sale", "return", "adjustment"]),
                "movement_quantity": random.randint(1, 80),
            }
        )
    return pd.DataFrame(rows)


def make_events(users: pd.DataFrame, products: pd.DataFrame, count: int = 20_000) -> pd.DataFrame:
    event_types = ["app_open", "product_view", "add_to_cart", "wishlist", "checkout", "purchase"]
    now = datetime.now()
    rows = []
    for i in range(1, count + 1):
        rows.append(
            {
                "event_id": f"E{i:07d}",
                "user_id": users.sample(1).iloc[0]["user_id"],
                "product_id": products.sample(1).iloc[0]["product_id"],
                "event_type": random.choices(event_types, weights=[22, 38, 15, 10, 9, 6])[0],
                "event_ts": now - timedelta(days=random.randint(0, 30), seconds=random.randint(0, 86400)),
                "session_id": f"S{random.randint(1, 7000):06d}",
                "device": random.choice(["ios", "android", "web"]),
                "campaign_id": random.choice(CAMPAIGNS),
            }
        )
    return pd.DataFrame(rows)


def make_payments(orders: pd.DataFrame) -> pd.DataFrame:
    paid_orders = orders[orders["status"].isin(["delivered", "returned"])]
    rows = []
    for i, (_, order) in enumerate(paid_orders.iterrows(), start=1):
        rows.append(
            {
                "payment_id": f"PAY{i:06d}",
                "order_id": order["order_id"],
                "payment_method": random.choice(["upi", "card", "wallet", "cod"]),
                "payment_status": random.choices(["success", "failed"], weights=[96, 4])[0],
                "payment_amount": order["order_amount"],
                "payment_ts": pd.to_datetime(order["order_date"]) + timedelta(minutes=random.randint(1, 8)),
            }
        )
    return pd.DataFrame(rows)


def make_refunds(orders: pd.DataFrame) -> pd.DataFrame:
    refund_orders = orders[orders["status"].isin(["returned", "cancelled"])].copy()
    rows = []
    for i, (_, order) in enumerate(refund_orders.iterrows(), start=1):
        rows.append(
            {
                "refund_id": f"R{i:05d}",
                "order_id": order["order_id"],
                "refund_reason": random.choice(["size_issue", "late_delivery", "quality_issue", "changed_mind"]),
                "refund_amount": round(order["order_amount"] * random.uniform(0.7, 1.0), 2),
                "refund_ts": pd.to_datetime(order["order_date"]) + timedelta(days=random.randint(1, 7)),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    ensure_directories()
    raw_dir = project_path("data", "raw")

    users = make_users()
    products = make_products()
    orders = make_orders(users, products)
    inventory = make_inventory(products)
    events = make_events(users, products)
    payments = make_payments(orders)
    refunds = make_refunds(orders)

    datasets = {
        "users.csv": users,
        "products.csv": products,
        "orders.csv": orders,
        "inventory.csv": inventory,
        "events.csv": events,
        "payments.csv": payments,
        "refunds.csv": refunds,
    }
    for filename, frame in datasets.items():
        frame.to_csv(raw_dir / filename, index=False)
        logger.info("Generated %s with %s rows", filename, len(frame))


if __name__ == "__main__":
    main()
