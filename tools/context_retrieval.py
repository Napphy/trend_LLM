import json
import requests
import os
from dotenv import load_dotenv
from transformers import tool
from typing import Any

load_dotenv()

scan_api_key = os.getenv("SCAN_API_KEY")
scan_url = os.getenv("SCAN_URL")

@tool
def retrieve_scan_result(hash: str) -> str:
    """
    A tool for retrieving scan results from the Grid Scanner API.

    This function fetches scan results for a given hash from the Grid Scanner API.

    Args:
        hash: The hash value of the scan result to retrieve.
        scan_api_key: The API key required for authentication with the Grid Scanner API.

    Returns:
        str: The scan result as a JSON string or an error message.
    """
    url = f"{scan_url}{hash}"
    headers = {"X-API-KEY": scan_api_key}
    response = requests.get(url, headers=headers)
    
    # Handle response based on status code
    if response.status_code == 200:
        return json.dumps(response.json(), indent=2)  # Successful response
    elif response.status_code == 400:
        return "Invalid request parameters. Please check the input data."
    elif response.status_code == 401:
        return "API key is missing or invalid. Please verify the API key."
    elif response.status_code == 422:
        return "Validation error occurred. Please check the request data."
    elif response.status_code == 500:
        return "Internal server error. Please try again later."
    else:
        return f"Unexpected error occurred. Status code: {response.status_code}"
