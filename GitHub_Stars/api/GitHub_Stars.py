import os
import json
import requests
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# GitHub API URL
GITHUB_API_URL = 'https://api.github.com'

# Load GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Function to get user data
def get_user_data(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Function to get user repositories
def get_user_repositories(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    all_repos = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        if response.status_code == 200:
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            page += 1
        else:
            return {"error": response.status_code, "message": response.text}
    
    sorted_repos = sorted(all_repos, key=lambda repo: repo['stargazers_count'], reverse=True)
    return sorted_repos

# Function to get user contributions
def get_user_contributions(username):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API_URL}/users/{username}/events/public'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# API endpoint to fetch user statistics
@app.route('/api/github-stats', methods=['GET'])
def github_stats():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    user_data = get_user_data(username)
    if "error" in user_data:
        return jsonify(user_data), user_data["error"]

    repositories = get_user_repositories(username)
    if isinstance(repositories, dict) and "error" in repositories:
        return jsonify(repositories), repositories["error"]

    contributions = get_user_contributions(username)
    if isinstance(contributions, dict) and "error" in contributions:
        return jsonify(contributions), contributions["error"]
    
    report = {
        "user": {
            "login": user_data.get("login"),
            "name": user_data.get("name"),
            "bio": user_data.get("bio"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following")
        },
        "repositories": [
            {"name": repo["name"], "stars": repo["stargazers_count"], "forks": repo["forks_count"]}
            for repo in repositories
        ],
        "recent_contributions": [
            {"type": event["type"], "created_at": event["created_at"]}
            for event in contributions[:5]
        ]
    }
    return jsonify(report)

# Vercel requires a main handler
def handler(request, context=None):
    return app(request, context)
