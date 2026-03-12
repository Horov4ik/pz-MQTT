from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Prometheus metrics (auto-exposes /metrics)
metrics = PrometheusMetrics(app)


@app.get('/')
def index():
    return jsonify({"service": "web2", "status": "ok"})


@app.get('/health')
def health():
    return jsonify({"service": "web2", "status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
