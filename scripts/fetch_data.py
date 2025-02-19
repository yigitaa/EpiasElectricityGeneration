# fetch_generation.py
import requests
import pandas as pd
from datetime import datetime, timedelta

# API endpoint
API_URL = "https://seffaflik.epias.com.tr/electricity-service/v1/generation/data/realtime-generation"

def fetch_real_time_generation(tgt, start_date, end_date):
    """
    Fetch real-time generation data in 3-month intervals using the TGT in a custom header.

    Args:
        tgt (str): The Ticket Granting Ticket (TGT) for authentication.
        start_date (str): Start date in the format "YYYY-MM-DDTHH:MM:SS+03:00".
        end_date (str): End date in the format "YYYY-MM-DDTHH:MM:SS+03:00".

    Returns:
        pd.DataFrame: A DataFrame containing the fetched data.
    """
    # Convert input strings to datetime objects
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    # init
    all_data = []

    # fetch data in 3-month intervals, obligation by epias
    current_start = start_dt
    interval_count = 1
    while current_start < end_dt:
        # Calculate the end date for the current 3-month interval
        current_end = min(current_start + timedelta(days=90), end_dt)

        # print
        print(f"\nFetching interval {interval_count}: {current_start} to {current_end}")

        # Prepare the request payload
        payload = {
            "startDate": current_start.isoformat(),
            "endDate": current_end.isoformat()
        }

        # Set the headers with the TGT in a custom header
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "TGT": tgt  # Include the TGT in a custom header
        }

        try:
            # Make a POST request to the API
            print("Making request to the API...")
            response = requests.post(API_URL, json=payload, headers=headers, timeout=90)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the JSON response
            data = response.json()

            # Check if the response contains the expected data
            if isinstance(data, dict) and "items" in data:  # Adjust "items" based on the actual key
                items = data["items"]  # Extract the nested data
                all_data.extend(items)
                print(f"Fetched {len(items)} records.")
            else:
                print("No data found for this interval.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            print(f"Response content: {response.content}")  # Print the response content for debugging
            # Continue to the next interval instead of breaking
            current_start = current_end
            interval_count += 1
            continue

        # Move to the next 3-month interval
        current_start = current_end
        interval_count += 1

    # Convert the list of data to a DataFrame
    df = pd.DataFrame(all_data)
    return df