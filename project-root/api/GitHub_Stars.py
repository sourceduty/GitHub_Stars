from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/github-stats", methods=["GET"])
def github_stats():
    repo = request.args.get("repo")
    token = request.args.get("token")

    if not repo:
        return render_template("error.html", message="Please provide a repository name (e.g., owner/repo).")

    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(f"{GITHUB_API_URL}/repos/{repo}", headers=headers)

    if response.status_code == 200:
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
    elif response.status_code == 404:
        return render_template("error.html", message=f"Repository '{repo}' not found.")
    else:
        return render_template("error.html", message=f"Error fetching data. Status Code: {response.status_code}")

@app.route("/api/rate-limit", methods=["GET"])
def rate_limit():
    token = request.args.get("token")
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(f"{GITHUB_API_URL}/rate_limit", headers=headers)

    if response.status_code == 200:
        rate = response.json()["rate"]
        return jsonify({
            "Limit": rate["limit"],
            "Remaining": rate["remaining"],
            "Reset": rate["reset"]
        })
    else:
        return jsonify({"error": f"Error fetching rate limit. Status Code: {response.status_code}"})

def fetch_contributors(repo, headers):
    """
    Fetch contributors for a GitHub repository.
    """
    response = requests.get(f"{GITHUB_API_URL}/repos/{repo}/contributors", headers=headers)
    if response.status_code == 200:
        contributors = [contributor["login"] for contributor in response.json()]
        return contributors[:5]  # Limit to top 5 contributors
    return None

if __name__ == "__main__":
    app.run(debug=True)
