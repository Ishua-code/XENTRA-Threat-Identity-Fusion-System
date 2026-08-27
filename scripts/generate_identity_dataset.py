import csv
import random

first_names = ["john", "sara", "amit", "riya", "raj", "priya", "arjun", "meena", "vikram", "anita"]
privilege_levels = ["domain_admin", "standard", "service_account"]
hosts = [f"192.168.1.{i}" for i in range(10, 25)]

random.seed(42)

identities = []
for i in range(30):
    name = f"{random.choice(first_names)}_{i}"
    privilege = random.choices(privilege_levels, weights=[0.2, 0.6, 0.2])[0]
    mfa = random.choices(["true", "false"], weights=[0.4, 0.6])[0]
    last_login = random.choice([1, 2, 5, 10, 15, 30, 45, 60, 90, 120])
    host = random.choice(hosts)
    identities.append((name, privilege, mfa, last_login, host))

with open("lab-setup/identity-data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["username", "privilege_level", "mfa_enabled", "last_login_days_ago", "owned_asset_ip"])
    writer.writerows(identities)

print(f"Generated lab-setup/identity-data.csv with {len(identities)} synthetic identities")
