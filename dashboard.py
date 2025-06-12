import streamlit as st
import pandas as pd
import sqlite3

def load_data():
    conn = sqlite3.connect('honeypot.db')
    df = pd.read_sql_query("SELECT * FROM attacks ORDER BY timestamp DESC", conn)
    conn.close()
    return df

st.title("Honeypot Real-Time Attack Dashboard")

# Load data
df = load_data()

# Filters
attack_types = df['attack_type'].unique()
selected_attack_type = st.sidebar.multiselect("Filter by Attack Type", attack_types, default=attack_types)

severity_levels = df['severity'].unique()
selected_severity = st.sidebar.multiselect("Filter by Severity", severity_levels, default=severity_levels)

filtered_df = df[
    (df['attack_type'].isin(selected_attack_type)) & 
    (df['severity'].isin(selected_severity))
]

st.write(f"Showing {len(filtered_df)} attack records")

# Display table
st.dataframe(filtered_df)

# Visualization: Attack counts by IP
attack_counts = filtered_df['ip'].value_counts()

st.bar_chart(attack_counts)

# Visualization: Attacks over time
df['timestamp'] = pd.to_datetime(df['timestamp'])
attacks_over_time = filtered_df.groupby(pd.Grouper(key='timestamp', freq='H')).size()
st.line_chart(attacks_over_time)

# Show recent attacks
st.subheader("Most Recent Attacks")
st.table(filtered_df.head(10))
