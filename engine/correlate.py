import csv

with open("engine/real-enriched-vulnerabilities.csv") as f:
    vulns = list(csv.DictReader(f))

with open("engine/scored-identities.csv") as f:
    identities = list(csv.DictReader(f))

asset_to_identity = {i["owned_asset_ip"]: i for i in identities}

results = []
for v in vulns:
    host = v["host"]
    identity = asset_to_identity.get(host)

    epss = float(v["epss_score"])
    identity_score = float(identity["identity_exposure_score"]) if identity else 0.0

    unified_risk_score = round((epss * 0.5) + (identity_score * 0.5), 3)

    results.append({
        "cve_id": v["cve_id"],
        "host": host,
        "owner": identity["username"] if identity else "unknown",
        "epss_score": epss,
        "identity_exposure_score": identity_score,
        "unified_risk_score": unified_risk_score
    })

results.sort(key=lambda x: x["unified_risk_score"], reverse=True)

with open("engine/unified-risk-scores.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("✅ Unified Risk Scores (highest risk first):\n")
for r in results:
    print(r)
