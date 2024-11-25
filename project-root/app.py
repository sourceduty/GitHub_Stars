from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

def get_github_stats(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        stars = data.get('stargazers_count', 'N/A')
        forks = data.get('forks_count', 'N/A')
        return stars, forks
    else:
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats', methods=['POST'])
def stats():
    owner = request.form['owner']
    repo = request.form['repo']
    
    stars, forks = get_github_stats(owner, repo)
    
    if stars is not None and forks is not None:
        return render_template('result.html', owner=owner, repo=repo, stars=stars, forks=forks)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
