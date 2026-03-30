from flask import Flask, jsonify, render_template
from prometheus_flask_exporter import PrometheusMetrics
import paho.mqtt.client as mqtt
from prometheus_client import Gauge
import threading
import time

app = Flask(__name__)

# Prometheus metrics (auto-exposes /metrics)
metrics = PrometheusMetrics(app)

# MQTT availability gauge
mqtt_available = Gauge('mqtt_broker_available', 'MQTT broker availability (1=up, 0=down)')


def check_mqtt():
    """Background thread that periodically checks MQTT broker connectivity."""
    while True:
        try:
            client = mqtt.Client()
            client.connect("mosquitto", 1883, keepalive=5)
            client.disconnect()
            mqtt_available.set(1)
        except Exception:
            mqtt_available.set(0)
        time.sleep(10)


threading.Thread(target=check_mqtt, daemon=True).start()


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/health')
def health():
    return jsonify({"service": "web1", "status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
