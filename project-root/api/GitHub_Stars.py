import json

def handler(event, context):
    """
    Vercel-compatible handler function to process HTTP requests.
    """

    # Parse the incoming request (Vercel provides an event object)
    try:
        # Extracting the path and query string
        path = event.get("path", "")
        query = event.get("queryStringParameters", {})

        # Route logic
        if path == "/api/github-stats":
            response = {
                "message": "Welcome to the GitHub Stars Tracker!",
                "instructions": "Use this API to fetch and display GitHub repository stats."
            }
        else:
            response = {
                "error": "Route not found. Please use '/api/github-stats'."
            }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
