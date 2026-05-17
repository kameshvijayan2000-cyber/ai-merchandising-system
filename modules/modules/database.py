import sqlite3
import os

DB_FILE = "prp_garments.db"


def get_connection():

    conn = sqlite3.connect(DB_FILE)

    return conn


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # ================= STYLE MASTER =================
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS style_master (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        style_name TEXT UNIQUE,

        total_qty INTEGER,

        extra_percent REAL,

        cut_qty_percent REAL,

        sizes TEXT,

        colors TEXT,

        color_ratios TEXT

    )

    """)

    # ================= FABRIC STORE =================
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS fabric_store (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        roll_no TEXT,

        fabric TEXT,

        color TEXT,

        kg REAL

    )

    """)

    # ================= PRODUCTION =================
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS production_tracking (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        entry_date TEXT,

        process TEXT,

        entry_type TEXT,

        qty REAL,

        party TEXT,

        rate REAL,

        total REAL

    )

    """)

    conn.commit()

    conn.close()