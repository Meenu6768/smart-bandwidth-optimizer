from flask import Flask, jsonify, request
from optimizer import allocate_bandwidth
from db import init_db, log_allocation, get_history
import time

app = Flask(__name__)
init_db()

@app.route("/allocate", methods=["POST"])
def allocate():
    data = request.get_json()
    if not data or "users" not in data:
        return jsonify({"error": "Provide a list of users with usage data"}), 400

    users = data["users"]
    result = allocate_bandwidth(users)
    log_allocation(result)

    return jsonify({
        "status": "ok",
        "timestamp": time.strftime("%H:%M:%S"),
        "allocations": result
    })

@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": get_history()})

@app.route("/dashboard", methods=["GET"])
def dashboard():
    history = get_history()
    if not history:
        return "<h3>No data yet. POST to /allocate first.</h3>"

    rows = ""
    for entry in history[-10:][::-1]:
        rows += f"<tr><td>{entry['timestamp']}</td><td>{entry['user']}</td><td>{entry['priority']}</td><td>{entry['usage_mbps']} Mbps</td><td><b>{entry['allocated_mbps']} Mbps</b></td></tr>"

    return f"""
    <html>
    <head>
      <title>Bandwidth Dashboard</title>
      <style>
        body {{ font-family: Arial, sans-serif; padding: 30px; background: #f4f6f9; }}
        h2 {{ color: #1A56A5; }}
        table {{ border-collapse: collapse; width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        th {{ background: #1A56A5; color: white; padding: 12px 16px; text-align: left; }}
        td {{ padding: 10px 16px; border-bottom: 1px solid #eee; }}
        tr:hover td {{ background: #f0f4ff; }}
      </style>
      <meta http-equiv="refresh" content="5">
    </head>
    <body>
      <h2>Smart Bandwidth Optimizer — Live Dashboard</h2>
      <p>Auto-refreshes every 5 seconds</p>
      <table>
        <tr><th>Time</th><th>User</th><th>Priority</th><th>Current Usage</th><th>Allocated</th></tr>
        {rows}
      </table>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)