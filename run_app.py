import subprocess
import os

print("🚀 Setting up database...")
subprocess.run(["python3", "reload_db.py"], check=True)

print("📊 Launching dashboard...")
subprocess.run(["python3", "-m", "streamlit", "run", "dashboard.py"])