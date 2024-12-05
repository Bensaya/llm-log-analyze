import requests


def query_logs(query_text):
    """Sends a query to the FastAPI server.
    Args:
    query_text: The query string.
    Returns:
    The server's response as a string, or None if an error occurred.
    """
    url = f"http://127.0.0.1:8000/query_logs/{query_text}" # Adjust URL and port as needed
    try:
        response = requests.post(url)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.text # or response.json() if you expect JSON
    except requests.exceptions.RequestException as e:
        print(f"Error querying server: {e}")
        return None
# Example usage:
query = "create report for all the failed builds in jenkins-agent-linux ONLY"
response = query_logs(query)
if response:
    print(response)