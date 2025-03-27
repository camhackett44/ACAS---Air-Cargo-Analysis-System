# 📦 Air Cargo Profitability & Demand Analysis Dashboard

Welcome to the **Cargo Route Profitability & Demand Analysis** project — an interactive analytics dashboard built with **Python**, **Pandas**, and **Streamlit**, designed to provide deep insights into global air cargo traffic based on U.S. DOT **T-100 Segment Data**.

This tool transforms thousands of flight records into a powerful visual and tabular interface for exploring airline operations, cargo volumes, aircraft utilization, and route profitability across dozens of major cargo carriers.

---

## ✈️ What This Dashboard Does

This project enables users to:

- 🔍 **Search** individual flight data by year, airline, aircraft model/variant, region, city, or airport  
- 📊 **Summarize** performance metrics like total freight, mail, and flight operations by airline or airline group  
- 📈 **Visualize trends** over time: growth, aircraft efficiency, regional patterns, and more  
- 💻 **Run custom SQL queries** directly on the dataset  
- 🧠 **Explore preset queries and graphs** for quick access to valuable insights  
- 🛠️ **Filter and order results dynamically** — great for both aviation analysts and data enthusiasts

---

## 📁 Data Source

All data is derived from the [U.S. Bureau of Transportation Statistics](https://www.transtats.bts.gov/) — specifically the **T-100 Segment (All Carriers)** dataset. This includes monthly operational records of U.S. and foreign carriers operating in U.S. airspace.

Additional mapping and enrichment is performed through a custom `AIRCRAFT_VARIANTS.csv` file, which links raw aircraft codes to real-world aircraft variants, airline names, and parent airline groups.

---

## 🚀 Features

- 🔹 **Two Modes of Exploration**
  - **Flight Lookup**: Browse individual flight-level records with full filter control
  - **Summarized Data**: View totals per airline, per year, and by group, with rollups

- 🔹 **Smart Filtering**
  - Year, airline, group, aircraft, route, freighter-only toggle, city names, and more

- 🔹 **Preset Query Library**
  - One-click access to high-value insights (top routes, busiest carriers, efficient aircraft)

- 🔹 **Custom SQL Editor**
  - Build and execute raw SQL queries with visual support

- 🔹 **Auto-Built Database**
  - All data is loaded from CSV and preprocessed via `reload_db.py`

---

## ⚙️ Installation & Setup

### 🪟 Windows Users

1. Download the repo as a ZIP and extract it  
2. Double-click `launch.bat`  
3. The dashboard will install everything and launch automatically in your browser

### 🍎 macOS / Linux Users

1. Open Terminal in this project folder  
2. Run the following:
```bash
chmod +x setup.sh
./setup.sh
```

---

## 🔧 File Overview

| File | Description |
|------|-------------|
| `reload_db.py` | Loads CSVs into a normalized SQLite database |
| `dashboard.py` | Main Streamlit dashboard logic |
| `run_app.py` | Launches both loader and dashboard in one command |
| `setup.sh / launch.bat` | One-click launchers for Linux/macOS and Windows |
| `requirements.txt` | Python dependencies (auto-installed) |
| `AIRCRAFT_VARIANTS.csv` | Custom mapping of aircraft types and airlines |
| `T_T100_*.csv` | BTS raw monthly data (2018–2024 recommended) |

---

## 🧠 Use Cases

- ✈️ **Airline Route Optimization**  
- 📦 **Freight Volume Analysis**  
- 💰 **Investment Research & Cargo Trends**  
- 🧪 **Academic and Student Projects**  
- 📊 **Market Research & Strategic Planning**

---

## 🧑‍💻 Built With

- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [SQLite](https://www.sqlite.org/index.html)  
- [Pandas](https://pandas.pydata.org/)  
- [DOT T-100 Dataset](https://www.transtats.bts.gov/Fields.asp?Table_ID=293)

---

## 📌 Notes

- This app runs **locally** and does not upload or share your data  
- You are free to modify, add airlines, and extend this tool for your own analyses  
- Designed to be lightweight, portable, and installable without any cloud services

---

## 🧳 Author

**Cameron Hackett**  
📍 Computer Science & Political Science, University of Miami  
📫 [LinkedIn](https://www.linkedin.com/in/cameron-hackett-um) • [GitHub](https://github.com/camhackett44)
