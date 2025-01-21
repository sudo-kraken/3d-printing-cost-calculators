from flask import Flask, render_template, request, jsonify
from resin_calculator import calculate_resin_cost
from fdm_calculator import calculate_fdm_cost

app = Flask(__name__)

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
        data = request.json
        result = calculate_resin_cost(data)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/calculate-fdm", methods=["POST"])
def calculate_fdm():
    try:
        data = request.json
        result = calculate_fdm_cost(data)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969)
