# app/services/generator.py
import csv
import uuid
import random
import os
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker with a fixed seed for reproducibility [cite: 81]
fake = Faker()
Faker.seed(42)
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.csv")
REFUNDS_FILE = os.path.join(DATA_DIR, "refunds.csv")

def generate_mock_data():
    print("Starting data generation... (This might take a few minutes)")
    
    # 1. Generate Customers (100,000) [cite: 82]
    customer_ids = []
    if not os.path.exists(CUSTOMERS_FILE):
        print("Generating 100,000 Customers...")
        with open(CUSTOMERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "email", "joined_at"])
            for _ in range(100_000):
                c_id = str(uuid.uuid4())
                customer_ids.append(c_id)
                joined_at = fake.date_time_between(start_date='-2y', end_date='now')
                writer.writerow([c_id, fake.name(), fake.unique.email(), joined_at.isoformat()])
    else:
        print("Customers file already exists. Loading IDs...")
        import pandas as pd
        df = pd.read_csv(CUSTOMERS_FILE, usecols=['id'])
        customer_ids = df['id'].tolist()

    # 2. Generate Orders (1,000,000) [cite: 83]
    order_ids = []
    if not os.path.exists(ORDERS_FILE):
        print("Generating 1,000,000 Orders...")
        with open(ORDERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "customer_id", "amount", "created_at"])
            for _ in range(1_000_000):
                o_id = str(uuid.uuid4())
                order_ids.append(o_id)
                c_id = random.choice(customer_ids)
                amount = round(random.uniform(10.0, 1500.0), 2)
                created_at = fake.date_time_between(start_date='-1y', end_date='now')
                writer.writerow([o_id, c_id, amount, created_at.isoformat()])
    else:
        print("Orders file already exists. Loading IDs...")
        import pandas as pd
        df = pd.read_csv(ORDERS_FILE, usecols=['id'])
        order_ids = df['id'].tolist()

    # 3. Generate Refunds (200,000) [cite: 83]
    if not os.path.exists(REFUNDS_FILE):
        print("Generating 200,000 Refunds...")
        with open(REFUNDS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "order_id", "amount", "reason", "processed_at"])
            refunded_orders = random.sample(order_ids, 200_000)
            for o_id in refunded_orders:
                r_id = str(uuid.uuid4())
                amount = round(random.uniform(5.0, 500.0), 2)
                processed_at = fake.date_time_between(start_date='-6m', end_date='now')
                reason = random.choice(["Defective", "Not Needed", "Wrong Item", "Late Delivery"])
                writer.writerow([r_id, o_id, amount, reason, processed_at.isoformat()])
    
    print("Data Generation Complete!")

if __name__ == "__main__":
    generate_mock_data()