from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

CONSUL_URL = os.getenv("CONSUL_URL", "http://localhost:8500")
GATEWAY_PORT = 8080


def discover_service(service_name):
    url = f"{CONSUL_URL}/v1/health/service/{service_name}"

    response = requests.get(
        url,
        params={"passing": "true"},
        timeout=5
    )

    response.raise_for_status()

    services = response.json()

    if not services:
        raise Exception(f"No healthy instances found for {service_name}")

    service = services[0]["Service"]

    address = service["Address"]
    port = service["Port"]

    return address, port


@app.route("/service-a/info")
def service_a_info():
    return forward_to_service("service-a")


@app.route("/service-b/info")
def service_b_info():
    return forward_to_service("service-b")


@app.route("/service-c/info")
def service_c_info():
    return forward_to_service("service-c")


def forward_to_service(service_name):
    try:
        address, port = discover_service(service_name)

        service_url = f"http://{address}:{port}/info"

        response = requests.get(
            service_url,
            timeout=5
        )

        return (
            jsonify(response.json()),
            response.status_code
        )

    except Exception as e:
        return jsonify({
            "error": str(e),
            "service": service_name
        }), 503


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "API Gateway"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=GATEWAY_PORT
    )
