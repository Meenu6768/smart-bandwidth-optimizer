import requests

data = {
    "users": [
        {"name": "User_A", "priority": "high",   "usage_mbps": 400},
        {"name": "User_B", "priority": "medium",  "usage_mbps": 250},
        {"name": "User_C", "priority": "low",     "usage_mbps": 600},
        {"name": "User_D", "priority": "high",    "usage_mbps": 150}
    ]
}

r = requests.post("http://localhost:5000/allocate", json=data)
print(r.json())