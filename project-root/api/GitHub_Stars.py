from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# HTML Template with a text box area for output
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
        <input type="text" id="repo" name="repo" placeholder="e.g., tensorflow/tensorflow"><br><br>
        <button type="submit">Fetch Stats</button>
    </form>
    <br>
    <textarea id="output" rows="10" cols="50" readonly>{{ output }}</textarea>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    """
    Render the home page with an input form and output area.
    """
    return render_template_string(HTML_TEMPLATE, output="")

@app.route("/api/github-stats", methods=["GET"])
def github_stats():
    """
    Fetch GitHub repository stats and display them.
    """
    repo = request.args.get("repo", None)
    if not repo:
        return render_template_string(
            HTML_TEMPLATE,
            output="Please provide a valid GitHub repository name (e.g., owner/repo)."
        )

    # Simulate fetching GitHub stats (replace with actual API call if needed)
    stats = {
        "repository": repo,
        "stars": 1500,  # Simulated data
        "forks": 300,   # Simulated data
    }

    output = f"Repository: {stats['repository']}\nStars: {stats['stars']}\nForks: {stats['forks']}"
    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(debug=True)
