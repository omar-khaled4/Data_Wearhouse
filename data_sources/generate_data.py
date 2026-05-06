import pandas as pd
from faker import Faker
import random
import json
import os

fake = Faker()
random.seed(42)

# ── 1. Generate Customers CSV (simulates CDC source) ──────────────────
customers = []
customer_ids = [f"CUST_{i:04d}" for i in range(1, 201)]

for cid in customer_ids:
    customers.append({
        "customer_id":   cid,
        "customer_name": fake.name(),
        "email":         fake.email(),
        "country":       fake.country(),
        "signup_date":   str(fake.date_between(start_date="-3y", end_date="today"))
    })

pd.DataFrame(customers).to_csv("customers.csv", index=False)
print("✅ customers.csv generated")

# ── 2. Generate Orders CSV (simulates file drop source) ───────────────
product_ids = [f"PROD_{i:03d}" for i in range(1, 51)]
statuses    = ["completed", "pending", "cancelled", "refunded"]
orders      = []

for i in range(1, 1001):
    orders.append({
        "order_id":    f"ORD_{i:05d}",
        "customer_id": random.choice(customer_ids),
        "product_id":  random.choice(product_ids),
        "quantity":    random.randint(1, 20),
        "price":       round(random.uniform(5.0, 500.0), 2),
        "order_date":  str(fake.date_between(start_date="-1y", end_date="today")),
        "status":      random.choice(statuses)
    })

pd.DataFrame(orders).to_csv("orders.csv", index=False)
print("✅ orders.csv generated")

# ── 3. Generate App Logs JSON (simulates streaming logs) ──────────────
event_types = ["page_view", "click", "purchase", "logout", "login"]
pages       = ["/home", "/products", "/cart", "/checkout", "/profile"]
logs        = []

for i in range(1, 501):
    logs.append({
        "log_id":     f"LOG_{i:05d}",
        "user_id":    random.choice(customer_ids),
        "event_type": random.choice(event_types),
        "event_time": str(fake.date_time_this_year()),
        "page":       random.choice(pages)
    })

with open("app_logs.json", "w") as f:
    json.dump(logs, f, indent=2)
print("✅ app_logs.json generated")

print("\n🎉 All source data files generated successfully!")