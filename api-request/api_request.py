import requests
import os

# Get values from environment, with a fallback for local testing
API_KEY = os.getenv("EARTHQUAKE_API_KEY")
BASE_URL = os.getenv("EARTHQUAKE_API_URL", "https://earthquake.usgs.gov/fdsnws/event/1/query")

def fetch_data():
    # Construct params safely
    params = {
        "format": "csv",
        "starttime": "2014-01-01",
        "endtime": "2014-01-02",
        "key": API_KEY  # This will be None if not set, or the real key if set
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        raise