import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Database connection
DB_PATH = "food_wastage.db"

def get_data(query):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Page setup
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")
st.title("Local Food Wastage Management System")

menu = ["Providers", "Receivers", "Food Listings", "Claims", "Analysis"]
choice = st.sidebar.selectbox("Menu", menu)

# --------------- Providers ---------------
if choice == "Providers":
    st.subheader("All Providers")
    df = get_data("SELECT * FROM providers")
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique().tolist()))
    if city_filter != "All":
        df = df[df["City"] == city_filter]
    st.dataframe(df)

# --------------- Receivers ---------------
elif choice == "Receivers":
    st.subheader("All Receivers")
    df = get_data("SELECT * FROM receivers")
    city_filter = st.selectbox("Filter by City", ["All"] + sorted(df["City"].unique().tolist()))
    if city_filter != "All":
        df = df[df["City"] == city_filter]
    st.dataframe(df)

# --------------- Food Listings ---------------
elif choice == "Food Listings":
    st.subheader("Available Food Listings")
    df = get_data("SELECT * FROM food_listings")
    # Filters
    city_filter = st.selectbox("Filter by Location", ["All"] + sorted(df["Location"].unique().tolist()))
    meal_filter = st.selectbox("Filter by Meal Type", ["All"] + sorted(df["Meal_Type"].unique().tolist()))
    if city_filter != "All":
        df = df[df["Location"] == city_filter]
    if meal_filter != "All":
        df = df[df["Meal_Type"] == meal_filter]
    st.dataframe(df)

# --------------- Claims ---------------
elif choice == "Claims":
    st.subheader("Claims Data")
    df = get_data("SELECT * FROM claims")
    status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique().tolist()))
    if status_filter != "All":
        df = df[df["Status"] == status_filter]
    st.dataframe(df)

# --------------- Analysis ---------------
elif choice == "Analysis":
    st.subheader("Analytical Queries")

    queries = {
        "Providers per City":
            "SELECT City, COUNT(*) AS provider_count FROM providers GROUP BY City ORDER BY provider_count DESC",
        "Receivers per City":
            "SELECT City, COUNT(*) AS receiver_count FROM receivers GROUP BY City ORDER BY receiver_count DESC",
        "Top Provider Types by Total Quantity":
            "SELECT Provider_Type, SUM(Quantity) AS total_qty FROM food_listings GROUP BY Provider_Type ORDER BY total_qty DESC",
        "Contact Info of Providers in a City":
            "SELECT Name, Contact, City FROM providers",
        "Top Receivers by Claimed Quantity":
            """SELECT r.Name, COUNT(c.Claim_ID) AS claims_count, COALESCE(SUM(f.Quantity),0) AS total_quantity_claimed
               FROM claims c
               JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
               LEFT JOIN food_listings f ON c.Food_ID = f.Food_ID
               GROUP BY r.Name ORDER BY total_quantity_claimed DESC LIMIT 10""",
        "Total Quantity of Food Available":
            "SELECT SUM(Quantity) AS total_available FROM food_listings",
        "City with Most Food Listings":
            "SELECT Location, COUNT(*) AS listings FROM food_listings GROUP BY Location ORDER BY listings DESC LIMIT 1",
        "Most Common Food Types":
            "SELECT Food_Type, COUNT(*) AS freq FROM food_listings GROUP BY Food_Type ORDER BY freq DESC",
        "Claims per Food Item":
            """SELECT f.Food_Name, COUNT(c.Claim_ID) AS claims
               FROM food_listings f
               LEFT JOIN claims c ON f.Food_ID = c.Food_ID
               GROUP BY f.Food_Name ORDER BY claims DESC""",
        "Top Provider by Completed Claims":
            """SELECT p.Name, COUNT(c.Claim_ID) AS completed_claims
               FROM providers p
               JOIN food_listings f ON p.Provider_ID = f.Provider_ID
               JOIN claims c ON f.Food_ID = c.Food_ID
               WHERE c.Status = 'Completed'
               GROUP BY p.Name ORDER BY completed_claims DESC LIMIT 1""",
        "Claim Status Percentage":
            """SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS pct
               FROM claims GROUP BY Status""",
        "Average Quantity Claimed per Receiver":
            """SELECT r.Name, AVG(f.Quantity) AS avg_qty_claimed
               FROM claims c
               JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
               JOIN food_listings f ON c.Food_ID = f.Food_ID
               GROUP BY r.Name ORDER BY avg_qty_claimed DESC""",
        "Most Claimed Meal Type":
            """SELECT f.Meal_Type, COUNT(c.Claim_ID) AS claims_count
               FROM claims c
               JOIN food_listings f ON c.Food_ID = f.Food_ID
               GROUP BY f.Meal_Type ORDER BY claims_count DESC""",
        "Total Quantity Donated by Each Provider":
            """SELECT p.Name, SUM(f.Quantity) AS total_donated
               FROM providers p
               JOIN food_listings f ON p.Provider_ID = f.Provider_ID
               GROUP BY p.Name ORDER BY total_donated DESC""",
    }

    selected_query = st.selectbox("Select a Query", list(queries.keys()))
    df = get_data(queries[selected_query])
    st.dataframe(df)

    # Auto-generate charts for numeric queries
    if df.shape[1] == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=selected_query)
        st.plotly_chart(fig, use_container_width=True)

