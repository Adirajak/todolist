import streamlit as st
import sqlite3
import pandas as pd
import os

# Adjust DB_FILE path relative to the current script location for reliability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "..", "honeypot", "honeypot_logs.db")

def get_logs():
    # Use a context manager to ensure connection closes properly
    with sqlite3.connect(DB_FILE) as conn:
        query = "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql_query(query, conn)
    return df

def main():
    st.title("Honeypot Attack Dashboard")

    # Fetch latest logs
    logs = get_logs()

    if logs.empty:
        st.info("No attack logs found yet.")
    else:
        # Show summary stats
        st.subheader("Summary")
        st.write(f"Total Attack Events: {len(logs)}")
        st.write(f"Unique Attacker IPs: {logs['ip'].nunique()}")

        # Filter by IP
        ip_filter = st.text_input("Filter by IP (leave empty for all)")

        if ip_filter:
            filtered_logs = logs[logs['ip'].str.contains(ip_filter)]
        else:
            filtered_logs = logs

        st.subheader("Recent Attack Logs")
        st.dataframe(filtered_logs)

        # Simple bar chart of attacks per IP
        st.subheader("Attacks by IP")
        ip_counts = filtered_logs['ip'].value_counts()
        st.bar_chart(ip_counts)

if __name__ == "__main__":
    main()
