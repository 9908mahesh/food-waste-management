# 🍽️ Local Food Wastage Management System

A Streamlit-based web application to manage, analyze, and reduce local food wastage by connecting providers with receivers.  
This project uses a **SQLite database** to store food donation data and provides CRUD operations along with 15 analytical queries for insights.

---

## 📌 Features

### 🔹 Dashboard
- Overview of total providers, receivers, food listings, and claims
- Bar chart of providers per city

### 🔹 Data Sections
- **Providers**: List and filter food providers by city
- **Receivers**: List and filter receivers by city
- **Food Listings**: View and filter available food items by location & meal type
- **Claims**: View and filter claim requests by status

### 🔹 Analysis
- Run 15 predefined SQL queries
- View results in **tables and colorful charts**
- Automatic chart selection (bar or pie) based on data type

### 🔹 CRUD Operations
- Add new food listings
- Add new claims
- Update claim statuses
- Delete listings or claims

---

## 🗄 Database Schema:

**Tables:**
1. **providers**: Stores provider details (Provider_ID, Name, Provider_Type, City, Contact)
2. **receivers**: Stores receiver details (Receiver_ID, Name, Receiver_Type, City, Contact)
3. **food_listings**: Stores details of food available for donation (Food_ID, Provider_ID, Food_Name, Food_Type, Quantity, Meal_Type, Location, Expiry_Date)
4. **claims**: Stores claim transactions for food items (Claim_ID, Food_ID, Receiver_ID, Status)

---
✅ **ER Diagram:**
<img width="288" height="212" alt="image" src="https://github.com/user-attachments/assets/cefd945d-fdb3-4334-9e28-df60aa3112d9" />

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/local-food-wastage-management.git
cd local-food-wastage-management
```

### 2️⃣ Install Dependencies
Make sure you have Python 3.x installed. Then run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Ensure Database is Available
The food_wastage.db file is included in the repo with all required tables and sample data.
If missing, run:
```bash
python create_database.py
```
### 4️⃣ Run the App
```bash
streamlit run app.py
```

---

## 🌐 Online Deployment
The app is hosted on **Streamlit Cloud**:  
[Live Demo](https://food-waste-management-ygo7emuthcwiaf4qxzcsro.streamlit.app/)

---

## 📂 Project Structure
```
.
├── app.py                  # Main Streamlit app
├── food_wastage.db         # SQLite database
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .streamlit/
    └── config.toml         # Theme configuration
```

## ✨ Features
- 📊 **15 Predefined Analytical Queries** with colorful charts (bar, pie).  
- 🔎 **Custom SQL Query Executor** – evaluator can test any SQL query directly.  
- 🏠 **Dashboard Overview** – key stats (providers, receivers, listings, claims).  
- 🗂️ **CRUD Operations** – add, update, and delete food listings and claims.  
- 🎯 **Filters** for quick search by city, food type, meal type, and claim status.  
- 🎨 **Attractive UI** with emojis, colors, and charts for better user experience.  

---

## 📜 License
This project is developed **for academic purposes only**.  
