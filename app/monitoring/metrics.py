from prometheus_client import Counter, Histogram, Info
from fastapi import Request
import time

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

API_INFO = Info('api_info', 'API information')

# Update API info
API_INFO.info({
    'version': '1.0.0',
    'name': 'MyAPI Gateway'
})

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    # Record request count and latency
    labels = {
        'method': request.method,
        'endpoint': request.url.path,
        'status': response.status_code
    }
    
    REQUEST_COUNT.labels(
        method=labels['method'],
        endpoint=labels['endpoint'],
        status=labels['status']
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=labels['method'],
        endpoint=labels['endpoint']
    ).observe(time.time() - start_time)
    
    return response