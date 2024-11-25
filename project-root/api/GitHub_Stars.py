from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# GitHub API Base URL
GITHUB_API_URL = "https://api.github.com"

# HTML Templates for the Web Interface
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Stars Tracker</title>
</head>
<body>
    <h1>GitHub Stars Tracker</h1>
    <form action="/github-stats" method="POST">
        <label for="username">GitHub Username:</label>
        <input type="text" id="username" name="username" required>
        <button type="submit">Get Stats</button>
    </form>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

STATS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Stats</title>
</head>
<body>
    <h1>GitHub Stats for {{ user.login }}</h1>
    <p>Name: {{ user.name }}</p>
    <p>Bio: {{ user.bio }}</p>
    <p>Followers: {{ user.followers }}</p>
    <p>Following: {{ user.following }}</p>
    <p>Total Stars: {{ total_stars }}</p>
    <h2>Top Repositories</h2>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Stars</th>
                <th>Forks</th>
            </tr>
        </thead>
        <tbody>
            {% for repo in repositories %}
                <tr>
                    <td>{{ repo.name }}</td>
                    <td>{{ repo.stars }}</td>
                    <td>{{ repo.forks }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

# Route: Web Interface
@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

# Route: Fetch GitHub Stats (API Endpoint)
@app.route('/api/github-stats', methods=['GET'])
def get_github_stats():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Missing 'username' query parameter"}), 400

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return jsonify({"error": "GitHub token not configured"}), 500

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

# Route: Fetch and Display Stats (Web)
@app.route('/github-stats', methods=['POST'])
def display_stats():
    username = request.form.get('username')

    if not username:
        return render_template_string(INDEX_HTML, error="Please provide a GitHub username")

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return render_template_string(INDEX_HTML, error="GitHub token is not configured")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fetch user and repository data
    user_url = f"{GITHUB_API_URL}/users/{username}"
    repos_url = f"{GITHUB_API_URL}/users/{username}/repos"

    try:
        user_response = requests.get(user_url, headers=headers)
        repos_response = requests.get(repos_url, headers=headers, params={"per_page": 100})

        if user_response.status_code != 200 or repos_response.status_code != 200:
            return render_template_string(
                INDEX_HTML,
                error="Failed to fetch data from GitHub"
            )

        user_data = user_response.json()
        repos_data = repos_response.json()

        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        repos_summary = sorted(
            [{"name": repo["name"], "stars": repo["stargazers_count"], "forks": repo["forks_count"]} for repo in repos_data],
            key=lambda x: x["stars"],
            reverse=True
        )

        return render_template_string(
            STATS_HTML,
            user=user_data,
            total_stars=total_stars,
            repositories=repos_summary[:10]
        )

    except requests.exceptions.RequestException as e:
        return render_template_string(INDEX_HTML, error="An error occurred while fetching data", details=str(e))

if __name__ == '__main__':
    app.run(debug=True)
