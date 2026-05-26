from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# ── Métricas ──────────────────────────────────────────────
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total de requests HTTP',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Latencia de requests en segundos',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Usuarios activos simulados'
)

@app.route('/api/products')
def products():
    start = time.time()
    time.sleep(random.uniform(0.01, 0.3))          # latencia simulada
    
    REQUEST_COUNT.labels('GET', '/api/products', '200').inc()
    REQUEST_LATENCY.labels('/api/products').observe(time.time() - start)
    
    return jsonify({"products": ["laptop", "mouse", "teclado"], "count": 3})

@app.route('/api/orders', methods=['GET'])
def orders():
    start = time.time()
    time.sleep(random.uniform(0.05, 0.5))
    
    # Simula errores 20% del tiempo
    if random.random() < 0.2:
        REQUEST_COUNT.labels('GET', '/api/orders', '500').inc()
        REQUEST_LATENCY.labels('/api/orders').observe(time.time() - start)
        return jsonify({"error": "DB timeout"}), 500
    
    REQUEST_COUNT.labels('GET', '/api/orders', '200').inc()
    REQUEST_LATENCY.labels('/api/orders').observe(time.time() - start)
    return jsonify({"orders": [1, 2, 3], "total": 3})

@app.route('/api/users')
def users():
    start = time.time()
    users_count = random.randint(10, 100)
    ACTIVE_USERS.set(users_count)
    
    REQUEST_COUNT.labels('GET', '/api/users', '200').inc()
    REQUEST_LATENCY.labels('/api/users').observe(time.time() - start)
    return jsonify({"active_users": users_count})

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
