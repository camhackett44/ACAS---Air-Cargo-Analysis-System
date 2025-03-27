import streamlit as st
import sqlite3
import pandas as pd

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("cargo_database.db")
    return conn

# Load available options for filtering
def get_options(column):
    conn = get_db_connection()
    query = f"SELECT DISTINCT {column} FROM CargoFlights ORDER BY {column};"
    options = pd.read_sql(query, conn)[column].dropna().tolist()
    conn.close()
    return options

# Streamlit app
def main():
    st.set_page_config(page_title="Cargo Route Analysis", layout="wide")
    st.title("📊 Cargo Route Profitability & Demand Analysis")

    # Sidebar Navigation
    page = st.sidebar.radio("Select Page", ["Home", "Flight Data Lookup", "Summarized Data", "Preset Queries", "Custom Query"])

    if page == "Home":
        st.header("🏠 Welcome to the Cargo Analytics Dashboard")
        st.markdown("""
        This dashboard lets you explore detailed insights into global air cargo operations, flight data, and airline performance.

        **🔍 Pages Overview:**
        - **Flight Data Lookup**: See individual flight records and apply detailed filters.
        - **Summarized Data**: View total cargo volumes and flights per airline, grouped by year.
        - **Preset Queries**: One-click access to powerful pre-defined analytics.
        - **Custom Query**: Run your own raw SQL query directly against the database.

        **📁 Data Sources:** U.S. DOT T-100 Segment Data (filtered by selected cargo airlines)

        _For the most accurate results, ensure the database is up-to-date with all relevant CSVs._
        """)

    elif page == "Flight Data Lookup":
        st.header("🔍 Flight Data Lookup")
        st.markdown("_Tip: Use this page to explore individual flights. Combine filters like aircraft variant, airline, and region for precise slices of data._")

        st.sidebar.header("Filters")
        selected_year = st.sidebar.selectbox("Select Year", ["All"] + get_options("YEAR"))
        selected_airline = st.sidebar.selectbox("Select Airline", ["All"] + get_options("AIRLINE_NAME"))
        selected_airline_group = st.sidebar.selectbox("Select Airline Group", ["All"] + get_options("AIRLINE_GROUP"))
        selected_aircraft = st.sidebar.selectbox("Select Aircraft Model", ["All"] + get_options("AIRCRAFT_MODEL"))
        selected_variant = st.sidebar.selectbox("Select Aircraft Variant", ["All"] + get_options("AIRCRAFT_VARIANT"))
        selected_origin = st.sidebar.selectbox("Select Origin Airport", ["All"] + get_options("ORIGIN"))
        selected_origin_city = st.sidebar.selectbox("Select Origin City", ["All"] + get_options("ORIGIN_CITY_NAME"))
        selected_dest = st.sidebar.selectbox("Select Destination Airport", ["All"] + get_options("DEST"))
        selected_dest_city = st.sidebar.selectbox("Select Destination City", ["All"] + get_options("DEST_CITY_NAME"))
        selected_region = st.sidebar.selectbox("Select Region", ["All"] + get_options("REGION"))
        exclude_belly_cargo = st.sidebar.checkbox("Exclude Belly Cargo (Freighters Only)")

        st.sidebar.header("📌 Display Options")
        available_columns = ["YEAR", "AIRLINE_NAME", "AIRLINE_GROUP", "AIRCRAFT_MODEL", "AIRCRAFT_VARIANT", "ORIGIN", "ORIGIN_CITY_NAME", "DEST", "DEST_CITY_NAME", "FREIGHT", "MAIL", "DISTANCE", "DEPARTURES_PERFORMED", "FREIGHT_PER_FLIGHT"]
        selected_columns = st.sidebar.multiselect("Select Columns to Display", available_columns, default=["YEAR", "AIRLINE_NAME", "AIRCRAFT_MODEL", "AIRCRAFT_VARIANT", "ORIGIN", "DEST", "FREIGHT", "MAIL", "DEPARTURES_PERFORMED"])
        order_by_column = st.sidebar.selectbox("Order Results By", selected_columns, index=selected_columns.index("FREIGHT") if "FREIGHT" in selected_columns else 0)

        query = f"SELECT {', '.join(selected_columns)} FROM CargoFlights WHERE 1=1"
        params = []

        if selected_year != "All":
            query += " AND YEAR = ?"
            params.append(selected_year)

        if selected_airline != "All":
            query += " AND AIRLINE_NAME = ?"
            params.append(selected_airline)

        if selected_airline_group != "All":
            query += " AND AIRLINE_GROUP = ?"
            params.append(selected_airline_group)

        if selected_aircraft != "All":
            query += " AND AIRCRAFT_MODEL = ?"
            params.append(selected_aircraft)

        if selected_variant != "All":
            query += " AND AIRCRAFT_VARIANT = ?"
            params.append(selected_variant)

        if selected_origin != "All":
            query += " AND ORIGIN = ?"
            params.append(selected_origin)

        if selected_origin_city != "All":
            query += " AND ORIGIN_CITY_NAME = ?"
            params.append(selected_origin_city)

        if selected_dest != "All":
            query += " AND DEST = ?"
            params.append(selected_dest)

        if selected_dest_city != "All":
            query += " AND DEST_CITY_NAME = ?"
            params.append(selected_dest_city)

        if selected_region != "All":
            query += " AND REGION = ?"
            params.append(selected_region)

        if exclude_belly_cargo:
            query += " AND AIRCRAFT_VARIANT LIKE '%F'"

        query += f" ORDER BY {order_by_column} DESC;"

        conn = get_db_connection()
        df_results = pd.read_sql(query, conn, params=params)
        df_results["YEAR"] = df_results["YEAR"].astype(str).str.replace(",", "")
        conn.close()

        st.subheader("📌 Filtered Cargo Data")
        st.dataframe(df_results)

    elif page == "Summarized Data":
        st.header("📊 Summarized Cargo Data")
        st.markdown("_Tip: Select a year or airline group to view yearly summaries above and full totals below. Selecting 'All' years will show total cargo per airline across all years._")

        st.sidebar.header("Filters")
        selected_year = st.sidebar.selectbox("Select Year", ["All"] + get_options("YEAR"))
        selected_airline = st.sidebar.selectbox("Select Airline", ["All"] + get_options("AIRLINE_NAME"))
        selected_airline_group = st.sidebar.selectbox("Select Airline Group", ["All"] + get_options("AIRLINE_GROUP"))

        base_query = "SELECT YEAR, AIRLINE_NAME, SUM(FREIGHT + MAIL) AS TotalCargo, SUM(DEPARTURES_PERFORMED) AS TotalFlights FROM CargoFlights WHERE 1=1"
        total_query = "SELECT AIRLINE_NAME, SUM(FREIGHT + MAIL) AS TotalCargo, SUM(DEPARTURES_PERFORMED) AS TotalFlights FROM CargoFlights WHERE 1=1"
        params = []
        total_params = []

        if selected_year != "All":
            base_query += " AND YEAR = ?"
            total_query += " AND YEAR = ?"
            params.append(selected_year)
            total_params.append(selected_year)

        if selected_airline != "All":
            base_query += " AND AIRLINE_NAME = ?"
            total_query += " AND AIRLINE_NAME = ?"
            params.append(selected_airline)
            total_params.append(selected_airline)

        if selected_airline_group != "All":
            base_query += " AND AIRLINE_GROUP = ?"
            total_query += " AND AIRLINE_GROUP = ?"
            params.append(selected_airline_group)
            total_params.append(selected_airline_group)

        grouped_query = base_query + " GROUP BY YEAR, AIRLINE_NAME ORDER BY YEAR, TotalCargo DESC"

        conn = get_db_connection()
        df_summary = pd.read_sql(grouped_query, conn, params=params)
        df_summary["YEAR"] = df_summary["YEAR"].astype(str).str.replace(",", "")
        df_total = pd.read_sql(total_query + " GROUP BY AIRLINE_NAME ORDER BY TotalCargo DESC", conn, params=total_params)
        conn.close()

        df_total["Total"] = df_total["TotalCargo"] + df_total["TotalFlights"]

        st.subheader("📌 Cargo Summary Per Airline")
        st.dataframe(df_summary)
        st.subheader("📌 Total Cargo Summary")
        st.dataframe(df_total)

    elif page == "Preset Queries":
        st.header("📌 Preset Queries")
        st.markdown("Select a query below to explore interesting insights from the cargo dataset.")

        query_options = {
            "Top 10 Airlines by Total Cargo": {
                "sql": """
                    SELECT AIRLINE_NAME, SUM(FREIGHT + MAIL) AS TotalCargo, SUM(DEPARTURES_PERFORMED) AS TotalFlights
                    FROM CargoFlights
                    GROUP BY AIRLINE_NAME
                    ORDER BY TotalCargo DESC
                    LIMIT 10;
                """,
                "visualize": False
            },
            "Monthly Cargo Trends for FedEx Express": {
                "sql": """
                    SELECT YEAR, MONTH, SUM(FREIGHT + MAIL) AS MonthlyCargo
                    FROM CargoFlights
                    WHERE AIRLINE_NAME = 'FedEx Express'
                    GROUP BY YEAR, MONTH
                    ORDER BY YEAR, MONTH;
                """,
                "visualize": True
            },
            "Top Origin Airports by Cargo Volume": {
                "sql": """
                    SELECT ORIGIN, ORIGIN_CITY_NAME, SUM(FREIGHT + MAIL) AS TotalCargo
                    FROM CargoFlights
                    GROUP BY ORIGIN, ORIGIN_CITY_NAME
                    ORDER BY TotalCargo DESC
                    LIMIT 10;
                """,
                "visualize": False
            },
            "Most Efficient Aircraft (Freight per Flight)": {
                "sql": """
                    SELECT AIRCRAFT_VARIANT, AVG(FREIGHT_PER_FLIGHT) AS AvgFreightPerFlight
                    FROM CargoFlights
                    GROUP BY AIRCRAFT_VARIANT
                    ORDER BY AvgFreightPerFlight DESC
                    LIMIT 10;
                """,
                "visualize": True
            },
            "Yearly Cargo Totals for Emirates": {
                "sql": """
                    SELECT YEAR, SUM(FREIGHT + MAIL) AS TotalCargo
                    FROM CargoFlights
                    WHERE AIRLINE_NAME = 'Emirates'
                    GROUP BY YEAR
                    ORDER BY YEAR;
                """,
                "visualize": True
            }
        }

        selected_query = st.selectbox("Choose a preset query:", list(query_options.keys()))
        if st.button("Run Query"):
            conn = get_db_connection()
            result = pd.read_sql(query_options[selected_query]["sql"], conn)
            conn.close()
            st.dataframe(result)

    elif page == "Custom Query":
        st.header("🛠️ Custom SQL Query")
        st.markdown("_Tip: Make sure to include_ `SUM(DEPARTURES_PERFORMED) AS TotalFlights` _in your SELECT clause if you're aggregating flight data._")
        query = st.text_area("Enter your SQL query:", height=200)

        if st.button("Run Query"):
            try:
                conn = get_db_connection()
                df_custom = pd.read_sql(query, conn)
                conn.close()
                st.success("Query executed successfully!")
                st.dataframe(df_custom)
            except Exception as e:
                st.error(f"Error running query: {e}")

if __name__ == "__main__":
    main()
