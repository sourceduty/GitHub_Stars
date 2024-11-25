from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"

# HTML Template with enhanced UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Stars Tracker</title>
</head>
<body>
    <h1>GitHub Stars Tracker</h1>
    <form method="GET" action="/api/github-stats">
        <label for="repo">Enter GitHub Repository (e.g., owner/repo):</label><br><br>
        <input type="text" id="repo" name="repo" placeholder="e.g., tensorflow/tensorflow" required><br><br>
        <label for="token">Enter Personal Access Token (optional):</label><br><br>
        <input type="text" id="token" name="token" placeholder="GitHub Personal Access Token"><br><br>
        <button type="submit">Fetch Stats</button>
    </form>
    <br>
    <textarea id="output" rows="15" cols="80" readonly>{{ output }}</textarea>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE, output="Welcome! Enter a repository to get started.")

@app.route("/api/github-stats", methods=["GET"])
def github_stats():
    repo = request.args.get("repo", None)
    token = request.args.get("token", None)

    if not repo:
        return render_template_string(HTML_TEMPLATE, output="Error: Repository name is required.")

    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API_URL}/repos/{repo}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        output = (
            f"Repository: {data['full_name']}\n"
            f"Description: {data.get('description', 'No description available')}\n"
            f"Stars: {data['stargazers_count']}\n"
            f"Forks: {data['forks_count']}\n"
            f"Watchers: {data['watchers_count']}\n"
            f"Open Issues: {data['open_issues_count']}\n"
            f"Default Branch: {data['default_branch']}\n"
            f"Owner: {data['owner']['login']}\n"
        )
    elif response.status_code == 404:
        output = f"Error: Repository '{repo}' not found."
    elif response.status_code == 403:
        output = "Error: Rate limit exceeded. Please provide a valid GitHub token."
    else:
        output = f"Error: Unable to fetch data. Status Code: {response.status_code}"

    return render_template_string(HTML_TEMPLATE, output=output)

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit():
    token = request.args.get("token", None)
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API_URL}/rate_limit"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        rate = data['rate']
        output = (
            f"Rate Limit:\n"
            f"Limit: {rate['limit']}\n"
            f"Remaining: {rate['remaining']}\n"
            f"Reset: {rate['reset']}\n"
        )
    else:
        output = f"Error: Unable to fetch rate limit. Status Code: {response.status_code}"

    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(debug=True)
