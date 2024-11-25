from flask import Flask, request, jsonify
import requests
import os
import logging
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def make_request(url, headers):
    """Make a GET request to GitHub API with rate limit handling."""
    logging.debug(f"Making request to: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        current_time = int(time.time())
        wait_time = reset_time - current_time
        if wait_time > 0:
            logging.error(f"Rate limit exceeded. Retry after {wait_time} seconds.")
            return {"error": "Rate limit exceeded. Retry after some time."}
    return response

def get_user_data(username):
    """Fetch GitHub user data."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}'
    response = make_request(url, headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to fetch user data for {username}: {response.text}")
        return {"error": response.status_code, "message": response.text}

def get_repositories(username):
    """Fetch repositories of the GitHub user."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    response = make_request(url, headers)
    if response.status_code == 200:
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
        logging.error(f"Failed to fetch repositories for {username}: {response.text}")
        return {"error": response.status_code, "message": response.text}

def get_recent_contributions(username):
    """Fetch recent contributions of the GitHub user."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/events'
    response = make_request(url, headers)
    if response.status_code == 200:
        events = response.json()
        return [
            {"type": event["type"], "created_at": event["created_at"]}
            for event in events if event["type"] == "PushEvent"
        ]
    else:
        logging.error(f"Failed to fetch recent contributions for {username}: {response.text}")
        return {"error": response.status_code, "message": response.text}

@app.route('/api/github-stats', methods=['GET'])
def github_stats():
    """API endpoint to fetch GitHub stats."""
    logging.debug("Request received at /api/github-stats")
    username = request.args.get('username')
    if not username:
        logging.error("Username not provided in request")
        return jsonify({"error": "Username is required"}), 400

    logging.debug(f"Fetching data for username: {username}")
    user_data = get_user_data(username)
    if "error" in user_data:
        return jsonify({"error": "Failed to fetch user data", "details": user_data}), 400

    repositories = get_repositories(username)
    if isinstance(repositories, dict) and "error" in repositories:
        return jsonify({"error": "Failed to fetch repositories", "details": repositories}), 400

    recent_contributions = get_recent_contributions(username)
    if isinstance(recent_contributions, dict) and "error" in recent_contributions:
        return jsonify({"error": "Failed to fetch recent contributions", "details": recent_contributions}), 400

    response = {
        "user": user_data,
        "repositories": repositories,
        "recent_contributions": recent_contributions,
        "total_stars": sum(repo.get("stars", 0) for repo in repositories)
    }

    logging.debug(f"Response prepared: {response}")
    return jsonify(response)

# Vercel compatibility
def handler(event, context):
    """Vercel handler for AWS Lambda compatibility."""
    return app(event, context)
