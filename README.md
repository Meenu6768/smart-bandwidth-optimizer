Smart Bandwidth Optimizer
Show Image
Show Image
Show Image
Show Image
A Flask-powered REST API that implements a priority-weighted fair queuing algorithm for dynamic bandwidth allocation across multiple users. Includes a live auto-refreshing web dashboard and persistent SQLite logging.

 Live Dashboard

Access at http://localhost:5000/dashboard — auto-refreshes every 5 seconds.

TimeUserPriorityCurrent UsageAllocated18:20:15User_Ahigh400 Mbps333.33 Mbps18:20:15User_Bmedium250 Mbps222.22 Mbps18:20:15User_Dhigh150 Mbps180.00 Mbps18:20:15User_Clow600 Mbps111.11 Mbps  Congestion

 Features

 Priority queuing algorithm — distributes 1000 Mbps across users using weighted fair queuing (High: 3x, Medium: 2x, Low: 1x)
Congestion detection — flags users consuming far beyond their fair share
REST API — 3 clean endpoints for allocation, history, and dashboard
Live dashboard — real-time HTML table with auto-refresh
SQLite persistence — every allocation logged with full history
Zero external DB setup — SQLite works out of the box

 Tech Stack
ToolPurposeFlaskREST API and dashboard serverSQLite3Persistent allocation loggingPythonPriority-weighted queuing algorithm

 Getting Started
Prerequisites
bashpip install flask
Run
Terminal 1 — Start the API server:
bashpython app.py
Terminal 2 — Send test data:
bashpython test.py
Open dashboard in browser:
http://localhost:5000/dashboard

API Endpoints
POST /allocate
Accepts a list of users with their priority and current usage. Returns optimized bandwidth allocation.
Request:
json{
  "users": [
    {"name": "User_A", "priority": "high",   "usage_mbps": 400},
    {"name": "User_B", "priority": "medium", "usage_mbps": 250},
    {"name": "User_C", "priority": "low",    "usage_mbps": 600}
  ]
}
Response:
json{
  "status": "ok",
  "timestamp": "18:20:15",
  "allocations": [
    {"user": "User_A", "priority": "high",   "allocated_mbps": 375.0,  "congestion": "No"},
    {"user": "User_B", "priority": "medium", "allocated_mbps": 250.0,  "congestion": "No"},
    {"user": "User_C", "priority": "low",    "allocated_mbps": 125.0,  "congestion": "Yes"}
  ]
}
GET /history
Returns the last 50 allocation records from the database.
GET /dashboard
Returns an auto-refreshing HTML dashboard showing recent allocations.

Algorithm — Priority-Weighted Fair Queuing
Priority Weights:  High = 3,  Medium = 2,  Low = 1

Fair Share = (User Weight / Total Weight) × 1000 Mbps
Allocated  = min(Fair Share, Requested × 1.2), floored at 10 Mbps
Congestion = flagged if Requested > Fair Share × 1.5
This prevents any single low-priority user from starving the network while ensuring high-priority users always get proportionally more bandwidth.

 Project Structure
smart_bandwidth_optimizer/
│
├── app.py          # Flask API — 3 routes: /allocate, /history, /dashboard
├── optimizer.py    # Priority-weighted fair queuing algorithm
├── db.py           # SQLite init, logging, and retrieval
├── test.py         # Sample POST request for testing
└── bandwidth.db    # Auto-generated: SQLite database

 Future Improvements

 Real-time chart on dashboard using Chart.js
 WebSocket-based live updates instead of meta-refresh
 Authentication layer for admin access
 Dynamic total bandwidth configuration via API


📄 License
MIT License — free to use, modify, and distribute.
