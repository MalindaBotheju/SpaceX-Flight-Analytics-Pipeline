# SpaceX Flight Analytics Pipeline 🚀

An automated, serverless ELT data pipeline that extracts live aerospace launch records from a public REST API, transforms data on-the-fly using DuckDB SQL, and displays real-time metrics on a public interactive dashboard.

## 🔗 Live Interactive Dashboard
👉 **[View the Live Analytics Dashboard Here](https://spacex-flight-analytics-pipeline-mrnqnuoqjxr4joe9rftjbu.streamlit.app/)**

---

## 🛠️ Architecture & Tools
* **Language:** Python 3.10 (Data extraction & data staging)
* **Data Warehouse Engine:** DuckDB (High-performance analytical SQL processing over CSV)
* **Orchestration & Automation:** GitHub Actions (Daily serverless cron scheduling)
* **Data Visualization Frontend:** Streamlit Community Cloud (Hosted interactive reporting)
* **Data Source:** SpaceX Public v4 REST API

---

## 🔄 Data Pipeline Workflow

```text
[Public API] ──(Python Extract)──> [spacex_launches.csv] ──(GitHub Commit)──> [DuckDB SQL Engine] ──> [Streamlit Web UI]

```

1. **Extract:** A Python script connects to the public SpaceX API and fetches raw nested JSON launch data.
2. **Load:** The raw JSON fields are structured into a Pandas DataFrame and stored as a lightweight, version-controlled flat file (`spacex_launches.csv`).
3. **Orchestrate:** GitHub Actions wakes up a serverless environment daily at 9:00 AM UTC, executes the extraction pipeline, and pushes data updates automatically back to the repo.
4. **Transform (On-the-Fly SQL):** The reporting tier initializes an in-memory **DuckDB** instance to execute high-performance analytical SQL transformations directly on top of the raw CSV file.
5. **Serve:** Streamlit reads the processed data schema to deliver key metric callouts and an interactive time-series chart to end users.

---

## 📊 Sample SQL Analytics Transformation

The dashboard uses DuckDB to run ultra-fast file queries without requiring a heavy, always-on database server:

```sql
SELECT 
    date_utc AS launch_date,
    COUNT(*) AS total_launches,
    COUNT(CASE WHEN success = true THEN 1 END) AS successful_launches
FROM read_csv_auto('spacex_launches.csv')
GROUP BY date_utc
ORDER BY launch_date ASC;

```

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone [https://github.com/MalindaBotheju/SpaceX-Flight-Analytics-Pipeline.git](https://github.com/MalindaBotheju/SpaceX-Flight-Analytics-Pipeline.git)
cd SpaceX-Flight-Analytics-Pipeline

```

### 2. Install dependencies

```bash
pip install -r requirements.txt

```

### 3. Run the pipeline script

```bash
python pipeline.py

```

### 4. Boot up the interactive dashboard

```bash
streamlit run dashboard.py

```

```

***

### 💡 Pro-Tip for your GitHub Profile:
Once you commit this, your repository homepage will look incredibly sharp, professional, and completely ready to be sent over to recruiters!

```