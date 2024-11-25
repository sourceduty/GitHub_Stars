from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/github-stats', methods=['GET'])
def github_stats():
    """
    Endpoint to fetch GitHub stats.
    """
    return jsonify({
        "message": "Welcome to the GitHub Stars Tracker!",
        "instructions": "Use this API to fetch and display GitHub repository stats."
    })

@app.route('/', methods=['GET'])
def home():
    """
    A default home route to verify the app is running.
    """
    return jsonify({
        "message": "This is the home route of the GitHub Stars Tracker API.",
        "available_routes": ["/api/github-stats"]
    })

if __name__ == "__main__":
    app.run(debug=True)
