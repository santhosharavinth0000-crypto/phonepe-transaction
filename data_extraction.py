import json
import os
import pandas as pd
import mysql.connector

# MySQL Connection

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_db;")
cursor.execute("USE phonepe_db;")
conn.commit()

#  PATH
base_path = r"C:\Users\SMB140\Desktop\pulse-master\data\\"

# 1. AGGREGATED TRANSACTION

cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        Transaction_type VARCHAR(100),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    );
""")

path = base_path + r"aggregated\transaction\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        filepath = os.path.join(path, year, file)
        with open(filepath) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for txn in data["data"]["transactionData"]:
            rows.append(("India", int(year), quarter,
                         txn["name"],
                         txn["paymentInstruments"][0]["count"],
                         txn["paymentInstruments"][0]["amount"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            filepath = os.path.join(state_path, state, year, file)
            with open(filepath) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for txn in data["data"]["transactionData"]:
                rows.append((state, int(year), quarter,
                             txn["name"],
                             txn["paymentInstruments"][0]["count"],
                             txn["paymentInstruments"][0]["amount"]))

cursor.executemany("""
    INSERT INTO aggregated_transaction
    (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" aggregated_transaction — {len(rows)} rows inserted")

# 2. AGGREGATED USER

cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        Brand VARCHAR(100),
        User_count BIGINT,
        User_percentage DOUBLE
    );
""")

path = base_path + r"aggregated\user\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        if data["data"]["usersByDevice"]:
            for device in data["data"]["usersByDevice"]:
                rows.append(("India", int(year), quarter,
                             device["brand"],
                             device["count"],
                             device["percentage"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            if data["data"]["usersByDevice"]:
                for device in data["data"]["usersByDevice"]:
                    rows.append((state, int(year), quarter,
                                 device["brand"],
                                 device["count"],
                                 device["percentage"]))

cursor.executemany("""
    INSERT INTO aggregated_user
    (State, Year, Quarter, Brand, User_count, User_percentage)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" aggregated_user — {len(rows)} rows inserted")


# 3. AGGREGATED INSURANCE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_insurance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        Insurance_type VARCHAR(100),
        Insurance_count BIGINT,
        Insurance_amount DOUBLE
    );
""")

path = base_path + r"aggregated\insurance\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for txn in data["data"]["transactionData"]:
            rows.append(("India", int(year), quarter,
                         txn["name"],
                         txn["paymentInstruments"][0]["count"],
                         txn["paymentInstruments"][0]["amount"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for txn in data["data"]["transactionData"]:
                rows.append((state, int(year), quarter,
                             txn["name"],
                             txn["paymentInstruments"][0]["count"],
                             txn["paymentInstruments"][0]["amount"]))

cursor.executemany("""
    INSERT INTO aggregated_insurance
    (State, Year, Quarter, Insurance_type, Insurance_count, Insurance_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" aggregated_insurance — {len(rows)} rows inserted")


# 4. MAP TRANSACTION

cursor.execute("""
    CREATE TABLE IF NOT EXISTS map_transaction (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        District VARCHAR(100),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    );
""")

path = base_path + r"map\transaction\hover\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for item in data["data"]["hoverDataList"]:
            rows.append(("India", int(year), quarter,
                         item["name"],
                         item["metric"][0]["count"],
                         item["metric"][0]["amount"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for item in data["data"]["hoverDataList"]:
                rows.append((state, int(year), quarter,
                             item["name"],
                             item["metric"][0]["count"],
                             item["metric"][0]["amount"]))

cursor.executemany("""
    INSERT INTO map_transaction
    (State, Year, Quarter, District, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" map_transaction — {len(rows)} rows inserted")

# 5. MAP USER

cursor.execute("""
    CREATE TABLE IF NOT EXISTS map_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        District VARCHAR(100),
        Registered_users BIGINT,
        App_opens BIGINT
    );
""")

path = base_path + r"map\user\hover\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for district, values in data["data"]["hoverData"].items():
            rows.append(("India", int(year), quarter,
                         district,
                         values["registeredUsers"],
                         values["appOpens"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for district, values in data["data"]["hoverData"].items():
                rows.append((state, int(year), quarter,
                             district,
                             values["registeredUsers"],
                             values["appOpens"]))

cursor.executemany("""
    INSERT INTO map_user
    (State, Year, Quarter, District, Registered_users, App_opens)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" map_user — {len(rows)} rows inserted")


# 6. MAP INSURANCE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS map_insurance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        District VARCHAR(100),
        Insurance_count BIGINT,
        Insurance_amount DOUBLE
    );
""")

path = base_path + r"map\insurance\hover\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for item in data["data"]["hoverDataList"]:
            rows.append(("India", int(year), quarter,
                         item["name"],
                         item["metric"][0]["count"],
                         item["metric"][0]["amount"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for item in data["data"]["hoverDataList"]:
                rows.append((state, int(year), quarter,
                             item["name"],
                             item["metric"][0]["count"],
                             item["metric"][0]["amount"]))

cursor.executemany("""
    INSERT INTO map_insurance
    (State, Year, Quarter, District, Insurance_count, Insurance_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" map_insurance — {len(rows)} rows inserted")


# 7. TOP TRANSACTION

cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_transaction (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        Entity_name VARCHAR(100),
        Entity_type VARCHAR(50),
        Transaction_count BIGINT,
        Transaction_amount DOUBLE
    );
""")

path = base_path + r"top\transaction\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for entity_type in ["states", "districts", "pincodes"]:
            for item in data["data"][entity_type]:
                rows.append(("India", int(year), quarter,
                             item["entityName"],
                             entity_type,
                             item["metric"]["count"],
                             item["metric"]["amount"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for entity_type in ["districts", "pincodes"]:
                for item in data["data"][entity_type]:
                    rows.append((state, int(year), quarter,
                                 item["entityName"],
                                 entity_type,
                                 item["metric"]["count"],
                                 item["metric"]["amount"]))

cursor.executemany("""
    INSERT INTO top_transaction
    (State, Year, Quarter, Entity_name, Entity_type, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" top_transaction — {len(rows)} rows inserted")


# 8. TOP USER

cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        Entity_name VARCHAR(100),
        Entity_type VARCHAR(50),
        Registered_users BIGINT
    );
""")

path = base_path + r"top\user\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for entity_type in ["states", "districts", "pincodes"]:
            for item in data["data"][entity_type]:
                rows.append(("India", int(year), quarter,
                             item["name"],
                             entity_type,
                             item["registeredUsers"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for entity_type in ["districts", "pincodes"]:
                for item in data["data"][entity_type]:
                    rows.append((state, int(year), quarter,
                                 item["name"],
                                 entity_type,
                                 item["registeredUsers"]))

cursor.executemany("""
    INSERT INTO top_user
    (State, Year, Quarter, Entity_name, Entity_type, Registered_users)
    VALUES (%s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" top_user — {len(rows)} rows inserted")


# 9. TOP INSURANCE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_insurance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        State VARCHAR(100),
        Year INT,
        Quarter INT,
        Entity_name VARCHAR(100),
        Entity_type VARCHAR(50),
        Insurance_count BIGINT,
        Insurance_amount DOUBLE
    );
""")

path = base_path + r"top\insurance\country\india\\"
rows = []

for year in os.listdir(path):
    if year == "state": continue
    for file in os.listdir(os.path.join(path, year)):
        with open(os.path.join(path, year, file)) as f:
            data = json.load(f)
        quarter = int(file.replace(".json",""))
        for entity_type in ["states", "districts", "pincodes"]:
            for item in data["data"][entity_type]:
                rows.append(("India", int(year), quarter,
                             item["entityName"],
                             entity_type,
                             item["metric"]["count"],
                             item["metric"]["amount"]))

state_path = os.path.join(path, "state")
for state in os.listdir(state_path):
    for year in os.listdir(os.path.join(state_path, state)):
        for file in os.listdir(os.path.join(state_path, state, year)):
            with open(os.path.join(state_path, state, year, file)) as f:
                data = json.load(f)
            quarter = int(file.replace(".json",""))
            for entity_type in ["districts", "pincodes"]:
                for item in data["data"][entity_type]:
                    rows.append((state, int(year), quarter,
                                 item["entityName"],
                                 entity_type,
                                 item["metric"]["count"],
                                 item["metric"]["amount"]))

cursor.executemany("""
    INSERT INTO top_insurance
    (State, Year, Quarter, Entity_name, Entity_type, Insurance_count, Insurance_amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", rows)
conn.commit()
print(f" top_insurance — {len(rows)} rows inserted")

# ============================================
# CLOSE CONNECTION
# ============================================
cursor.close()
conn.close()
print("\n🎉 ALL 9 TABLES CREATED AND LOADED SUCCESSFULLY!")
