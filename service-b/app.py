from flask import Flask, jsonify
from datetime import datetime, timezone
import requests
import os

app = Flask(__name__)

CONSUL_URL = os.getenv("CONSUL_URL", "http://localhost:8500")

SERVICE_NAME = "service-b"
SERVICE_PORT = 5002


def register_with_consul():
    registration = {
        "ID": SERVICE_NAME,
        "Name": SERVICE_NAME,
        "Address": "service-b",
        "Port": SERVICE_PORT,
        "Check": {
            "HTTP": f"http://service-b:{SERVICE_PORT}/health",
            "Interval": "10s",
            "Timeout": "5s"
        }
    }

    response = requests.put(
        f"{CONSUL_URL}/v1/agent/service/register",
        json=registration
    )

    response.raise_for_status()
    print(f"{SERVICE_NAME} registered with Consul")


@app.route("/info")
def info():
    return jsonify({
        "service": "Service B",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Service B"
    })


if __name__ == "__main__":
    register_with_consul()
    app.run(host="0.0.0.0", port=SERVICE_PORT)
