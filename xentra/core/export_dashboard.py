import csv
import json
from datetime import datetime, timezone

def export_dashboard(output_path="engine/dashboard.json"):
    with open("engine/unified-risk-scores.csv") as f:
        findings = list(csv.DictReader(f))

    with open("engine/attack-paths.json") as f:
        attack_paths = json.load(f)

    with open("lab-setup/identity-data.csv") as f:
        identities = list(csv.DictReader(f))

    critical = [f for f in findings if float(f["unified_risk_score"]) > 0.7]

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": {
            "total_vulnerabilities": len(findings),
            "identities_monitored": len(identities),
            "critical_findings": len(critical),
            "active_incidents": len(attack_paths),
        },
        "findings": findings[:10],
        "attack_paths": attack_paths[:10],
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Dashboard data exported to {output_path}")

if __name__ == "__main__":
    export_dashboard()
