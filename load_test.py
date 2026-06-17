import asyncio
import httpx
import time

API_BASE = "http://localhost:8000/analytics"

# Endpoints to be tested for performance
ENDPOINTS = [
    "/total-orders",
    "/total-revenue",
    "/total-refunds",
    "/net-revenue",
    "/average-order-value",
    "/repeat-customer-revenue",
    "/revenue-trends?interval=monthly",
    "/top-customers-by-spend?limit=10"
]

CONCURRENT_REQUESTS = 50  # Number of simultaneous requests per endpoint

async def fetch_endpoint(client, endpoint):
    start_time = time.time()
    try:
        response = await client.get(f"{API_BASE}{endpoint}")
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds
        return latency, response.status_code
    except Exception as e:
        return None, 500

async def run_load_test():
    print(f"Starting Load Test ({CONCURRENT_REQUESTS} concurrent requests per endpoint)...\n")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for endpoint in ENDPOINTS:
            print(f"Testing: {endpoint}")
            
            # WARM-UP PHASE: Prevent Cache Stampede
            # Send 1 single request first to prime the Redis cache
            await fetch_endpoint(client, endpoint)
            
            # LOAD PHASE: Fire all concurrent requests simultaneously
            tasks = [fetch_endpoint(client, endpoint) for _ in range(CONCURRENT_REQUESTS)]
            results = await asyncio.gather(*tasks)
            
            # Filter successfully completed requests
            latencies = [res[0] for res in results if res[0] is not None and res[1] == 200]
            
            if latencies:
                avg_time = sum(latencies) / len(latencies)
                max_time = max(latencies)
                min_time = min(latencies)
                
                print(f"   -> Success Rate: {len(latencies)}/{CONCURRENT_REQUESTS}")
                print(f"   -> Fastest: {min_time:.2f} ms | Average: {avg_time:.2f} ms | Slowest: {max_time:.2f} ms")
                print(f"   -> Meets < 2s (2000ms) Requirement: {'YES' if max_time < 2000 else 'NO'}\n")
            else:
                print(f"   -> All requests failed for this endpoint.\n")

if __name__ == "__main__":
    asyncio.run(run_load_test())