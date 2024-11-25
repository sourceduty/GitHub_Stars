from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def get_github_stats(owner, repo):
    """Fetch GitHub repository statistics for the given owner and repo."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        stars = data.get('stargazers_count', 'N/A')
        forks = data.get('forks_count', 'N/A')
        return stars, forks
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return None, None

@app.route('/')
def index():
    """Render the homepage with the input form."""
    return render_template('index.html')

@app.route('/stats', methods=['POST'])
def stats():
    """Fetch stats based on user input and render results or error page."""
    owner = request.form['owner'].strip()
    repo = request.form['repo'].strip()
    
    if not owner or not repo:
        return render_template('error.html', message="Owner and repository fields cannot be empty.")

    stars, forks = get_github_stats(owner, repo)
    
    if stars is not None and forks is not None:
        return render_template('result.html', owner=owner, repo=repo, stars=stars, forks=forks)
    else:
        return render_template('error.html', message="Failed to fetch repository statistics.")

if __name__ == '__main__':
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")
