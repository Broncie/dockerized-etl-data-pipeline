import requests
import csv

api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2014-01-01&endtime=2014-01-02"

def fetch_data():
    print("Fetching data from Earthquake API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("Data fetched successfully")
        print(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise
