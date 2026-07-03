import sqlite3
from datetime import datetime

DB_PATH = "power_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp      TEXT,
            device         TEXT,
            voltage        REAL,
            current        REAL,
            calc_power     REAL,
            api_power      REAL,
            hybrid_power   REAL,
            predicted_total REAL,
            category       TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            kwh       REAL,
            cost      REAL
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialised.")

def insert_reading(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO readings
        (timestamp, device, voltage, current, calc_power,
         api_power, hybrid_power, predicted_total, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data.get("device"),
        data.get("voltage"),
        data.get("current"),
        data.get("calc_power"),
        data.get("api_power"),
        data.get("hybrid_power"),
        data.get("predicted_total"),
        data.get("category")
    ))
    conn.commit()
    conn.close()

def get_recent_readings(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def insert_bill(kwh, cost):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO bills (timestamp, kwh, cost) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), kwh, cost))
    conn.commit()
    conn.close()