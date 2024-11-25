from flask import Flask, request, jsonify
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# GitHub API Base URL
GITHUB_API_URL = "https://api.github.com"

# Get GitHub Token from Environment Variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("Missing GITHUB_TOKEN environment variable")


@app.route('/api/github-stats', methods=['GET'])
def github_stats():
    # Get the username from the query parameters
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username query parameter is required"}), 400

    # Headers for GitHub API authentication
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Fetch user data from GitHub API
        user_response = requests.get(f"{GITHUB_API_URL}/users/{username}", headers=headers)
        if user_response.status_code != 200:
            return jsonify({"error": "Failed to fetch user data", "details": user_response.json()}), user_response.status_code

        user_data = user_response.json()

        # Fetch user's public repositories
        repos_response = requests.get(f"{GITHUB_API_URL}/users/{username}/repos", headers=headers)
        if repos_response.status_code != 200:
            return jsonify({"error": "Failed to fetch repositories", "details": repos_response.json()}), repos_response.status_code

        repos_data = repos_response.json()

        # Calculate total stars and prepare detailed repository stats
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        repositories = [{"name": repo["name"], "stars": repo.get("stargazers_count", 0), "forks": repo.get("forks_count", 0)} for repo in repos_data]

        # Fetch user's recent activity
        events_response = requests.get(f"{GITHUB_API_URL}/users/{username}/events", headers=headers)
        if events_response.status_code != 200:
            return jsonify({"error": "Failed to fetch recent contributions", "details": events_response.json()}), events_response.status_code

        events_data = events_response.json()
        recent_contributions = [{"type": event.get("type"), "created_at": event.get("created_at")} for event in events_data[:5]]

        # Prepare and return final response
        return jsonify({
            "user": {
                "login": user_data.get("login"),
                "name": user_data.get("name"),
                "bio": user_data.get("bio"),
                "followers": user_data.get("followers"),
                "following": user_data.get("following"),
                "public_repos": user_data.get("public_repos")
            },
            "repositories": repositories,
            "total_stars": total_stars,
            "recent_contributions": recent_contributions
        })

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


if __name__ == '__main__':
    # Run the Flask app for local testing
    app.run(debug=True)
