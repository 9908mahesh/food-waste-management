import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Food Wastage Demo", layout="wide")
st.title("Local Food Wastage Management — Demo")

# Show repo files (debug check)
st.write("Files in repo root:", os.listdir('.'))

# Path to database
db_path = "food_wastage.db"
st.write("DB exists?", os.path.exists(db_path))

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)

    st.subheader("Providers")
    df_providers = pd.read_sql_query("SELECT * FROM providers", conn)
    st.dataframe(df_providers)

    st.subheader("Food Listings")
    df_food = pd.read_sql_query("SELECT * FROM food_listings", conn)
    st.dataframe(df_food)

    st.subheader("Claims")
    df_claims = pd.read_sql_query("SELECT * FROM claims", conn)
    st.dataframe(df_claims)

    st.subheader("Providers per City (Sample Query)")
    q = "SELECT city, COUNT(*) AS provider_count FROM providers GROUP BY city"
    st.table(pd.read_sql_query(q, conn))

    conn.close()
else:
    st.error("Database file not found in repo root.")
