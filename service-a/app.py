from flask import Flask, jsonify
from datetime import datetime, timezone
import requests
import os

app = Flask(__name__)

CONSUL_URL = os.getenv("CONSUL_URL", "http://localhost:8500")

SERVICE_NAME = "service-a"
SERVICE_ID = os.getenv("SERVICE_ID", SERVICE_NAME)
SERVICE_ADDRESS = os.getenv("SERVICE_ADDRESS", "service-a")
SERVICE_PORT = 5001


def register_with_consul():
    registration = {
        "ID": SERVICE_ID,
        "Name": SERVICE_NAME,
        "Address": SERVICE_ADDRESS,
        "Port": SERVICE_PORT,
        "Check": {
            "HTTP": f"http://{SERVICE_ADDRESS}:{SERVICE_PORT}/health",
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
        "service": "Service A",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Service A"
    })


if __name__ == "__main__":
    register_with_consul()
    app.run(host="0.0.0.0", port=SERVICE_PORT)
