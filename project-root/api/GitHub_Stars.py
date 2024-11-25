from flask import Flask, request, render_template, jsonify, send_from_directory
import requests

app = Flask(__name__)

# GitHub API Base URL
GITHUB_API_URL = "https://api.github.com"

@app.route("/")
def home():
    """
    Render the home page with a form for user input.
    """
    return render_template("index.html", output="Welcome to the GitHub Stars Tracker!")

@app.route("/api/github-stats", methods=["GET"])
def github_stats():
    """
    Fetch repository statistics from the GitHub API.
    """
    repo = request.args.get("repo")
    token = request.args.get("token")

    # Validate the repository input
    if not repo:
        return render_template("error.html", message="Please provide a valid repository name (e.g., owner/repo).")

    # Set up headers for GitHub API requests
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"{GITHUB_API_URL}/repos/{repo}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the response data
        data = response.json()
        contributors = fetch_contributors(repo, headers)

        return render_template(
            "index.html",
            output=f"Repository: {data['full_name']}\n"
                   f"Description: {data.get('description', 'No description available')}\n"
                   f"Stars: {data['stargazers_count']}\n"
                   f"Forks: {data['forks_count']}\n"
                   f"Watchers: {data['watchers_count']}\n"
                   f"Open Issues: {data['open_issues_count']}\n"
                   f"Default Branch: {data['default_branch']}\n"
                   f"Owner: {data['owner']['login']}\n\n"
                   f"Top Contributors: {', '.join(contributors) if contributors else 'No contributors available.'}"
        )
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return render_template("error.html", message=f"Repository '{repo}' not found.")
        else:
            return render_template("error.html", message=f"HTTP error occurred: {http_err}")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit():
    """
    Check GitHub API rate limits.
    """
    token = request.args.get("token")
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"{GITHUB_API_URL}/rate_limit"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()["rate"]

        return jsonify({
            "Limit": data["limit"],
            "Remaining": data["remaining"],
            "Reset": data["reset"]
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

@app.route("/favicon.ico")
def favicon_ico():
    """
    Serve the favicon.ico file.
    """
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/favicon.png")
def favicon_png():
    """
    Serve the favicon.png file.
    """
    return send_from_directory("static", "favicon.png", mimetype="image/png")

def fetch_contributors(repo, headers):
    """
    Fetch the top contributors for a GitHub repository.
    """
    url = f"{GITHUB_API_URL}/repos/{repo}/contributors"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        contributors = [contributor["login"] for contributor in response.json()]
        return contributors[:5]  # Limit to top 5 contributors
    except Exception:
        return None

if __name__ == "__main__":
    app.run(debug=True)
