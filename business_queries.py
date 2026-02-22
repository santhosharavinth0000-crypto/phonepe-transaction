import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="phonepe_db"
)

# ============================================
# CASE 1: Decoding Transaction Dynamics
# ============================================

# 1a. Transaction by Payment Type
case1a = pd.read_sql_query("""
    SELECT Transaction_type,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM aggregated_transaction
    GROUP BY Transaction_type
    ORDER BY Total_amount DESC;
""", conn)
print("CASE 1 - Transaction by Payment Type:")
print(case1a)
print()

# 1b. State-wise Transaction Trends
case1b = pd.read_sql_query("""
    SELECT State, Year, Quarter,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM aggregated_transaction
    WHERE State != 'India'
    GROUP BY State, Year, Quarter
    ORDER BY Total_amount DESC
    LIMIT 10;
""", conn)
print("CASE 1b - State-wise Transaction Trends:")
print(case1b)
print()

# 1c. Quarter-wise Growth
case1c = pd.read_sql_query("""
    SELECT Year, Quarter,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM aggregated_transaction
    WHERE State = 'India'
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
""", conn)
print("CASE 1c - Quarter-wise Growth:")
print(case1c)
print()

# ============================================
# CASE 2: Device Dominance and User Engagement
# ============================================

# 2a. Top Device Brands
case2a = pd.read_sql_query("""
    SELECT Brand,
           SUM(User_count) AS Total_users,
           ROUND(AVG(User_percentage)*100, 2) AS Avg_percentage
    FROM aggregated_user
    WHERE State = 'India'
    GROUP BY Brand
    ORDER BY Total_users DESC
    LIMIT 10;
""", conn)
print("CASE 2a - Top Device Brands:")
print(case2a)
print()

# 2b. App Opens vs Registered Users by State
case2b = pd.read_sql_query("""
    SELECT State,
           SUM(Registered_users) AS Total_registered,
           SUM(App_opens) AS Total_app_opens,
           ROUND(SUM(App_opens)/SUM(Registered_users), 2) AS Opens_per_user
    FROM map_user
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Opens_per_user DESC
    LIMIT 10;
""", conn)
print("CASE 2b - App Opens vs Registered Users:")
print(case2b)
print()

# 2c. Year-wise User Growth
case2c = pd.read_sql_query("""
    SELECT Year,
           SUM(User_count) AS Total_users
    FROM aggregated_user
    WHERE State = 'India'
    GROUP BY Year
    ORDER BY Year;
""", conn)
print("CASE 2c - Year-wise User Growth:")
print(case2c)
print()

# ============================================
# CASE 3: Insurance Penetration and Growth
# ============================================

# 3a. Year-wise Insurance Growth
case3a = pd.read_sql_query("""
    SELECT Year,
           SUM(Insurance_count) AS Total_policies,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM aggregated_insurance
    WHERE State = 'India'
    GROUP BY Year
    ORDER BY Year;
""", conn)
print("CASE 3a - Year-wise Insurance Growth:")
print(case3a)
print()

# 3b. Top States for Insurance Penetration
case3b = pd.read_sql_query("""
    SELECT State,
           SUM(Insurance_count) AS Total_policies,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM aggregated_insurance
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Total_policies DESC
    LIMIT 10;
""", conn)
print("CASE 3b - Top States for Insurance:")
print(case3b)
print()

# 3c. Quarter-wise Insurance Trend
case3c = pd.read_sql_query("""
    SELECT Year, Quarter,
           SUM(Insurance_count) AS Total_policies,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM aggregated_insurance
    WHERE State = 'India'
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
""", conn)
print("CASE 3c - Quarter-wise Insurance Trend:")
print(case3c)
print()

# ============================================
# CASE 4: Transaction Analysis for Market Expansion
# ============================================

# 4a. Top States by Transaction Volume
case4a = pd.read_sql_query("""
    SELECT State,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM aggregated_transaction
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Total_transactions DESC
    LIMIT 10;
""", conn)
print("CASE 4a - Top States by Transaction Volume:")
print(case4a)
print()

# 4b. Low Performing States (Expansion Opportunity)
case4b = pd.read_sql_query("""
    SELECT State,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM aggregated_transaction
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Total_transactions ASC
    LIMIT 10;
""", conn)
print("CASE 4b - Low Performing States:")
print(case4b)
print()

# ============================================
# CASE 5: User Engagement and Growth Strategy
# ============================================

# 5a. Top States by Registered Users
case5a = pd.read_sql_query("""
    SELECT State,
           SUM(Registered_users) AS Total_users,
           SUM(App_opens) AS Total_opens
    FROM map_user
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Total_users DESC
    LIMIT 10;
""", conn)
print("CASE 5a - Top States by Registered Users:")
print(case5a)
print()

# 5b. Top Districts by User Engagement
case5b = pd.read_sql_query("""
    SELECT District,
           SUM(Registered_users) AS Total_users,
           SUM(App_opens) AS Total_opens
    FROM map_user
    GROUP BY District
    ORDER BY Total_users DESC
    LIMIT 10;
""", conn)
print("CASE 5b - Top Districts by User Engagement:")
print(case5b)
print()

# 5c. Low Engagement States
case5c = pd.read_sql_query("""
    SELECT State,
           SUM(Registered_users) AS Total_users,
           SUM(App_opens) AS Total_opens,
           ROUND(SUM(App_opens)/SUM(Registered_users), 2) AS Engagement_ratio
    FROM map_user
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Engagement_ratio ASC
    LIMIT 10;
""", conn)
print("CASE 5c - Low Engagement States:")
print(case5c)
print()

# ============================================
# CASE 6: Insurance Engagement Analysis
# ============================================

# 6a. Top States by Insurance Transactions
case6a = pd.read_sql_query("""
    SELECT State,
           SUM(Insurance_count) AS Total_insurance,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM map_insurance
    WHERE State != 'India'
    GROUP BY State
    ORDER BY Total_insurance DESC
    LIMIT 10;
""", conn)
print("CASE 6a - Top States by Insurance:")
print(case6a)
print()

# 6b. Top Districts by Insurance
case6b = pd.read_sql_query("""
    SELECT District,
           SUM(Insurance_count) AS Total_insurance,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM map_insurance
    GROUP BY District
    ORDER BY Total_insurance DESC
    LIMIT 10;
""", conn)
print("CASE 6b - Top Districts by Insurance:")
print(case6b)
print()

# ============================================
# CASE 7: Transaction Analysis Across States and Districts
# ============================================

# 7a. Top States by Transaction
case7a = pd.read_sql_query("""
    SELECT Entity_name AS State,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM top_transaction
    WHERE Entity_type = 'states'
    GROUP BY Entity_name
    ORDER BY Total_transactions DESC
    LIMIT 10;
""", conn)
print("CASE 7a - Top States by Transaction:")
print(case7a)
print()

# 7b. Top Districts by Transaction
case7b = pd.read_sql_query("""
    SELECT Entity_name AS District,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM top_transaction
    WHERE Entity_type = 'districts'
    GROUP BY Entity_name
    ORDER BY Total_transactions DESC
    LIMIT 10;
""", conn)
print("CASE 7b - Top Districts by Transaction:")
print(case7b)
print()

# 7c. Top Pincodes by Transaction
case7c = pd.read_sql_query("""
    SELECT Entity_name AS Pincode,
           SUM(Transaction_count) AS Total_transactions,
           ROUND(SUM(Transaction_amount), 2) AS Total_amount
    FROM top_transaction
    WHERE Entity_type = 'pincodes'
    GROUP BY Entity_name
    ORDER BY Total_transactions DESC
    LIMIT 10;
""", conn)
print("CASE 7c - Top Pincodes by Transaction:")
print(case7c)
print()

# ============================================
# CASE 8: User Registration Analysis
# ============================================

# 8a. Top States by User Registration
case8a = pd.read_sql_query("""
    SELECT Entity_name AS State,
           SUM(Registered_users) AS Total_users
    FROM top_user
    WHERE Entity_type = 'states'
    GROUP BY Entity_name
    ORDER BY Total_users DESC
    LIMIT 10;
""", conn)
print("CASE 8a - Top States by User Registration:")
print(case8a)
print()

# 8b. Top Districts by User Registration
case8b = pd.read_sql_query("""
    SELECT Entity_name AS District,
           SUM(Registered_users) AS Total_users
    FROM top_user
    WHERE Entity_type = 'districts'
    GROUP BY Entity_name
    ORDER BY Total_users DESC
    LIMIT 10;
""", conn)
print("CASE 8b - Top Districts by User Registration:")
print(case8b)
print()

# 8c. Top Pincodes by User Registration
case8c = pd.read_sql_query("""
    SELECT Entity_name AS Pincode,
           SUM(Registered_users) AS Total_users
    FROM top_user
    WHERE Entity_type = 'pincodes'
    GROUP BY Entity_name
    ORDER BY Total_users DESC
    LIMIT 10;
""", conn)
print("CASE 8c - Top Pincodes by User Registration:")
print(case8c)
print()

# ============================================
# CASE 9: Insurance Transactions Analysis
# ============================================

# 9a. Top States by Insurance Transactions
case9a = pd.read_sql_query("""
    SELECT Entity_name AS State,
           SUM(Insurance_count) AS Total_insurance,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM top_insurance
    WHERE Entity_type = 'states'
    GROUP BY Entity_name
    ORDER BY Total_insurance DESC
    LIMIT 10;
""", conn)
print("CASE 9a - Top States by Insurance:")
print(case9a)
print()

# 9b. Top Districts by Insurance Transactions
case9b = pd.read_sql_query("""
    SELECT Entity_name AS District,
           SUM(Insurance_count) AS Total_insurance,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM top_insurance
    WHERE Entity_type = 'districts'
    GROUP BY Entity_name
    ORDER BY Total_insurance DESC
    LIMIT 10;
""", conn)
print("CASE 9b - Top Districts by Insurance:")
print(case9b)
print()

# 9c. Top Pincodes by Insurance Transactions
case9c = pd.read_sql_query("""
    SELECT Entity_name AS Pincode,
           SUM(Insurance_count) AS Total_insurance,
           ROUND(SUM(Insurance_amount), 2) AS Total_amount
    FROM top_insurance
    WHERE Entity_type = 'pincodes'
    GROUP BY Entity_name
    ORDER BY Total_insurance DESC
    LIMIT 10;
""", conn)
print("CASE 9c - Top Pincodes by Insurance:")
print(case9c)
print()

conn.close()
print("✅ All 9 Business Case Queries Executed Successfully!")