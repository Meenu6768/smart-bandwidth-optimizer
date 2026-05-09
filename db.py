import sqlite3
import time

DB = "bandwidth.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS allocations (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user      TEXT,
            priority  TEXT,
            usage_mbps    REAL,
            allocated_mbps REAL,
            congestion TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_allocation(results):
    conn = sqlite3.connect(DB)
    ts = time.strftime("%H:%M:%S")
    for r in results:
        conn.execute("""
            INSERT INTO allocations (timestamp, user, priority, usage_mbps, allocated_mbps, congestion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ts, r["user"], r["priority"], r["usage_mbps"], r["allocated_mbps"], r["congestion"]))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM allocations ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return [dict(r) for r in rows]