import requests
import pandas as pd
from datetime import datetime

def extract_data():
    print("Extracting live data from public API...")
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status: {response.status_code}")

def run_pipeline():
    raw_json = extract_data()
    
    extracted_records = []
    for launch in raw_json:
        extracted_records.append({
            'flight_number': launch.get('flight_number'),
            'mission_name': launch.get('name'),
            'date_utc': launch.get('date_utc')[:10],
            'rocket_id': launch.get('rocket'),
            'success': launch.get('success')
        })
    df = pd.DataFrame(extracted_records)
    
    # Save directly as a clean CSV file instead of a local database binary
    df.to_csv('spacex_launches.csv', index=False)
    print("Successfully updated spacex_launches.csv!")

if __name__ == "__main__":
    run_pipeline()