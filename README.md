# PhonePe Transaction Insights Dashboard

A comprehensive data analytics dashboard built with **Streamlit** to visualize 
and analyze PhonePe Pulse transaction data across India.

---

##  Project Overview

This dashboard analyzes PhonePe's publicly available Pulse data to provide:

- **Transaction Dynamics** – Year-over-year growth, payment types, state performance
- **Device & User Engagement** – Brand market share, app usage patterns
- **Insurance Analytics** – Policy trends and state-wise penetration
- **Market Expansion** – Top and low performing states and districts
- **Top Performers** – States, districts, and pincodes by volume
- **India Heatmap** – Choropleth map for visual geographic analysis

---

##  Dashboard Pages

| Page | Description |
|------|-------------|
|  Home | Key metrics – Total Transactions, Amount, Users, Insurance |
|  Transaction Analysis | Payment type breakdown, quarter-wise growth, state trends |
|  User & Device Analysis | Top device brands, app opens vs users, year-wise growth |
|  Insurance Analysis | Year-wise growth, top states, quarter-wise trend |
|  Market Expansion | High and low performing states for business strategy |
|  Top Performers | Top states, districts and pincodes by transaction volume |
|  India Map | Interactive choropleth map for Transactions, Users, Insurance |

---

##  Technology Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| MySQL | Database to store all 9 tables |
| Streamlit | Interactive web dashboard |
| Plotly | Charts – bar, pie, line, choropleth |
| Pandas | Data processing and analysis |
| mysql-connector-python | MySQL to Python connection |

---

##  Installation

### Step 1 – Install Required Libraries
```
pip install streamlit plotly mysql-connector-python pandas
```

### Step 2 – Clone PhonePe Pulse Data
```
git clone https://github.com/PhonePe/pulse.git
```

### Step 3 – Setup MySQL Database
```sql
CREATE DATABASE phonepe_db;
```

### Step 4 – Extract and Load Data
```
python data_extraction.py
```

### Step 5 – Run the Dashboard
```
streamlit run app.py
```

Dashboard opens at: **http://localhost:8501**

---

## Database Schema (9 Tables)

| Category | Table Name | Description |
|----------|-----------|-------------|
| Aggregated | aggregated_transaction | Payment type, count, amount |
| Aggregated | aggregated_user | Device brand, user count |
| Aggregated | aggregated_insurance | Insurance count and amount |
| Map | map_transaction | District-level transactions |
| Map | map_user | Registered users and app opens |
| Map | map_insurance | District-level insurance data |
| Top | top_transaction | Top states, districts, pincodes |
| Top | top_user | Top user regions |
| Top | top_insurance | Top insurance regions |

---

##  Project Structure
```
phonepe_project/
│
├── app.py                  # Streamlit Dashboard (7 pages)
├── data_extraction.py      # JSON to MySQL extraction (9 tables)
├── business_queries.py     # 9 Business case SQL queries
│
└── Strmilit_Dashboard/     # Dashboard screenshots
    ├── Home.jpg
    ├── Tran_Type.jpg
    ├── User&Device_Analysis.jpg
    ├── Insurance_Analysis.jpg
    ├── Market_expansions.jpg
    ├── TOP_perf.jpg
    └── India_Map.jpg
```

---

## Key Business Insights

# Transaction Insights
- Peer-to-peer payments are the **highest transaction type**
- Consistent **quarter-over-quarter growth** from 2018 to 2024
- **Karnataka, Maharashtra, Telangana** are the top 3 states

# User Insights
- **Xiaomi** leads with highest market share among device brands
- **Maharashtra** has the most registered users
- App engagement is highest in southern states

# Insurance Insights
- Insurance transactions grew **6x from 2020 to 2024**
- **Karnataka** leads in insurance policy adoption
- Bengaluru Urban is the top district for insurance

# Market Expansion
- North-eastern states show **lowest transaction volumes** — expansion opportunity
- Metro cities dominate pincode-level transaction data

---

# Security Notes
- Never commit real database passwords to GitHub
- Use placeholder: `password="your_password"` in uploaded files

---

# Data Source
PhonePe Pulse – Official public data repository  
https://github.com/PhonePe/pulse

---

# Domain
**Finance / Payment Systems**
