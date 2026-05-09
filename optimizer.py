TOTAL_BANDWIDTH = 1000  # Total available Mbps

PRIORITY_WEIGHTS = {
    "high":   3,
    "medium": 2,
    "low":    1
}

def allocate_bandwidth(users):
    """
    Priority-weighted fair queuing algorithm.
    Users with high priority get proportionally more bandwidth.
    Congestion is reduced by capping greedy users.
    """
    # Step 1 — assign weight to each user
    for user in users:
        user["weight"] = PRIORITY_WEIGHTS.get(user.get("priority", "low"), 1)

    total_weight = sum(u["weight"] for u in users)

    # Step 2 — calculate fair share based on weight
    results = []
    for user in users:
        fair_share = (user["weight"] / total_weight) * TOTAL_BANDWIDTH
        requested  = user.get("usage_mbps", 0)

        # Step 3 — cap allocation: don't give more than requested, floor at 10 Mbps
        allocated = round(min(fair_share, requested * 1.2), 2)
        allocated = max(allocated, 10)

        congestion = "Yes" if requested > fair_share * 1.5 else "No"

        results.append({
            "user":           user["name"],
            "priority":       user.get("priority", "low"),
            "usage_mbps":     requested,
            "allocated_mbps": allocated,
            "congestion":     congestion
        })

    # Sort by allocated descending
    results.sort(key=lambda x: x["allocated_mbps"], reverse=True)
    return results