import requests
import pandas as pd
import duckdb
from datetime import datetime

# 1. EXTRACT: Fetch completely free, public data (SpaceX Launch Data)
def extract_data():
    print("Extracting live data from public API...")
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status: {response.status_code}")

# 2. TRANSFORM & LOAD: Clean it up using Python and SQL inside DuckDB
def run_pipeline():
    # Get raw data
    raw_json = extract_data()
    
    # Standardize it into a DataFrame
    extracted_records = []
    for launch in raw_json:
        extracted_records.append({
            'flight_number': launch.get('flight_number'),
            'mission_name': launch.get('name'),
            'date_utc': launch.get('date_utc')[:10], # Keep just the YYYY-MM-DD
            'rocket_id': launch.get('rocket'),
            'success': launch.get('success')
        })
    df = pd.DataFrame(extracted_records)
    
    # Connect to DuckDB (This automatically creates a local database file called 'analytics.duckdb')
    con = duckdb.connect('analytics.duckdb')
    
    # Register the DataFrame as a view so we can run SQL on it
    con.register('raw_launches', df)
    
    print("Running SQL transformations inside DuckDB...")
    # Write SQL to create a clean, aggregated summary table
    con.execute("""
        CREATE OR REPLACE TABLE daily_summary AS
        SELECT 
            date_utc AS launch_date,
            COUNT(*) AS total_launches,
            COUNT(CASE WHEN success = true THEN 1 END) AS successful_launches
        FROM raw_launches
        GROUP BY date_utc
        ORDER BY launch_date DESC;
    """)
    
    # Preview the clean SQL table in the console
    print("\n--- Portfolio Analytics Table Created Successfully! ---")
    print(con.execute("SELECT * FROM daily_summary LIMIT 5").df())
    
    # Close the database connection
    con.close()

if __name__ == "__main__":
    run_pipeline()