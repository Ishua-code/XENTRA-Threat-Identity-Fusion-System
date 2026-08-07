import csv
import requests
import time

def get_epss_score(cve_id):
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    response = requests.get(url)
    data = response.json()
    if data["data"]:
        return float(data["data"][0]["epss"])
    return 0.0

with open("scanner/real-scan-results.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print("Fetching EPSS scores for REAL OpenVAS scan findings...\n")

for row in rows:
    row["epss_score"] = get_epss_score(row["cve_id"])
    print(f"{row['cve_id']}: EPSS = {row['epss_score']}")
    time.sleep(0.5)

with open("engine/real-enriched-vulnerabilities.csv", "w", newline="") as f:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n✅ Real scan data enriched with EPSS scores.")
print("Saved to engine/real-enriched-vulnerabilities.csv")
