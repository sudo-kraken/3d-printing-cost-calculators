import os

from flask import Flask, jsonify, render_template, request

from .config import apply_profit_default
from .fdm_calculator import calculate_fdm_cost
from .resin_calculator import calculate_resin_cost

app = Flask(__name__)

# Branding and server options
app.config["BRAND_NAME"] = os.getenv("APP_BRAND_NAME", "3D Print Calculators")
app.config["LOGO_URL"] = os.getenv("APP_LOGO_URL", "/static/logo.png")
app.config["FAVICON_URL"] = os.getenv("APP_FAVICON_URL", "/static/favicon.ico")
PORT = int(os.getenv("PORT", "6969"))
HOST = os.getenv("HOST", "0.0.0.0")


@app.context_processor
def inject_branding():
    return {
        "brand_name": app.config["BRAND_NAME"],
        "logo_url": app.config["LOGO_URL"],
        "favicon_url": app.config["FAVICON_URL"],
    }


@app.get("/health")
def health():
    return jsonify({"ok": True}), 200


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/resin-calculator")
def resin_calculator():
    return render_template("resin_calculator.html")


@app.route("/resin-simple")
def resin_simple():
    return render_template("resin_simple.html")


@app.route("/fdm-calculator")
def fdm_calculator():
    return render_template("fdm_calculator.html")


@app.route("/fdm-simple")
def fdm_simple():
    return render_template("fdm_simple.html")


@app.route("/calculate-resin", methods=["POST"])
def calculate_resin():
    try:
        payload = request.json or {}
        inputs = apply_profit_default(payload)
        result = calculate_resin_cost(inputs)
        return jsonify({"success": True, "inputs_used": inputs, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/calculate-fdm", methods=["POST"])
def calculate_fdm():
    try:
        payload = request.json or {}
        inputs = apply_profit_default(payload)
        result = calculate_fdm_cost(inputs)
        return jsonify({"success": True, "inputs_used": inputs, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
