# app/api/mock_routes.py
from fastapi import APIRouter, Query, HTTPException
import pandas as pd
import os
import math

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_paginated_data(filepath: str, page: int, limit: int):
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Data file not found. Run generator first.")
    
    # Pandas chunking is very efficient for large datasets
    # Skip rows calculates the offset mathematically
    skip = (page - 1) * limit
    
    try:
        # We read just the chunk we need to save memory
        df_chunk = pd.read_csv(filepath, skiprows=range(1, skip + 1), nrows=limit)
        
        # Calculate total records (fast path: using WC or pre-calculated could be faster, 
        # but for mock API this is acceptable)
        with open(filepath, 'r', encoding="utf-8") as f:
            total_rows = sum(1 for _ in f) - 1 # Subtract header
            
        data = df_chunk.to_dict(orient='records')
        
        return {
            "page": page,
            "limit": limit,
            "total_records": total_rows,
            "total_pages": math.ceil(total_rows / limit),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mock/customers")
async def get_mock_customers(page: int = Query(1, ge=1), limit: int = Query(1000, ge=1, le=10000)):
    filepath = os.path.join(DATA_DIR, "customers.csv")
    return get_paginated_data(filepath, page, limit)

@router.get("/mock/orders")
async def get_mock_orders(page: int = Query(1, ge=1), limit: int = Query(1000, ge=1, le=10000)):
    filepath = os.path.join(DATA_DIR, "orders.csv")
    return get_paginated_data(filepath, page, limit)

@router.get("/mock/refunds")
async def get_mock_refunds(page: int = Query(1, ge=1), limit: int = Query(1000, ge=1, le=10000)):
    filepath = os.path.join(DATA_DIR, "refunds.csv")
    return get_paginated_data(filepath, page, limit)