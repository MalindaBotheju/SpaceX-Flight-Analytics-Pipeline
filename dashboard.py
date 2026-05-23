import streamlit as st
import duckdb
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="SpaceX Launch Analytics", layout="wide")
st.title("🚀 SpaceX Historical Launch Analytics")
st.markdown("This live dashboard reads data automatically processed by our DuckDB pipeline.")

# 2. Query the Data from DuckDB
con = duckdb.connect('analytics.duckdb')
df = con.execute("SELECT * FROM daily_summary ORDER BY launch_date ASC").df()
con.close()

# Convert launch_date to datetime for better plotting
df['launch_date'] = pd.to_datetime(df['launch_date'])

# 3. Create Key Metrics Layout
total_missions = int(df['total_launches'].sum())
total_successes = int(df['successful_launches'].sum())
success_rate = (total_successes / total_missions) * 100 if total_missions > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Missions Tracked", total_missions)
col2.metric("Successful Launches", total_successes)
col3.metric("Overall Success Rate", f"{success_rate:.1f}%")

st.markdown("---")

# 4. Interactive Time-Series Line Chart
st.subheader("Launch Trends Over Time")
# Cumulative metrics for visual appeal
df['Cumulative Launches'] = df['total_launches'].cumsum()
st.line_chart(data=df, x='launch_date', y='Cumulative Launches', use_container_width=True)

# 5. Raw Data Preview Dropdown
with st.expander("View Raw Aggregated Data Schema"):
    st.dataframe(df, use_container_width=True)