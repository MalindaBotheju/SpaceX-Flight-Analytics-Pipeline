import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="SpaceX Launch Analytics", layout="wide")
st.title("🚀 SpaceX Historical Launch Analytics")
st.markdown("This live dashboard reads data automatically processed by our Python pipeline.")

# Connect to a temporary in-memory DuckDB instance and query the CSV file directly!
con = duckdb.connect()
df = con.execute("""
    SELECT 
        date_utc AS launch_date,
        COUNT(*) AS total_launches,
        COUNT(CASE WHEN success = true THEN 1 END) AS successful_launches
    FROM read_csv_auto('spacex_launches.csv')
    GROUP BY date_utc
    ORDER BY launch_date ASC
""").df()
con.close()

df['launch_date'] = pd.to_datetime(df['launch_date'])

# Metrics
total_missions = int(df['total_launches'].sum())
total_successes = int(df['successful_launches'].sum())
success_rate = (total_successes / total_missions) * 100 if total_missions > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Missions Tracked", total_missions)
col2.metric("Successful Launches", total_successes)
col3.metric("Overall Success Rate", f"{success_rate:.1f}%")

st.markdown("---")

st.subheader("Launch Trends Over Time")
df['Cumulative Launches'] = df['total_launches'].cumsum()
st.line_chart(data=df, x='launch_date', y='Cumulative Launches', use_container_width=True)

with st.expander("View Raw Aggregated Data Schema"):
    st.dataframe(df, use_container_width=True)