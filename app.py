# ------------------------------
# Local Food Wastage Management System - Enhanced Version
# With Dashboard, CRUD Operations, Colorful Charts, and Icons
# ------------------------------

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ------------------------------
# Database Functions
# ------------------------------
DB_PATH = "food_wastage.db"

def run_query(query, params=(), commit=False):
    """Run a SQL query and return the result as a DataFrame."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    if commit:
        conn.execute(query, params)
        conn.commit()
        conn.close()
        return None
    else:
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")
st.markdown("<h1 style='text-align:center;color:#2E8B57;'>🍽️ Local Food Wastage Management System</h1>", unsafe_allow_html=True)

# ------------------------------
# Sidebar Menu
# ------------------------------
menu = [
    "🏠 Home",
    "📦 Providers",
    "🎯 Receivers",
    "🍛 Food Listings",
    "📋 Claims",
    "📊 Analysis",
    "✏️ CRUD Operations"
]
choice = st.sidebar.selectbox("Navigation", menu)

# Sidebar Instructions
st.sidebar.markdown("## 📖 How to Use")
st.sidebar.markdown("""
- Navigate using the menu.
- Apply filters for quick search.
- Use **CRUD Operations** to add, update, or delete records.
- Go to **Analysis** for trends and insights.
""")

# ------------------------------
# Home Page
# ------------------------------
if choice == "🏠 Home":
    st.subheader("Dashboard Overview")
    col1, col2, col3, col4 = st.columns(4)

    total_providers = run_query("SELECT COUNT(*) as count FROM providers")["count"][0]
    total_receivers = run_query("SELECT COUNT(*) as count FROM receivers")["count"][0]
    total_listings = run_query("SELECT COUNT(*) as count FROM food_listings")["count"][0]
    total_claims = run_query("SELECT COUNT(*) as count FROM claims")["count"][0]

    col1.metric("Providers", total_providers)
    col2.metric("Receivers", total_receivers)
    col3.metric("Food Listings", total_listings)
    col4.metric("Claims", total_claims)

    st.markdown("---")
    st.subheader("Top Provider Cities")
    df_city = run_query("SELECT City, COUNT(*) as provider_count FROM providers GROUP BY City ORDER BY provider_count DESC")
    fig = px.bar(df_city, x="City", y="provider_count", color="provider_count", title="Providers per City")
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Providers
# ------------------------------
elif choice == "📦 Providers":
    st.subheader("All Providers")
    df = run_query("SELECT * FROM providers")
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique()))
    if city_filter != "All":
        df = df[df["City"] == city_filter]
    st.dataframe(df)

# ------------------------------
# Receivers
# ------------------------------
elif choice == "🎯 Receivers":
    st.subheader("All Receivers")
    df = run_query("SELECT * FROM receivers")
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique()))
    if city_filter != "All":
        df = df[df["City"] == city_filter]
    st.dataframe(df)

# ------------------------------
# Food Listings
# ------------------------------
elif choice == "🍛 Food Listings":
    st.subheader("Available Food Listings")
    df = run_query("SELECT * FROM food_listings")
    city_filter = st.selectbox("Filter by Location", ["All"] + sorted(df["Location"].unique()))
    meal_filter = st.selectbox("Filter by Meal Type", ["All"] + sorted(df["Meal_Type"].unique()))
    if city_filter != "All":
        df = df[df["Location"] == city_filter]
    if meal_filter != "All":
        df = df[df["Meal_Type"] == meal_filter]
    st.dataframe(df)

# ------------------------------
# Claims
# ------------------------------
elif choice == "📋 Claims":
    st.subheader("Claims Data")
    df = run_query("SELECT * FROM claims")
    status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique()))
    if status_filter != "All":
        df = df[df["Status"] == status_filter]
    st.dataframe(df)

# ------------------------------
# Analysis
# ------------------------------
elif choice == "📊 Analysis":
    st.subheader("Analytical Queries")
    queries = {
        "Providers per City": "SELECT City, COUNT(*) AS provider_count FROM providers GROUP BY City ORDER BY provider_count DESC",
        "Receivers per City": "SELECT City, COUNT(*) AS receiver_count FROM receivers GROUP BY City ORDER BY receiver_count DESC",
        "Top Provider Types by Total Quantity": "SELECT Provider_Type, SUM(Quantity) AS total_qty FROM food_listings GROUP BY Provider_Type ORDER BY total_qty DESC",
        "Claim Status Percentage": "SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS pct FROM claims GROUP BY Status",
    }
    selected_query = st.selectbox("Select a Query", list(queries.keys()))
    df = run_query(queries[selected_query])
    st.dataframe(df)

    if "pct" in df.columns:
        fig = px.pie(df, names="Status", values="pct", title=selected_query)
    elif df.shape[1] == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], color=df.columns[1], title=selected_query)
    else:
        fig = None

    if fig:
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# CRUD Operations
# ------------------------------
elif choice == "✏️ CRUD Operations":
    st.subheader("Manage Records")
    crud_menu = st.radio("Select Operation", ["Add Food Listing", "Add Claim", "Update Claim Status", "Delete Record"])

    # Add Food Listing
    if crud_menu == "Add Food Listing":
        with st.form("add_listing"):
            provider_id = st.number_input("Provider ID", min_value=1)
            food_name = st.text_input("Food Name")
            food_type = st.text_input("Food Type")
            quantity = st.number_input("Quantity", min_value=1)
            meal_type = st.text_input("Meal Type")
            location = st.text_input("Location")
            expiry_date = st.date_input("Expiry Date")
            submitted = st.form_submit_button("Add Listing")
            if submitted:
                run_query(
                    "INSERT INTO food_listings (Provider_ID, Food_Name, Food_Type, Quantity, Meal_Type, Location, Expiry_Date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (provider_id, food_name, food_type, quantity, meal_type, location, str(expiry_date)),
                    commit=True
                )
                st.success("✅ Food listing added successfully!")

    # Add Claim
    elif crud_menu == "Add Claim":
        with st.form("add_claim"):
            food_id = st.number_input("Food ID", min_value=1)
            receiver_id = st.number_input("Receiver ID", min_value=1)
            status = st.selectbox("Status", ["Pending", "Completed"])
            submitted = st.form_submit_button("Add Claim")
            if submitted:
                run_query(
                    "INSERT INTO claims (Food_ID, Receiver_ID, Status) VALUES (?, ?, ?)",
                    (food_id, receiver_id, status),
                    commit=True
                )
                st.success("✅ Claim added successfully!")

    # Update Claim Status
    elif crud_menu == "Update Claim Status":
        with st.form("update_claim"):
            claim_id = st.number_input("Claim ID", min_value=1)
            new_status = st.selectbox("New Status", ["Pending", "Completed"])
            submitted = st.form_submit_button("Update Status")
            if submitted:
                run_query(
                    "UPDATE claims SET Status = ? WHERE Claim_ID = ?",
                    (new_status, claim_id),
                    commit=True
                )
                st.success("✅ Claim status updated successfully!")

    # Delete Record
    elif crud_menu == "Delete Record":
        with st.form("delete_record"):
            table = st.selectbox("Table", ["food_listings", "claims"])
            record_id = st.number_input("Record ID", min_value=1)
            submitted = st.form_submit_button("Delete")
            if submitted:
                id_col = "Food_ID" if table == "food_listings" else "Claim_ID"
                run_query(f"DELETE FROM {table} WHERE {id_col} = ?", (record_id,), commit=True)
                st.success("✅ Record deleted successfully!")
