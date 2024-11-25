![GitHub_Stars_Banner](https://github.com/user-attachments/assets/6e20d313-5d42-48b2-ad03-31c29acf9e49)

> API to fetch GitHub user statistics, deployed using Vercel. Experimental development.
#

This program, GitHub Stars Tracker, is designed to provide an intuitive interface for fetching and displaying repository statistics from GitHub. Users can input a repository name (in the format owner/repo) and retrieve simulated stats such as stars and forks, which are presented in a clear text box. The program is built using Flask, a lightweight Python web framework, and includes both an API endpoint and a user-friendly HTML form to facilitate interaction. The /api/github-stats route serves as the core API endpoint, while the home route (/) renders an input form with a text area for displaying output. The application also includes a /status endpoint, making it easy to check if the program is running.

The design emphasizes simplicity and ease of use, with features like dynamic output rendering and a clear separation of routes for specific tasks. However, the stats fetching logic is currently simulated and needs to be connected to the GitHub API for real-time data. The HTML interface is a starting point for more advanced user interaction, such as sorting, filtering, or visualizing stats in charts. This foundational program showcases modularity and adaptability, paving the way for further enhancements.

#
### Partial Development

![Vercel](https://github.com/user-attachments/assets/4d57db81-dd39-4e41-b2c9-3ae52f63ff60)

The development process on Vercel leverages its serverless infrastructure, which simplifies deployment but requires specific configurations to support Python applications like this one. During partial development, challenges such as compatibility between Flask and Vercel's serverless functions arose. The program needs refinements to align with Vercel's environment, including routing fixes and dependency adjustments. To achieve full functionality, integration with GitHub's REST API or GraphQL API is required, allowing users to fetch actual data. Expanding the program could include adding authentication for private repositories, handling rate limits, and improving the UI with real-time updates. These improvements will transform the program into a robust tool for GitHub repository analysis.

#

```
project-root/
├── api/
│   └── GitHub_Stars.py
├── vercel.json
└── requirements.txt
── README.md
```

#
### Features

This application provides an API to fetch GitHub user statistics, deployed using Vercel.

- Fetches user profile data from GitHub.
- Lists repositories sorted by stars.
- Displays recent public contributions.

#
### Requirements

Python 3.8+ Flask Requests Vercel account

#
### Setup Instructions

```
Clone the repository: git clone https://github.com/your-username/github-stats-app.git

Navigate to the project directory: cd github-stats-app

Install dependencies: pip install -r requirements.txt

Set up a .env file in the env/ directory with your GitHub token: GITHUB_TOKEN=your_github_personal_access_token
```

#
### API Endpoints

GET /api/github-stats: Fetches GitHub user data. 

Query Parameters: username (required): GitHub username to fetch data for.

Response Format: JSON object with user profile, repositories, and contributions.

#
### Related Links

[GitHub](https://github.com/sourceduty/GitHub)

***
Copyright (C) 2024, Sourceduty - All Rights Reserved.
