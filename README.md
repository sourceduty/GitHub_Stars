![GitHub_Stars_Banner](https://github.com/user-attachments/assets/6e20d313-5d42-48b2-ad03-31c29acf9e49)

> API to fetch GitHub user statistics and stars, deployed using Vercel. Experimental development.
#

This program, GitHub Stars, is designed to provide an intuitive interface for fetching and displaying repository statistics from GitHub. Users can input a repository name (in the format owner/repo) and retrieve simulated stats such as stars and forks, which are presented in a clear text box. The program is built using Flask, a lightweight Python web framework, and includes both an API endpoint and a user-friendly HTML form to facilitate interaction. The /api/github-stats route serves as the core API endpoint, while the home route (/) renders an input form with a text area for displaying output. The application also includes a /status endpoint, making it easy to check if the program is running.

The design emphasizes simplicity and ease of use, with features like dynamic output rendering and a clear separation of routes for specific tasks. However, the stats fetching logic is currently simulated and needs to be connected to the GitHub API for real-time data. The HTML interface is a starting point for more advanced user interaction, such as sorting, filtering, or visualizing stats in charts. This foundational program showcases modularity and adaptability, paving the way for further enhancements.

#
### Partial Development

![Vercel](https://github.com/user-attachments/assets/d51592ca-5a0e-4d0f-939c-cc87c5c1d120)

The development process on Vercel leverages its serverless infrastructure, which simplifies deployment but requires specific configurations to support Python applications like this one. During partial development, challenges such as compatibility between Flask and Vercel's serverless functions arose. The program needs refinements to align with Vercel's environment, including routing fixes and dependency adjustments. To achieve full functionality, integration with GitHub's REST API or GraphQL API is required, allowing users to fetch actual data. Expanding the program could include adding authentication for private repositories, handling rate limits, and improving the UI with real-time updates. These improvements will transform the program into a robust tool for GitHub repository analysis.

#
### Vercel

![vercel](https://github.com/user-attachments/assets/67cd9d57-cead-4d74-b3dc-b9c23a29650f)

Vercel is a cloud platform for static sites and Serverless Functions, which integrates seamlessly with GitHub to provide a streamlined workflow for deploying web applications. By linking a GitHub repository to a Vercel project, developers can easily deploy their applications every time they push code changes to the repository. For example, once a GitHub repository is connected, Vercel automatically detects changes and builds the project, making it accessible via a live URL. The integration is designed to be intuitive, allowing for fast deployments with minimal configuration. After linking your GitHub account, you simply select the repository to deploy, and Vercel takes care of the rest.

For instance, to deploy a simple React app on Vercel using GitHub, you would first push your project to a GitHub repository. Then, on the Vercel dashboard, you connect the repository by clicking the "New Project" button and selecting the repository you want to deploy. Vercel automatically detects the build settings for common frameworks like React or Next.js, and in a few minutes, your app is live. For more advanced use cases, you can configure Vercel's deployment settings through a vercel.json file in your repository, allowing you to specify routes, serverless functions, and environmental variables to control the deployment process further.

#

```
project-root/
├── api/
│   ├── __init__.py
│   ├── GitHub_Stars.py
├── static/
│   ├── favicon.ico
│   ├── favicon.png
├── templates/
│   ├── index.html
│   ├── error.html
├── wsgi.py
├── vercel.json
├── runtime.txt
├── requirements.txt
── README.md
```

#
### Features

1. Home Page:

- Displays a welcome message and a form for users to enter a GitHub repository name and an optional API token.

2. Fetch GitHub Repository Stats:

- Endpoint: `/api/github_stars`
- Fetches details about a GitHub repository:
 - Repository name and description.
 - Star count, fork count, watcher count.
 - Open issues count, default branch, and owner name.
 - Top 5 contributors.

3. Rate Limit Check:

- Endpoint: `/api/rate-limit`
- Displays the GitHub API rate limits:
 - Total limit, remaining calls, and reset time.

4. Error Handling:

- Provides clear error messages for:
 - Invalid or missing repository names.
 - Unauthorized requests (e.g., invalid or missing token).
 - Non-existent repositories (404 error).
 - HTTP and connection errors.

5. Static File Serving:

- Handles requests for `/favicon.ico` and `/favicon.png`.
- Serves favicon files to prevent unnecessary error logs in browsers.

6. Contributor Information:

- Fetches the top 5 contributors for a repository using the GitHub API.

7. Token Authentication Support:

- Optional GitHub token for authenticated requests to:
 - Bypass API rate limits.
 - Access private repositories.

8. API Integration:

- Uses the GitHub API (`https://api.github.com`) for all repository and contributor data.

9. Dynamic Web Pages:

- `index.html`: Displays fetched repository stats.
- `error.html`: Shows detailed error messages for failed requests.

10. Compatibility:

- Fully deployable to Vercel using `wsgi.py` and `vercel.json`.
- Local testing support with Flask's built-in server.

#
![vercel_login](https://github.com/user-attachments/assets/74173269-e916-4509-9b64-95a1b5baf4d5)
#
![Stars](https://github.com/user-attachments/assets/1838073c-0a81-4b76-83c5-d1572057b51b)

#
### Related Links

[GitHub](https://github.com/sourceduty/GitHub)

#
![Active Development](https://github.com/user-attachments/assets/8c7cee43-3c51-4741-a101-c3bbb9ae21a7)

***
Copyright (C) 2024, Sourceduty - All Rights Reserved.
