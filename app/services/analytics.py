import json
import time
import redis.asyncio as redis
from sqlalchemy import text
from app.core.database import AsyncSessionLocal
from app.core.config import settings

# Initialize Redis client
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
CACHE_TTL = 300  # 5 minutes cache [cite: 28]

async def get_cached_or_execute(cache_key: str, query: str, fetch_all: bool = False, params: dict | None= None):
    """Generic function to check Redis cache first, then execute DB query if needed."""
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    async with AsyncSessionLocal() as session:
        result = await session.execute(text(query), params or {})
        
        if fetch_all:
            # Convert rows to list of dicts
            data = [dict(row._mapping) for row in result.fetchall()]
            # Handle dates/decimals for JSON serialization
            data = json.loads(json.dumps(data, default=str)) 
        else:
            row = result.fetchone()
            data = dict(row._mapping) if row else {}
            data = json.loads(json.dumps(data, default=str))

    await redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
    return data

async def get_totals():
    query = """
        SELECT 
            (SELECT COUNT(*) FROM orders) as total_orders,
            (SELECT COALESCE(SUM(amount), 0) FROM orders) as total_revenue,
            (SELECT COALESCE(SUM(amount), 0) FROM refunds) as total_refunds,
            (SELECT COALESCE(SUM(amount), 0) FROM orders) - 
            (SELECT COALESCE(SUM(amount), 0) FROM refunds) as net_revenue
    """
    return await get_cached_or_execute("analytics:totals", query)

async def get_aov():
    query = "SELECT COALESCE(AVG(amount), 0) as average_order_value FROM orders"
    return await get_cached_or_execute("analytics:aov", query)

async def get_top_customers(limit: int = 10):
    # Utilizing the materialized view for instant sub-2s response [cite: 27]
    query = f"""
        SELECT customer_id, name, email, net_spend 
        FROM mv_customer_spend 
        ORDER BY net_spend DESC 
        LIMIT :limit
    """
    cache_key = f"analytics:top_customers:{limit}"
    return await get_cached_or_execute(cache_key, query, fetch_all=True, params={"limit": limit})

async def get_revenue_trends(interval: str = 'daily'):
    date_trunc_param = 'day'
    if interval == 'weekly':
        date_trunc_param = 'week'
    elif interval == 'monthly':
        date_trunc_param = 'month'

    query = f"""
        SELECT 
            DATE_TRUNC('{date_trunc_param}', created_at) as trend_date,
            SUM(amount) as revenue
        FROM orders
        GROUP BY trend_date
        ORDER BY trend_date ASC
    """
    cache_key = f"analytics:revenue_trends:{interval}"
    return await get_cached_or_execute(cache_key, query, fetch_all=True)
async def get_repeat_customer_revenue():
    # Calculating revenue only from customers who have more than 1 order
    query = """
        SELECT COALESCE(SUM(amount), 0) as repeat_customer_revenue
        FROM orders
        WHERE customer_id IN (
            SELECT customer_id 
            FROM orders 
            GROUP BY customer_id 
            HAVING COUNT(id) > 1
        )
    """
    return await get_cached_or_execute("analytics:repeat_revenue", query)