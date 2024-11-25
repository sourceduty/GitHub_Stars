from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def get_user_data(username):
    """Fetch GitHub user data."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

def get_repositories(username):
    """Fetch repositories of the GitHub user."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    response = requests.get(url, headers=headers)
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
        return {"error": response.status_code, "message": response.text}

def get_recent_contributions(username):
    """Fetch recent contributions of the GitHub user."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/events'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()
        return [
            {"type": event["type"], "created_at": event["created_at"]}
            for event in events if event["type"] == "PushEvent"
        ]
    else:
        return {"error": response.status_code, "message": response.text}

@app.route('/api/github-stats', methods=['GET'])
def github_stats():
    """API endpoint to fetch GitHub stats."""
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
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
    
    return jsonify(response)

# Vercel compatibility
def handler(event, context):
    """Vercel handler for AWS Lambda compatibility."""
    return app(event, context)
