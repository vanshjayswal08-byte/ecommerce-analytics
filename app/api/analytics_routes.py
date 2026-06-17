import time
from fastapi import APIRouter, Query
from app.services import analytics

router = APIRouter()

def format_response(data, start_time):
    """Helper to format all responses with execution time."""
    execution_time_ms = round((time.time() - start_time) * 1000, 2)
    return {
        "success": True,
        "execution_time_ms": execution_time_ms,
        "data": data
    }

# 1. Total Orders
@router.get("/analytics/total-orders", summary="Get Total Orders")
async def get_total_orders():
    start_time = time.time()
    totals = await analytics.get_totals()
    return format_response({"total_orders": totals["total_orders"]}, start_time)

# 2. Total Revenue
@router.get("/analytics/total-revenue", summary="Get Total Revenue")
async def get_total_revenue():
    start_time = time.time()
    totals = await analytics.get_totals()
    return format_response({"total_revenue": totals["total_revenue"]}, start_time)

# 3. Total Refunds
@router.get("/analytics/total-refunds", summary="Get Total Refunds")
async def get_total_refunds():
    start_time = time.time()
    totals = await analytics.get_totals()
    return format_response({"total_refunds": totals["total_refunds"]}, start_time)

# 4. Net Revenue
@router.get("/analytics/net-revenue", summary="Get Net Revenue")
async def get_net_revenue():
    start_time = time.time()
    totals = await analytics.get_totals()
    return format_response({"net_revenue": totals["net_revenue"]}, start_time)

# 5. Average Order Value
@router.get("/analytics/average-order-value", summary="Get Average Order Value")
async def get_average_order_value():
    start_time = time.time()
    data = await analytics.get_aov()
    return format_response(data, start_time)

# 6. Repeat Customer Revenue
@router.get("/analytics/repeat-customer-revenue", summary="Get Repeat Customer Revenue")
async def get_repeat_customer_revenue():
    start_time = time.time()
    data = await analytics.get_repeat_customer_revenue()
    return format_response(data, start_time)

# 7. Revenue Trends
@router.get("/analytics/revenue-trends", summary="Get Revenue Trends")
async def get_revenue_trends(interval: str = Query('daily', regex="^(daily|weekly|monthly)$")):
    start_time = time.time()
    data = await analytics.get_revenue_trends(interval)
    return format_response(data, start_time)

# 8. Top Customers by Spend
@router.get("/analytics/top-customers-by-spend", summary="Get Top Customers by Spend")
async def get_top_customers(limit: int = Query(10, ge=1, le=100)):
    start_time = time.time()
    data = await analytics.get_top_customers(limit)
    return format_response(data, start_time)