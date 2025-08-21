# ============================================================
# 🍽️ Local Food Wastage Management System (Streamlit App)
# ------------------------------------------------------------
# This app manages surplus food donations between providers
# (like restaurants, supermarkets) and receivers (like NGOs).
# Features:
# ✅ Dashboard showing key statistics
# ✅ Data filters for better navigation
# ✅ CRUD operations to add/update/delete data
# ✅ Predefined + Custom SQL queries
# ✅ Interactive visualizations using Plotly
# ============================================================

# ------------------------------
# Importing Required Libraries
# ------------------------------
import streamlit as st        # Streamlit - to create interactive web app
import pandas as pd           # Pandas - for handling tabular data
import sqlite3                # SQLite - lightweight relational database
import plotly.express as px   # Plotly Express - for data visualizations

# ------------------------------
# DATABASE CONFIGURATION & UTILITY FUNCTION
# ------------------------------
DB_PATH = "food_wastage.db"  # Path to the SQLite database file

def run_query(query, params=(), commit=False):
    """
    Executes a SQL query on the SQLite database.
    
    Parameters:
    ----------
    query : str
        The SQL query to execute.
    params : tuple
        Parameters for the query (for security and flexibility).
    commit : bool
        If True, commit changes (used for INSERT, UPDATE, DELETE).
    
    Returns:
    -------
    pd.DataFrame or None
        If SELECT query: returns DataFrame with query result.
        Otherwise: returns None.
    """
    # Connect to the database (allow multiple threads with check_same_thread=False)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    if commit:
        # For INSERT, UPDATE, DELETE queries
        conn.execute(query, params)
        conn.commit()   # Save changes to DB
        conn.close()
        return None
    else:
        # For SELECT queries - return results as DataFrame
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df

# ------------------------------
# STREAMLIT PAGE CONFIGURATION
# ------------------------------
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

# App Title (with custom color & emoji)
st.markdown("<h1 style='text-align:center;color:#2E8B57;'>🍽️ Local Food Wastage Management System</h1>", unsafe_allow_html=True)

# ------------------------------
# SIDEBAR MENU
# ------------------------------
# Sidebar navigation options
menu = [
    "🏠 Home",            # Dashboard Overview
    "📦 Providers",       # View Providers data
    "🎯 Receivers",       # View Receivers data
    "🍛 Food Listings",   # View Food Listings
    "📋 Claims",          # View Claims made by Receivers
    "📊 Analysis",        # Insights (Predefined & Custom SQL)
    "✏️ CRUD Operations"  # Add, Update, Delete Records
]

choice = st.sidebar.selectbox("Navigation", menu)

# Sidebar Help Instructions
st.sidebar.markdown("## 📖 How to Use")
st.sidebar.markdown("""
- Navigate between sections using the menu.
- **CRUD Operations** → Add or modify data.
- **Analysis** → Run predefined or custom SQL queries.
- **Charts** → Explore data visually.
""")

# ------------------------------
# HOME PAGE: DASHBOARD OVERVIEW
# ------------------------------
if choice == "🏠 Home":
    st.subheader("Dashboard Overview")

    # Create 4 columns for displaying summary metrics
    col1, col2, col3, col4 = st.columns(4)

    # Fetch total counts from the database
    total_providers = run_query("SELECT COUNT(*) as count FROM providers")["count"][0]
    total_receivers = run_query("SELECT COUNT(*) as count FROM receivers")["count"][0]
    total_listings = run_query("SELECT COUNT(*) as count FROM food_listings")["count"][0]
    total_claims = run_query("SELECT COUNT(*) as count FROM claims")["count"][0]

    # Display the metrics using Streamlit's metric widget
    col1.metric("Providers", total_providers)
    col2.metric("Receivers", total_receivers)
    col3.metric("Food Listings", total_listings)
    col4.metric("Claims", total_claims)

    # Separator line
    st.markdown("---")
    
    # Visualization: Bar chart of providers by city
    st.subheader("Top Provider Cities")
    df_city = run_query("SELECT City, COUNT(*) as provider_count FROM providers GROUP BY City ORDER BY provider_count DESC")
    fig = px.bar(df_city, x="City", y="provider_count", color="provider_count", title="Providers per City")
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# PROVIDERS SECTION
# ------------------------------
elif choice == "📦 Providers":
    st.subheader("All Providers")
    df = run_query("SELECT * FROM providers")
    
    # Filter providers by city
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique()))
    if city_filter != "All":
        df = df[df["City"] == city_filter]
    
    st.dataframe(df)

# ------------------------------
# RECEIVERS SECTION
# ------------------------------
elif choice == "🎯 Receivers":
    st.subheader("All Receivers")
    df = run_query("SELECT * FROM receivers")
    
    # Filter receivers by city
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique()))
    if city_filter != "All":
        df = df[df["City"] == city_filter]
    
    st.dataframe(df)

# ------------------------------
# FOOD LISTINGS SECTION
# ------------------------------
elif choice == "🍛 Food Listings":
    st.subheader("Available Food Listings")
    df = run_query("SELECT * FROM food_listings")
    
    # Apply two filters: by Location and Meal Type
    city_filter = st.selectbox("Filter by Location", ["All"] + sorted(df["Location"].unique()))
    meal_filter = st.selectbox("Filter by Meal Type", ["All"] + sorted(df["Meal_Type"].unique()))
    
    if city_filter != "All":
        df = df[df["Location"] == city_filter]
    if meal_filter != "All":
        df = df[df["Meal_Type"] == meal_filter]
    
    st.dataframe(df)

# ------------------------------
# CLAIMS SECTION
# ------------------------------
elif choice == "📋 Claims":
    st.subheader("Claims Data")
    df = run_query("SELECT * FROM claims")
    
    # Filter claims by status (Pending or Completed)
    status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique()))
    if status_filter != "All":
        df = df[df["Status"] == status_filter]
    
    st.dataframe(df)

# ------------------------------
# ANALYSIS SECTION: Predefined + Custom SQL Queries
# ------------------------------
elif choice == "📊 Analysis":
    st.subheader("Analytical Queries")

    # Dictionary of predefined queries
    queries = {
        "Providers per City": "SELECT City, COUNT(*) AS provider_count FROM providers GROUP BY City ORDER BY provider_count DESC",
        "Receivers per City": "SELECT City, COUNT(*) AS receiver_count FROM receivers GROUP BY City ORDER BY receiver_count DESC",
        "Top Provider Types by Total Quantity": "SELECT Provider_Type, SUM(Quantity) AS total_qty FROM food_listings GROUP BY Provider_Type ORDER BY total_qty DESC",
        "Contact Info of Providers in Delhi": "SELECT Name, Contact, City FROM providers WHERE City='Delhi'",
        "Top Receivers by Claimed Quantity": """SELECT r.Name, SUM(f.Quantity) AS total_claimed 
                                                FROM claims c 
                                                JOIN receivers r ON c.Receiver_ID = r.Receiver_ID 
                                                JOIN food_listings f ON c.Food_ID = f.Food_ID 
                                                GROUP BY r.Name ORDER BY total_claimed DESC"""
    }

    # Dropdown for predefined query selection
    selected_query = st.selectbox("Select a Predefined Query", list(queries.keys()))
    df = run_query(queries[selected_query])
    st.dataframe(df)

    # Auto-generate charts for numeric data
    if "pct" in df.columns:
        # Pie chart for percentage data
        fig = px.pie(df, names="Status", values="pct", title=selected_query)
    elif df.shape[1] == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
        # Bar chart for 2-column numeric queries
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], color=df.columns[1], title=selected_query)
    else:
        fig = None

    if fig:
        st.plotly_chart(fig, use_container_width=True)

    # Custom SQL Query Section
    st.markdown("---")
    st.subheader("🔎 Custom SQL Query Executor")
    custom_query = st.text_area("Enter your SQL query below and click Run:", height=120)
    
    if st.button("Run Custom Query"):
        try:
            df_custom = run_query(custom_query)
            if not df_custom.empty:
                st.success("✅ Query executed successfully!")
                st.dataframe(df_custom)
            else:
                st.info("ℹ️ Query executed but returned no results.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ------------------------------
# CRUD OPERATIONS SECTION
# ------------------------------
elif choice == "✏️ CRUD Operations":
    st.subheader("Manage Records")
    
    # Radio buttons for selecting CRUD operation
    crud_menu = st.radio("Select Operation", ["Add Food Listing", "Add Claim", "Update Claim Status", "Delete Record"])

    # ADD FOOD LISTING
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

    # ADD CLAIM
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

    # UPDATE CLAIM STATUS
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

    # DELETE RECORD
    elif crud_menu == "Delete Record":
        with st.form("delete_record"):
            table = st.selectbox("Table", ["food_listings", "claims"])
            record_id = st.number_input("Record ID", min_value=1)
            
            submitted = st.form_submit_button("Delete")
            if submitted:
                id_col = "Food_ID" if table == "food_listings" else "Claim_ID"
                run_query(f"DELETE FROM {table} WHERE {id_col} = ?", (record_id,), commit=True)
                st.success("✅ Record deleted successfully!")
