from fastapi import FastAPI
from app.api import mock_routes, analytics_routes

app = FastAPI(
    title="E-commerce Analytics Backend",
    description="High-performance backend service for ingesting and analyzing e-commerce data",
    version="1.0.0"
)

# Registering the mock routes for ingestion
app.include_router(mock_routes.router, tags=["Mock API"])

# Registering the analytics routes for the dashboard
app.include_router(analytics_routes.router, tags=["Analytics API"])

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce Analytics API. Check /docs for endpoints."}