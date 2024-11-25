from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# GitHub API Base URL
GITHUB_API_URL = "https://api.github.com"

@app.route('/api/github-stats', methods=['GET'])
def get_github_stats():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Missing 'username' query parameter"}), 400

    # Get the GitHub token from environment variables
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return jsonify({"error": "GitHub token not configured"}), 500

    # Headers for GitHub API request
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Fetch user data
        user_response = requests.get(f"{GITHUB_API_URL}/users/{username}", headers=headers)
        if user_response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch user data",
                "details": user_response.json()
            }), user_response.status_code

        user_data = user_response.json()

        # Fetch repositories
        repos_response = requests.get(f"{GITHUB_API_URL}/users/{username}/repos", headers=headers, params={"per_page": 100})
        if repos_response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch repositories",
                "details": repos_response.json()
            }), repos_response.status_code

        repos_data = repos_response.json()

        # Summarize repository stats
        repos_summary = []
        total_stars = 0
        for repo in repos_data:
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            repos_summary.append({
                "name": repo.get("name"),
                "stars": stars,
                "forks": forks
            })
            total_stars += stars

        # Sort repositories by stars
        repos_summary = sorted(repos_summary, key=lambda x: x["stars"], reverse=True)

        return jsonify({
            "user": {
                "login": user_data.get("login"),
                "name": user_data.get("name"),
                "bio": user_data.get("bio"),
                "followers": user_data.get("followers"),
                "following": user_data.get("following"),
                "public_repos": user_data.get("public_repos")
            },
            "total_stars": total_stars,
            "repositories": repos_summary[:10]  # Limit to top 10 repositories
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An error occurred while fetching data", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
