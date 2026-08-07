import csv

def identity_exposure_score(privilege, mfa_enabled, last_login_days):
    score = 0.0
    if privilege == "domain_admin":
        score += 0.4
    elif privilege == "service_account":
        score += 0.3
    else:
        score += 0.1

    if mfa_enabled == "false":
        score += 0.4

    if int(last_login_days) > 30:
        score += 0.2

    return min(score, 1.0)

with open("lab-setup/identity-data.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for row in rows:
    row["identity_exposure_score"] = identity_exposure_score(
        row["privilege_level"], row["mfa_enabled"], row["last_login_days_ago"]
    )
    print(f"{row['username']}: Exposure = {row['identity_exposure_score']}")

with open("engine/scored-identities.csv", "w", newline="") as f:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n✅ Done! Saved to engine/scored-identities.csv")
