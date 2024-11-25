from flask import Flask, request, jsonify
import requests
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Fetch token from environment variable

# Check if token exists at startup
if not GITHUB_TOKEN:
    logging.error("GITHUB_TOKEN is not set in the environment variables!")

@app.route('/api/github-stats', methods=['GET'])
def github_stats():
    """API endpoint to fetch GitHub stats."""
    logging.debug("Received request at /api/github-stats")

    # Fetch username from request
    username = request.args.get('username')
    if not username:
        logging.error("No username provided in the request")
        return jsonify({"error": "Username is required"}), 400

    # Fetch user data
    user_data = get_user_data(username)
    if "error" in user_data:
        return jsonify({"error": "Failed to fetch user data", "details": user_data}), 400

    # Fetch repositories
    repositories = get_repositories(username)
    if isinstance(repositories, dict) and "error" in repositories:
        return jsonify({"error": "Failed to fetch repositories", "details": repositories}), 400

    # Prepare response
    response = {
        "user": user_data,
        "repositories": repositories,
        "total_stars": sum(repo.get("stars", 0) for repo in repositories)
    }

    logging.debug(f"Response prepared: {response}")
    return jsonify(response)

def get_user_data(username):
    """Fetch GitHub user data."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}'
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logging.error("Unauthorized access: Check your GITHUB_TOKEN")
        return {"error": 401, "message": "Unauthorized access. Check your GITHUB_TOKEN."}
    elif response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching user data: {response.status_code} - {response.text}")
        return {"error": response.status_code, "message": response.text}

def get_repositories(username):
    """Fetch GitHub repositories."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        logging.error("Unauthorized access: Check your GITHUB_TOKEN")
        return {"error": 401, "message": "Unauthorized access. Check your GITHUB_TOKEN."}
    elif response.status_code == 200:
        repos = response.json()
        return [
            {
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"]
            }
            for repo in repos
        ]
    else:
        logging.error(f"Error fetching repositories: {response.status_code} - {response.text}")
        return {"error": response.status_code, "message": response.text}

# Local testing endpoint to verify token
@app.route('/api/check-token', methods=['GET'])
def check_token():
    """Endpoint to validate GitHub token."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/user'
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        return jsonify({"error": "Invalid or missing GITHUB_TOKEN"}), 401
    elif response.status_code == 200:
        return jsonify({"message": "Token is valid", "user": response.json()}), 200
    else:
        return jsonify({"error": response.status_code, "message": response.text}), 400

if __name__ == "__main__":
    app.run(debug=True)
