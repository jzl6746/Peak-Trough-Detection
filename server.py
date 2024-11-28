from flask import Flask, jsonify, request
from backend.peak_trough_dectector import PeakTroughDetector

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    """
    Flask route to analyze stock data.
    """
    data = request.get_json()
    response, status_code = PeakTroughDetector.analyze_stock(data)
    return jsonify(response), status_code


def run_flask():
    """
    Run the Flask server.
    """
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    run_flask()
