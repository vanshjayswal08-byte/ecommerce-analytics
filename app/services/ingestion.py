import asyncio
import httpx
from datetime import datetime
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

API_BASE = "http://localhost:8000"
LIMIT = 10000  # Fetch and insert in chunks of 10,000

async def ingest_table(endpoint: str, table_name: str, columns: list):
    print(f"Starting ingestion for {table_name}...")
    page = 1
    total_inserted = 0
    
    # Define columns that require datetime object conversion
    date_columns = {"joined_at", "created_at", "processed_at"}
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"{API_BASE}/mock/{endpoint}?page={page}&limit={LIMIT}"
                response = await client.get(url, timeout=60.0)
                response.raise_for_status()
                
                data = response.json()
                records = data.get("data", [])
                
                if not records:
                    break
                
                # Transform string dates into Python datetime objects for asyncpg
                for record in records:
                    for col in date_columns:
                        if col in record and record[col]:
                            # Replace Z with standard offset for safe parsing if present
                            date_str = record[col].replace('Z', '+00:00')
                            record[col] = datetime.fromisoformat(date_str)
                    
                async with AsyncSessionLocal() as session:
                    binds = ", ".join([f":{col}" for col in columns])
                    query = text(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({binds}) ON CONFLICT DO NOTHING")
                    
                    await session.execute(query, records)
                    await session.commit()
                    
                total_inserted += len(records)
                print(f"[{table_name}] Inserted {total_inserted}/{data.get('total_records')} records (Page {page}/{data.get('total_pages')})")
                
                if page >= data.get("total_pages", 1):
                    break
                    
                page += 1
            except Exception as e:
                print(f"Error on page {page} of {endpoint}: {e}")
                break

async def run_ingestion():
    print("Starting Pipeline...")
    
    await ingest_table("customers", "customers", ["id", "name", "email", "joined_at"])
    await ingest_table("orders", "orders", ["id", "customer_id", "amount", "created_at"])
    await ingest_table("refunds", "refunds", ["id", "order_id", "amount", "reason", "processed_at"])
    
    print("Refreshing Materialized View (mv_customer_spend)...")
    async with AsyncSessionLocal() as session:
        await session.execute(text("REFRESH MATERIALIZED VIEW mv_customer_spend"))
        await session.commit()
        
    print("Data Ingestion Pipeline Complete!")

if __name__ == "__main__":
    asyncio.run(run_ingestion())