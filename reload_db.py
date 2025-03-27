import pandas as pd
import sqlite3

# Paths to yearly cargo data CSV files
file_paths = {
    "2018": "T_T100_SEGMENT_ALL_CARRIER_2018.csv",
    "2019": "T_T100_SEGMENT_ALL_CARRIER_2019.csv",
    "2020": "T_T100_SEGMENT_ALL_CARRIER_2020.csv",
    "2021": "T_T100_SEGMENT_ALL_CARRIER_2021.csv",
    "2022": "T_T100_SEGMENT_ALL_CARRIER_2022.csv",
    "2023": "T_T100_SEGMENT_ALL_CARRIER_2023.csv",
    "2024": "T_T100_SEGMENT_ALL_CARRIER_2024.csv"
}

# Load aircraft variants mapping
aircraft_variants = pd.read_csv("AIRCRAFT_VARIANTS.csv", dtype=str)
aircraft_variants["AIRCRAFT_TYPE_CODE"] = aircraft_variants["AIRCRAFT_TYPE_CODE"].astype(str).str.zfill(3)
aircraft_variants["UNIQUE_CARRIER_NAME"] = aircraft_variants["UNIQUE_CARRIER_NAME"].str.upper().str.strip()

# List of major cargo airlines
cargo_airlines = {
    "FEDERAL EXPRESS CORPORATION", "UNITED PARCEL SERVICE", "ATLAS AIR INC.",
    "KALITTA AIR LLC", "POLAR AIR CARGO AIRWAYS", "LUFTHANSA GERMAN AIRLINES",
    "QATAR AIRWAYS (Q.C.S.C)", "EMIRATES", "KOREAN AIR LINES CO. LTD.",
    "TURK HAVA YOLLARI A.O.", "CARGOLUX AIRLINES INTERNATIONAL S.A",
    "CHINA SOUTHERN AIRLINES", "ASIANA AIRLINES INC.", "ETIHAD AIRWAYS", 
    "KLM ROYAL DUTCH AIRLINES", "TAM LINHAS AEREAS SA DBA LATAM AIRLINES BRASIL", 
    "CATHAY PACIFIC AIRWAYS LTD.", "ALL NIPPON AIRWAYS CO.", "EUROPEAN AIR TRANSPORT LEIPZIG GMBH", 
    "MALAYSIAN AIRLINE SYSTEM", "AMERIJET INTERNATIONAL", "KALITTA CHARTERS II",
    "ALOHA AIR CARGO", "AEROFLOT RUSSIAN AIRLINES", "EL AL ISRAEL AIRLINES LTD.",
    "CHINA AIRLINES LTD.", "CARGOJET AIRWAYS LTD.", "ABX AIR INC",
    "VOLGA-DNEPR AIRLINES", "SKY LEASE CARGO", "WESTERN GLOBAL",
    "EVA AIRWAYS CORPORATION", "AEROLOGIC GMBH", "SINGAPORE AIRLINES LTD.",
    "MARTINAIR HOLLAND N.V.", "SILK WAY WEST AIRLINES", "CARGOLUX ITALIA SPA",
    "CHINA CARGO AIRLINE", "ETHIOPIAN AIRLINES", "ALASKA AIRLINES INC.", 
    "TRANSPORTES AEREOS MERCANTILES PANAMERICANOS S.A", "LAN COLOMBIA", "LAN ECUADOR",
    "LAN-CHILE AIRLINES", "AIR TRANSPORT INTERNATIONAL", "AIR CHINA",
    "COMPAGNIE NATL AIR FRANCE", "AIR ATLANTA ICELANDIC", "DHL AERO EXPRESSO",
    "AEROTRANSPORTES MAS DE CRGA", "ABSA-AEROLINHAS BRASILEIRAS", "CHALLENGE AIRLINES (BE) S.A.",
    "ICELANDAIR", "SAUDI ARABIAN AIRLINES CORP", "NATIONAL AIR CARGO GROUP INC DBA NATIONAL AIRLINES",
    "ANTONOV COMPANY", "NORTHERN AIR CARGO INC.", "AIR CANADA",
    "AIRBRIDGECARGO AIRLINES LIMITED", "AEROUNION AEROTRANSPORTE DE CARGA UNION SA DE CV",
    "CARGOLOGICAIR LIMITED", "SOUTHERN AIR INC.", "NIPPON CARGO AIRLINES",
    "SUN COUNTRY AIRLINES D/B/A MN AIRLINES", "21 AIR LLC", "HAWAIIAN AIRLINES INC.",
}

# Connect to SQLite database
db_path = "cargo_database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop old table if it exists and create a new one
cursor.execute("DROP TABLE IF EXISTS CargoFlights;")
cursor.execute("""
    CREATE TABLE CargoFlights (
        DEPARTURES_PERFORMED INTEGER,
        PAYLOAD REAL,
        FREIGHT REAL,
        MAIL REAL,
        DISTANCE REAL,
        UNIQUE_CARRIER TEXT,
        UNIQUE_CARRIER_NAME TEXT,
        AIRLINE_NAME TEXT,
        AIRLINE_GROUP TEXT,
        REGION TEXT,
        ORIGIN TEXT,
        ORIGIN_CITY_NAME TEXT,
        DEST TEXT,
        DEST_CITY_NAME TEXT,
        AIRCRAFT_TYPE TEXT,
        AIRCRAFT_VARIANT TEXT,
        AIRCRAFT_MODEL TEXT,
        AIRCRAFT_MANUFACTURER TEXT,
        YEAR INTEGER,
        MONTH INTEGER,
        FREIGHT_PER_FLIGHT INTEGER
    );
""")

print("✅ Database setup complete. Processing files...")

# Process each year
for year, file_path in file_paths.items():
    print(f"📥 Loading {year} data...")

    df = pd.read_csv(file_path, dtype=str)

    # Convert numeric columns
    numeric_cols = ["DEPARTURES_PERFORMED", "PAYLOAD", "FREIGHT", "MAIL", "DISTANCE", "YEAR", "MONTH"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Filter to only include cargo airlines from aircraft variants mapping
    df_cargo = df[df["UNIQUE_CARRIER_NAME"].str.upper().isin(aircraft_variants["UNIQUE_CARRIER_NAME"].unique())].copy()

    # **🚨 IMPORTANT: Ensure only flights with freight or mail are included**
    df_cargo = df_cargo[(df_cargo["FREIGHT"] > 0) | (df_cargo["MAIL"] > 0)]

    # Compute freight per flight (ensuring whole numbers)
    df_cargo["FREIGHT_PER_FLIGHT"] = ((df_cargo["FREIGHT"] + df_cargo["MAIL"]) / df_cargo["DEPARTURES_PERFORMED"]).fillna(0).astype(int)

    # Normalize formatting for aircraft type and airline names
    df_cargo["AIRCRAFT_TYPE"] = df_cargo["AIRCRAFT_TYPE"].astype(str).str.zfill(3)
    df_cargo["UNIQUE_CARRIER_NAME"] = df_cargo["UNIQUE_CARRIER_NAME"].str.upper().str.strip()

    # Merge to assign aircraft variant, airline name, group, model, and manufacturer
    df_cargo = df_cargo.merge(
        aircraft_variants[
            ["AIRCRAFT_TYPE_CODE", "UNIQUE_CARRIER_NAME", "AIRLINE_NAME", "AIRLINE_GROUP", "AIRCRAFT_VARIANT", "AIRCRAFT_MODEL", "AIRCRAFT_MANUFACTURER"]
        ],
        left_on=["AIRCRAFT_TYPE", "UNIQUE_CARRIER_NAME"],
        right_on=["AIRCRAFT_TYPE_CODE", "UNIQUE_CARRIER_NAME"],
        how="left"
    )

    # Drop redundant merge column
    df_cargo.drop(columns=["AIRCRAFT_TYPE_CODE"], inplace=True)

    # Insert data into SQLite
    df_cargo.to_sql("CargoFlights", conn, if_exists="append", index=False)

    print(f"✅ {year} data processed & inserted.")

# Close database connection
conn.close()
print("🔌 Database connection closed.")
print("✅ All years processed & inserted into SQL successfully!")
