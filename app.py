import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


# Connection

def get_data(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="phonepe_db"
    )
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Page Config

st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="📱",
    layout="wide"
)


# Sidebar Navigation

st.sidebar.title("📱 PhonePe Insights")
page = st.sidebar.radio("Go to", [
    "Home",
    "Transaction Analysis",
    "User & Device Analysis",
    "Insurance Analysis",
    "Market Expansion",
    "Top Performers",
    "India Map"
])


# PAGE 1: HOME

if page == "Home":
    st.title("📱 PhonePe Transaction Insights Dashboard")
    st.write("Welcome! This dashboard analyzes PhonePe digital payment data across India.")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    total_txn = get_data("SELECT SUM(Transaction_count) as total FROM aggregated_transaction WHERE State='India'")
    total_amt = get_data("SELECT SUM(Transaction_amount) as total FROM aggregated_transaction WHERE State='India'")
    total_users = get_data("SELECT SUM(Registered_users) as total FROM map_user WHERE State!='India'")
    total_ins = get_data("SELECT SUM(Insurance_count) as total FROM aggregated_insurance WHERE State='India'")

    with col1:
        st.metric("💳 Total Transactions", f"{total_txn['total'][0]/1e9:.2f}B")
    with col2:
        st.metric("💰 Total Amount", f"₹{total_amt['total'][0]/1e12:.2f}T")
    with col3:
        st.metric("👥 Registered Users", f"{total_users['total'][0]/1e9:.2f}B")
    with col4:
        st.metric("🛡️ Total Insurance", f"{total_ins['total'][0]/1e6:.2f}M")


# PAGE 2: TRANSACTION ANALYSIS

elif page == "Transaction Analysis":
    st.title("💳 Transaction Analysis")

    tab1, tab2, tab3 = st.tabs([
        "By Payment Type",
        "Quarter-wise Growth",
        "State-wise Trends"
    ])

    with tab1:
        st.subheader("Transaction by Payment Type")
        df = get_data("""
            SELECT Transaction_type,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM aggregated_transaction
            GROUP BY Transaction_type
            ORDER BY Total_amount DESC
        """)
        st.dataframe(df)
        fig = px.bar(df, x="Transaction_type", y="Total_amount",
                     title="Total Amount by Payment Type",
                     color="Transaction_type")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.pie(df, names="Transaction_type", values="Total_transactions",
                      title="Transaction Count Share by Type")
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Quarter-wise Growth")
        df = get_data("""
            SELECT Year, Quarter,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM aggregated_transaction
            WHERE State = 'India'
            GROUP BY Year, Quarter
            ORDER BY Year, Quarter
        """)
        df["Year_Quarter"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        st.dataframe(df)
        fig = px.line(df, x="Year_Quarter", y="Total_transactions",
                      title="Quarter-wise Transaction Growth",
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("State-wise Transaction Trends")
        df = get_data("""
            SELECT State,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM aggregated_transaction
            WHERE State != 'India'
            GROUP BY State
            ORDER BY Total_amount DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="State", y="Total_amount",
                     title="Top 10 States by Transaction Amount",
                     color="State")
        st.plotly_chart(fig, use_container_width=True)


# PAGE 3: USER & DEVICE ANALYSIS

elif page == "User & Device Analysis":
    st.title("📱 User & Device Analysis")

    tab1, tab2, tab3 = st.tabs([
        "Top Device Brands",
        "App Opens vs Users",
        "Year-wise User Growth"
    ])

    with tab1:
        st.subheader("Top Device Brands")
        df = get_data("""
            SELECT Brand,
                   SUM(User_count) AS Total_users,
                   ROUND(AVG(User_percentage)*100, 2) AS Avg_percentage
            FROM aggregated_user
            WHERE State = 'India'
            GROUP BY Brand
            ORDER BY Total_users DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="Brand", y="Total_users",
                     title="Top Device Brands by User Count",
                     color="Brand")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.pie(df, names="Brand", values="Total_users",
                      title="Device Brand Market Share")
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("App Opens vs Registered Users by State")
        df = get_data("""
            SELECT State,
                   SUM(Registered_users) AS Total_registered,
                   SUM(App_opens) AS Total_app_opens,
                   ROUND(SUM(App_opens)/SUM(Registered_users), 2) AS Opens_per_user
            FROM map_user
            WHERE State != 'India'
            GROUP BY State
            ORDER BY Opens_per_user DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="State", y="Opens_per_user",
                     title="App Opens per User by State",
                     color="State")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Year-wise User Growth")
        df = get_data("""
            SELECT Year,
                   SUM(User_count) AS Total_users
            FROM aggregated_user
            WHERE State = 'India'
            GROUP BY Year
            ORDER BY Year
        """)
        st.dataframe(df)
        fig = px.line(df, x="Year", y="Total_users",
                      title="Year-wise User Growth",
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)


# PAGE 4: INSURANCE ANALYSIS

elif page == "Insurance Analysis":
    st.title("🛡️ Insurance Analysis")

    tab1, tab2, tab3 = st.tabs([
        "Year-wise Growth",
        "Top States",
        "Quarter-wise Trend"
    ])

    with tab1:
        st.subheader("Year-wise Insurance Growth")
        df = get_data("""
            SELECT Year,
                   SUM(Insurance_count) AS Total_policies,
                   ROUND(SUM(Insurance_amount), 2) AS Total_amount
            FROM aggregated_insurance
            WHERE State = 'India'
            GROUP BY Year
            ORDER BY Year
        """)
        st.dataframe(df)
        fig = px.bar(df, x="Year", y="Total_policies",
                     title="Year-wise Insurance Policies",
                     color="Year")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Top States for Insurance")
        df = get_data("""
            SELECT State,
                   SUM(Insurance_count) AS Total_policies,
                   ROUND(SUM(Insurance_amount), 2) AS Total_amount
            FROM aggregated_insurance
            WHERE State != 'India'
            GROUP BY State
            ORDER BY Total_policies DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="State", y="Total_policies",
                     title="Top 10 States by Insurance Policies",
                     color="State")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Quarter-wise Insurance Trend")
        df = get_data("""
            SELECT Year, Quarter,
                   SUM(Insurance_count) AS Total_policies,
                   ROUND(SUM(Insurance_amount), 2) AS Total_amount
            FROM aggregated_insurance
            WHERE State = 'India'
            GROUP BY Year, Quarter
            ORDER BY Year, Quarter
        """)
        df["Year_Quarter"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        st.dataframe(df)
        fig = px.line(df, x="Year_Quarter", y="Total_policies",
                      title="Quarter-wise Insurance Trend",
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)


# PAGE 5: MARKET EXPANSION

elif page == "Market Expansion":
    st.title("🗺️ Market Expansion Analysis")

    tab1, tab2 = st.tabs([
        "Top Performing States",
        "Low Performing States"
    ])

    with tab1:
        st.subheader("Top States by Transaction Volume")
        df = get_data("""
            SELECT State,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM aggregated_transaction
            WHERE State != 'India'
            GROUP BY State
            ORDER BY Total_transactions DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="State", y="Total_transactions",
                     title="Top 10 States - Transaction Volume",
                     color="State")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Low Performing States — Expansion Opportunity")
        df = get_data("""
            SELECT State,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM aggregated_transaction
            WHERE State != 'India'
            GROUP BY State
            ORDER BY Total_transactions ASC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="State", y="Total_transactions",
                     title="Low Performing States",
                     color="State")
        st.plotly_chart(fig, use_container_width=True)


# PAGE 6: TOP PERFORMERS

elif page == "Top Performers":
    st.title("🏆 Top Performers")

    tab1, tab2, tab3 = st.tabs([
        "Top States",
        "Top Districts",
        "Top Pincodes"
    ])

    with tab1:
        st.subheader("Top States by Transaction")
        df = get_data("""
            SELECT Entity_name AS State,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM top_transaction
            WHERE Entity_type = 'states'
            GROUP BY Entity_name
            ORDER BY Total_transactions DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="State", y="Total_transactions",
                     title="Top 10 States",
                     color="State")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Top Districts by Transaction")
        df = get_data("""
            SELECT Entity_name AS District,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM top_transaction
            WHERE Entity_type = 'districts'
            GROUP BY Entity_name
            ORDER BY Total_transactions DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="District", y="Total_transactions",
                     title="Top 10 Districts",
                     color="District")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Top Pincodes by Transaction")
        df = get_data("""
            SELECT Entity_name AS Pincode,
                   SUM(Transaction_count) AS Total_transactions,
                   ROUND(SUM(Transaction_amount), 2) AS Total_amount
            FROM top_transaction
            WHERE Entity_type = 'pincodes'
            GROUP BY Entity_name
            ORDER BY Total_transactions DESC
            LIMIT 10
        """)
        st.dataframe(df)
        fig = px.bar(df, x="Pincode", y="Total_transactions",
                     title="Top 10 Pincodes",
                     color="Pincode")
        st.plotly_chart(fig, use_container_width=True)


# PAGE 7: INDIA MAP

elif page == "India Map":
    st.title("🗺️ India Transaction Map")

    map_option = st.selectbox("Select Category", [
        "Transactions",
        "Users",
        "Insurance"
    ])

    if map_option == "Transactions":
        df = get_data("""
            SELECT State,
                   SUM(Transaction_count) AS Value
            FROM aggregated_transaction
            WHERE State != 'India'
            GROUP BY State
        """)
        title = "Total Transactions by State"
        color = "Purples"

    elif map_option == "Users":
        df = get_data("""
            SELECT State,
                   SUM(Registered_users) AS Value
            FROM map_user
            WHERE State != 'India'
            GROUP BY State
        """)
        title = "Registered Users by State"
        color = "Blues"

    elif map_option == "Insurance":
        df = get_data("""
            SELECT State,
                   SUM(Insurance_count) AS Value
            FROM aggregated_insurance
            WHERE State != 'India'
            GROUP BY State
        """)
        title = "Insurance Policies by State"
        color = "Greens"

    state_name_map = {
        "andaman-&-nicobar-islands": "Andaman & Nicobar Island",
        "andhra-pradesh": "Andhra Pradesh",
        "arunachal-pradesh": "Arunachal Pradesh",
        "assam": "Assam",
        "bihar": "Bihar",
        "chandigarh": "Chandigarh",
        "chhattisgarh": "Chhattisgarh",
        "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli",
        "delhi": "Delhi",
        "goa": "Goa",
        "gujarat": "Gujarat",
        "haryana": "Haryana",
        "himachal-pradesh": "Himachal Pradesh",
        "jammu-&-kashmir": "Jammu & Kashmir",
        "jharkhand": "Jharkhand",
        "karnataka": "Karnataka",
        "kerala": "Kerala",
        "ladakh": "Ladakh",
        "lakshadweep": "Lakshadweep",
        "madhya-pradesh": "Madhya Pradesh",
        "maharashtra": "Maharashtra",
        "manipur": "Manipur",
        "meghalaya": "Meghalaya",
        "mizoram": "Mizoram",
        "nagaland": "Nagaland",
        "odisha": "Odisha",
        "puducherry": "Puducherry",
        "punjab": "Punjab",
        "rajasthan": "Rajasthan",
        "sikkim": "Sikkim",
        "tamil-nadu": "Tamil Nadu",
        "telangana": "Telangana",
        "tripura": "Tripura",
        "uttar-pradesh": "Uttar Pradesh",
        "uttarakhand": "Uttarakhand",
        "west-bengal": "West Bengal"
    }

    df["State"] = df["State"].map(state_name_map)
    df = df.dropna(subset=["State"])

    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Value",
        color_continuous_scale=color,
        title=title
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("State-wise Data Table")
    st.dataframe(df.sort_values("Value", ascending=False))
