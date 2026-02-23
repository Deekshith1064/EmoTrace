import json
from activity_db import insert_log, fetch_all_logs

# Paste browser JSON here
browser_logs = [
    {
        "duration": 0,
        "timestamp": "2026-02-12T04:31:37.328Z",
        "url": "https://www.linkedin.com/..."
    }
]


# Insert logs into database
for log in browser_logs:
    insert_log(
        log["url"],
        log["duration"],
        log["timestamp"]
    )

print("Logs inserted successfully.\n")

# Verify insertion
all_logs = fetch_all_logs()
for row in all_logs:
    print(row)
