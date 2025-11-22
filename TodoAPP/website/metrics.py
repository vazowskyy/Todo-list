from flask import Blueprint, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import time
import psutil

metrics_bp = Blueprint('metrics', __name__)

# Prometheus metrics

# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', [
                        'method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds',
                            'HTTP Request Duration', ['method', 'status', 'path'])
REQUEST_IN_PROGRESS = Gauge(
    'http_requests_in_progress', 'HTTP Requests in progress', ['method', 'path'])

# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes',
                     'Current memory usage in bytes')


@metrics_bp.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).inc()


@metrics_bp.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method,
                         status=response.status_code, path=request.path).inc()
    REQUEST_LATENCY.labels(method=request.method, status=response.status_code,
                           path=request.path).observe(request_latency)
    REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).dec()
    return response


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)


@metrics_bp.route('/')
def metrics():
    update_system_metrics()
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}
