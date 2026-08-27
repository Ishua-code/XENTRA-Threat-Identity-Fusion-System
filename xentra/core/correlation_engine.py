import csv
import yaml
from xentra.utils.logger import get_logger

logger = get_logger("CorrelationEngine")

class CorrelationEngine:
    def __init__(self, config_path="xentra/config/settings.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.paths = self.config["paths"]
        self.epss_weight = self.config["scoring"]["epss_weight"]
        self.identity_weight = self.config["scoring"]["identity_weight"]

    def run(self):
        logger.info("Loading enriched vulnerabilities and scored identities...")
        with open(self.paths["enriched_vulnerabilities"]) as f:
            vulns = list(csv.DictReader(f))
        with open(self.paths["scored_identities"]) as f:
            identities = list(csv.DictReader(f))

        asset_to_identity = {i["owned_asset_ip"]: i for i in identities}

        results = []
        for v in vulns:
            host = v["host"]
            identity = asset_to_identity.get(host)
            epss = float(v["epss_score"])
            identity_score = float(identity["identity_exposure_score"]) if identity else 0.0

            unified_score = round(
                (epss * self.epss_weight) + (identity_score * self.identity_weight), 3
            )

            results.append({
                "cve_id": v["cve_id"],
                "host": host,
                "owner": identity["username"] if identity else "unknown",
                "epss_score": epss,
                "identity_exposure_score": identity_score,
                "unified_risk_score": unified_score
            })

        results.sort(key=lambda x: x["unified_risk_score"], reverse=True)

        with open(self.paths["unified_scores"], "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        logger.info(f"Unified risk scores saved to {self.paths['unified_scores']}")
        return results
