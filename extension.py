import json
import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# File containing logged time data from the Chrome extension
TIME_LOG_FILE = 'time_log.json'

# Check if the file exists
if not os.path.exists(TIME_LOG_FILE):
    print(f"❌ '{TIME_LOG_FILE}' not found. Please make sure the file exists.")
    exit()

# Load time tracking data
with open(TIME_LOG_FILE, 'r') as file:
    time_logs = json.load(file)

# Aggregate time per category
category_time = defaultdict(int)
for entry in time_logs:
    domain = entry.get('domain', 'unknown.com')
    category = entry.get('category', 'Uncategorized')
    time_spent = entry.get('time_spent', 0)
    category_time[category] += time_spent

# Convert time from seconds to hours
category_hours = {cat: round(seconds / 3600, 2) for cat, seconds in category_time.items()}

# Console Summary
print("\n📊 Productivity Summary:")
for category, hours in category_hours.items():
    print(f" - {category}: {hours} hrs")

# Pie Chart
plt.figure(figsize=(7, 7))
plt.pie(category_hours.values(), labels=category_hours.keys(), autopct='%1.1f%%', startangle=140)
plt.title("Time Spent by Category")
plt.axis('equal')
plt.tight_layout()
plt.show()

# Export to CSV
CSV_FILE = 'productivity_summary.csv'
with open(CSV_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Category", "Time (hours)"])
    for cat, hrs in category_hours.items():
        writer.writerow([cat, hrs])

print(f"\n✅ Summary exported to '{CSV_FILE}'")